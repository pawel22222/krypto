MORSE_CODE_DICT = {'A': '.-', 'B': '-...',
                   'C': '-.-.', 'D': '-..', 'E': '.',
                   'F': '..-.', 'G': '--.', 'H': '....',
                   'I': '..', 'J': '.---', 'K': '-.-',
                   'L': '.-..', 'M': '--', 'N': '-.',
                   'O': '---', 'P': '.--.', 'Q': '--.-',
                   'R': '.-.', 'S': '...', 'T': '-',
                   'U': '..-', 'V': '...-', 'W': '.--',
                   'X': '-..-', 'Y': '-.--', 'Z': '--..',
                   '1': '.----', '2': '..---', '3': '...--',
                   '4': '....-', '5': '.....', '6': '-....',
                   '7': '--...', '8': '---..', '9': '----.',
                   '0': '-----', ', ': '--..--', '.': '.-.-.-',
                   '?': '..--..', '/': '-..-.', '-': '-....-',
                   '(': '-.--.', ')': '-.--.-'}


def morseEncrypt(textToEncrypt):
    encryptedText = ''
    for letter in textToEncrypt:
        if letter != ' ':
            encryptedText += MORSE_CODE_DICT[letter] + ' '
        else:
            encryptedText += ' '
    return encryptedText


def morseDecrypt(message, morseSignAsNumber=MORSE_CODE_DICT):
    message += ' '
    decipher = ''
    citext = ''
    for letter in message:
        if letter != ' ':
            i = 0
            citext += letter
        else:
            try:
                i += 1
            except UnboundLocalError:
                return None
            if i == 2:
                decipher += ' '
            else:
                try:
                    decipher += list(morseSignAsNumber.keys())[list(morseSignAsNumber.values()).index(citext)]
                except ValueError:
                    return None
                citext = ''
    return decipher
