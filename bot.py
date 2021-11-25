knowledge = [
        ('ψηφιακή σχεδίαση', 'καραμπατζάκη', 'δευτέρα', 16, 20),
        ('θεωρίες μάθησης', 'τσινάκο', 'τρίτη', 13, 15)
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
        Stem('ψηφιακή σχεδίαση', [['ψηφιακή', 'σχεδίαση'], ['ψηφιακής', 'σχεδίασης']]),
        Stem('θεωρίες μάθησης', [['θεωρίες', 'μάθησης'], ['θεωριών', 'μάθησης']]),
        Stem('καραμπατζάκη', [['καραμπατζάκης'], ['καραμπατζάκη']]),
        Stem('τσινάκο', [['τσινάκος'], ['τσινάκου'], ['τσινάκο']]),
]

def stemmer(token_list):
    stems_list = []
    i = 0
    while i < len(token_list):
        found_stem = False
        for stem in stems:
            tokens = token_list[i:i+len(stem.values[0])]
            for value in stem.values:
                if value == tokens:
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
    days = {'δευτέρα', 'τρίτη'}

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
    days = ['δευτέρα', 'τρίτη']
    responses = []
    for day in days:
        classes = [x for x in answers if x[2] == day]
        if len(classes) > 0:
            class_responses = ["%s με %s στις %s" % (x[0], x[1], x[3]) for x in classes]
            responses.append("την %s έχουμε " %day + and_join(class_responses))
    return and_join(responses)

while True:
    sentence = input('> ')
    print(respond(parser(stemmer(tokenizer(sentence)))))
