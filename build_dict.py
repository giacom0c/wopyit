MAX_LENGHT = 6 # 5 +1 for newline char (\n)
FORBIDDEN_CHARS = [
    'à', 'è', 'é', 'ì', 'ò', 'ù',
    '-', ' ', '.', ',', '\''
    '1', '2', '3', '4', '5', '6', '7' '8', '9', '0'
]

with open('dict/60000_parole_italiane.txt', 'r') as input:
    for line in input:
        if len(line) == MAX_LENGHT:
            for letter in line:
                if letter in FORBIDDEN_CHARS:
                    continue
            with open('dict/custom_dictionary.txt', 'a') as output:
                output.write(line)
