knowledge = [
        ('ψηφιακή σχεδίαση', 'καραμπατζάκης', 1, 16, 20),
        ('θεωρίες μάθησης', 'τσινάκος', 2, 13, 15)
]

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

while True:
    sentence = input('> ')
    print(tokenizer(sentence))
