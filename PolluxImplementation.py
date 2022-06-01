import random

from MorseAlphabet import *
from PolluxAttack import pollux_attack
from PolluxInputData import *


def polluxEncrypt(textToEncrypt, morseSignAsNumber):
    encryptedText = ''
    dotSignNumberArray, dashSignNumberArray, spaceSignNumberArray = collapseMorseSingAsNumberToArray(morseSignAsNumber)
    dotSignNumberArrayLength = len(dotSignNumberArray) - 1
    dashSignNumberArrayLength = len(dashSignNumberArray) - 1
    spaceSignNumberArrayLength = len(spaceSignNumberArray) - 1

    for letter in textToEncrypt:
        if letter == '.':
            encryptedText += str(dotSignNumberArray[random.randint(0, dotSignNumberArrayLength)])
        elif letter == '-':
            encryptedText += str(dashSignNumberArray[random.randint(0, dashSignNumberArrayLength)])
        elif letter == ' ':
            encryptedText += str(spaceSignNumberArray[random.randint(0, spaceSignNumberArrayLength)])

    return encryptedText


def polluxDecrypt(textToDecrypt, morseSignAsNumber):
    decryptedText = ''
    for digit in textToDecrypt:
        decryptedText += morseSignAsNumber.get(int(digit))
    return decryptedText


def collapseMorseSingAsNumberToArray(morseSignAsNumber):
    dotSignNumberArray = []
    dashSignNumberArray = []
    spaceSignNumberArray = []
    for key in morseSignAsNumber:
        if morseSignAsNumber.get(key) == '.':
            dotSignNumberArray.append(key)
        elif morseSignAsNumber.get(key) == '-':
            dashSignNumberArray.append(key)
        elif morseSignAsNumber.get(key) == ' ':
            spaceSignNumberArray.append(key)
        else:
            raise ValueError('Wrong data provided')

    if len(dotSignNumberArray) == 0 or len(dashSignNumberArray) == 0 or len(spaceSignNumberArray) == 0:
        raise ValueError('Wrong data provided')

    return dotSignNumberArray, dashSignNumberArray, spaceSignNumberArray


# Executes the main function
if __name__ == '__main__':
    # input program data (from PolluxInputData.py)
    textToEncrypt = TEXT_TO_ENCRYPT
    morseSignAsDigit = MORSE_SIGN_AS_DIGIT
    dictLanguage = DICT_LANGUAGE_TO_DECRYPT
    # end Input data

    # pollux algorithm
    textToEncryptInMorseAlphabet = morseEncrypt(textToEncrypt.upper())
    encryptedText = polluxEncrypt(textToEncryptInMorseAlphabet, morseSignAsDigit)
    decryptedTextInMorseAlphabet = polluxDecrypt(encryptedText, morseSignAsDigit)
    decryptedText = morseDecrypt(decryptedTextInMorseAlphabet)
    print('Szyfr Polux')
    print('Podano tekst: ' + textToEncrypt)
    print('Tekst zakodowany w alfabecie Morsa: ' + textToEncryptInMorseAlphabet)
    print('Zaszyforwany tekst: ' + encryptedText)
    print('Odszyfrowany teskt w alfabecie Morsa: ' + decryptedTextInMorseAlphabet)
    print('Odszyfrowany tekst: ' + decryptedText)
    print('Start ataku na szyfr Pollux')
    pollux_attack(encryptedText, dictLanguage)
    print('Zakończono atak na szyfr Pollux - wyniki w plikach: polux_atak_wszystko.txt oraz polux_atak_filtrowanie_slownikowe.txt')
