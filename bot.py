import unicodedata

knowledge = [
        ('ψηφιακή σχεδίαση', 'καραμπατζάκη', 'δευτέρα', 16, 20),
        ('θεωρίες μάθησης', 'τσινάκο', 'τρίτη', 13, 15),
        ('διακριτά μαθηματικά', 'λάγκα', 'πέμπτη', 14, 18),
        ('προγραμματισμό με c++', 'μωυσιάδη', 'πέμπτη', 18, 21),
        ('αγγλικά', 'χριστοδουλίδου', 'παρασκευή', 8, 10),
        ('μαθηματικά', 'λάγκα', 'παρασκευή', 16, 20)
]

def and_join(arr):
    if len(arr) == 0:
        return ""
    if len(arr) == 1:
        return str(arr[0])
    return ', '.join(arr[:-1]) + ' και ' + arr[-1]

def tokenizer(sentence):
    tokens = []
    token = ''
    for c in sentence:
        if c == ' ':
            if token != '':
                tokens.append(token)
                token = ''
        elif c in ['.', ',', ';', '!', ':', '(', ')', '-', '«', '»', '\'', '"']:
            if token != '':
                tokens.append(token)
                token = ''
            tokens.append(c)
        else:
            token += c
    if token != '': tokens.append(token)
    return tokens

class Stem:
    def __init__(self, name, values):
        self.name = name
        self.values = values

stems = [
        Stem('δευτέρα', [['δευτέρα'], ['δευτέρας'], ['δευτέρες']]),
        Stem('τρίτη', [['τρίτη'], ['τρίτης'], ['τρίτες']]),
        Stem('τετάρτη', [['τετάρτη'], ['τετάρτης'], ['τετάρτες']]),
        Stem('πέμπτη', [['πέμπτη'], ['πέμπτης'], ['πέμπτες']]),
        Stem('παρασκευή', [['παρασκευή'], ['παρασκευής'], ['παρασκευές']]),
        Stem('ψηφιακή σχεδίαση', [['ψηφιακή', 'σχεδίαση'], ['ψηφιακής', 'σχεδίασης']]),
        Stem('θεωρίες μάθησης', [['θεωρίες', 'μάθησης'], ['θεωριών', 'μάθησης']]),
        Stem('διακριτά μαθηματικά', [['διακριτά', 'μαθηματικά'], ['διακριτών', 'μαθηματικών']]),
        Stem('αγγλικά', [['αγγλικά'], ['αγγλικών']]),
        Stem('καραμπατζάκη', [['καραμπατζάκης'], ['καραμπατζάκη']]),
        Stem('τσινάκο', [['τσινάκος'], ['τσινάκου'], ['τσινάκο']]),
        Stem('λάγκα', [['λάγκας'], ['λάγκα']]),
        Stem('χριστοδουλίδου', [['χριστοδουλίδου']])
]

def normalize(word_list):
    """
    Removes diacritics from words and converts it to a standard form.
    """
    return [unicodedata.normalize('NFD', word).lower().translate({ord('\N{COMBINING ACUTE ACCENT}'): None}) for word in word_list]

def stemmer(token_list):
    stems_list = []
    i = 0
    while i < len(token_list):
        found_stem = False
        for stem in stems:
            tokens = token_list[i:i+len(stem.values[0])]
            for value in stem.values:
                if normalize(value) == normalize(tokens):
                    stems_list.append(stem.name)
                    found_stem = True
                    i += len(tokens)
        if not found_stem:
            stems_list.append(token_list[i])
            i += 1
    return stems_list

def parser(token_list):
    classes = {x[0] for x in knowledge}
    professors = {x[1] for x in knowledge}
    days = {'δευτέρα', 'τρίτη', 'τετάρτη', 'πέμπτη', 'παρασκευή'}

    answers = []
    contains_day = False
    for day in days:
        if day in token_list:
            answers += [x for x in knowledge if x[2] == day]
            contains_day = True
    if not contains_day:
        answers = knowledge

    contains_class = False
    for clas in classes:
        if clas in token_list:
            answers = [x for x in answers if x[0] == clas]
            contains_class = True

    contains_professor = False
    for professor in professors:
        if professor in token_list:
            answers = [x for x in answers if x[1] == professor]
            contains_professor = True

    if contains_day or contains_class or contains_professor:
        return answers

    return []

def respond(answers):
    days = ['δευτέρα', 'τρίτη', 'τετάρτη', 'πέμπτη', 'παρασκευή']
    responses = []
    for day in days:
        classes = [x for x in answers if x[2] == day]
        if len(classes) > 0:
            class_responses = ["%s με %s στις %s:00" % (x[0], x[1].capitalize(), x[3]) for x in classes]
            responses.append("την %s έχουμε " % (day.capitalize()) + and_join(class_responses))
    response = and_join(responses)
    return response[0].upper() + response[1:]

def answer(question):
    return respond(parser(stemmer(tokenizer(question))))
