import random
import time
from textwrap import wrap
from MorseAlphabet import *
from PolluxInputData import *
import ngram
import math

ns = ngram.Ngram_score("english_bigrams.txt")

attackOutput = set()


def generateKey(length):
    dotArray = []
    dashArray = []
    spaceArray = []
    key = {}
    morseCodeSingn = ['.', '-', ' ']

    digits = int(math.log10(length)) + 1
    addToKey = pow(10, digits - 1)

    for i in range(length):
        drawnCharacter = random.choice(morseCodeSingn)
        if drawnCharacter == '.': dotArray.append(i + addToKey)
        elif drawnCharacter == '-': dashArray.append(i + addToKey)
        elif drawnCharacter == ' ': spaceArray.append(i + addToKey)
        key[i + addToKey] = drawnCharacter
        if len(dotArray) == length / 3 and '.' in morseCodeSingn: morseCodeSingn.remove('.')
        if len(dashArray) == length / 3 and '-' in morseCodeSingn: morseCodeSingn.remove('-')
        if len(spaceArray) == length / 3 and ' ' in morseCodeSingn: morseCodeSingn.remove(' ')

    return key, dotArray, dashArray, spaceArray

def encrypt(textToEncrypt, dotKeyArray, dashKeyArray, spaceKeyArray):
    encryptedText = ''

    for letter in textToEncrypt:
        if letter == '.':
            encryptedText += str(dotKeyArray[random.randint(0, len(dotKeyArray) - 1)])
        elif letter == '-':
            encryptedText += str(dashKeyArray[random.randint(0, len(dashKeyArray) - 1)])
        elif letter == ' ':
            encryptedText += str(spaceKeyArray[random.randint(0, len(spaceKeyArray) - 1)])

    return encryptedText


def decrypt(textToDecrypt, key_length, key):
    decryptedText = ''
    dividedEncryptedText = wrap(textToDecrypt, key_length)
    for digit in dividedEncryptedText:
        decryptedText += key.get(int(digit))
    return decryptedText


def numberOfNumbersInAGivenNumericalRange(howManyDigitsIsTheNumber):
    start = pow(10, howManyDigitsIsTheNumber - 1)
    end = start * 10
    return len(range(start, end, 1))


def twist(key0):
    keyTmp = dict(key0)
    randomKey = random.choice(list(keyTmp.keys()))
    morseSing = ['.', '-', ' ']
    sign = keyTmp.get(randomKey)
    morseSing.remove(sign)
    oldSign = keyTmp[randomKey]
    newSign = random.choice(morseSing)
    keyTmp[randomKey] = newSign
    replace = list(keyTmp.keys())[list(keyTmp.values()).index(newSign)]
    keyTmp[replace] = oldSign
    return keyTmp


def changeKey0(key):
    return (twist(key))  # zamiana pojedynczego elementu klucza


# podstawowa wspinaczka (HillClimbing)
def solvePollux(kt, howManyDigitsIsTheKey, czas=5, tValue=time.time()):
    tj = None
    while (tj == None) or ' ' in tj.rstrip():
        key, dotArray, dashArray, spaceArray = generateKey(numberOfNumbersInAGivenNumericalRange(howManyDigitsIsTheKey))
        newKey = oldKey = key
        tj = morseDecrypt(decrypt(kt, howManyDigitsIsTheKey, oldKey))

    newValue = oldValue = ns.score(tj)
    j = 0
    t0 = tValue
    while time.time() - t0 < czas:
        newKey = changeKey0(oldKey)
        tj = morseDecrypt(decrypt(kt, howManyDigitsIsTheKey, newKey))
        while tj == None or ' ' in tj.rstrip():
            newKey = changeKey0(oldKey)
            tj = morseDecrypt(decrypt(kt, howManyDigitsIsTheKey, newKey))
        newValue = ns.score(tj)
        if newValue > oldValue:
            print(oldValue, end='\t')
            print(oldKey)
            oldKey, oldValue = newKey, newValue
        else:
            j += 1
        if (j > 500):
            tj = morseDecrypt(decrypt(kt, howManyDigitsIsTheKey, oldKey))
            print('Długi brak ulepszeń klucza. Znaleziony tekst: ' + tj)
            print('ns.score (atak): ' + str(ns.score(tj)))
            print('Ponownienie metody ataku\n\n')
            attackOutput.add(tj)
            return solvePollux(kt, howManyDigitsIsTheKey, czas, t0)

    print('spent time = ', time.time() - t0, ' sec ')
    return oldKey


# input program data (from PolluxInputData.py)
tekst_pocz = TEXT_TO_ENCRYPT
howManyDigitsIsTheKey = NUMBER_OF_HOW_MANY_DIGIT_IS_IN_THE_KEY
attackTime = ATTACK_TIME

tekst_pocz = tekst_pocz.replace('\n', '').replace('\t', '').replace('\r', '')
tekst_pocz = tekst_pocz.replace(' ', '').replace('.', '').replace(',', '')
tekst_pocz = tekst_pocz.upper()

print('TEKST POCZĄTKOWY: ' + tekst_pocz)
tekst_pocz = morseEncrypt(tekst_pocz)
print('TEKST POCZĄTKOWY (MORSE): ' + tekst_pocz)

key0, dotArray, dashArray, spaceArray = generateKey(numberOfNumbersInAGivenNumericalRange(howManyDigitsIsTheKey))
kt = encrypt(tekst_pocz, dotArray, dashArray, spaceArray)
print('\nKLUCZ: ' + str(key0))
print('ZASZYFROWANY TEKST: ' + str(kt))

tj = decrypt(kt, howManyDigitsIsTheKey, key0)
tj = morseDecrypt(tj)
print('\nODSZYFROWANY TEKST: ' + str(tj))
print("ns.score(odszyfrowany tekst) = ", ns.score(tj))

print('\nATAK')
solution = solvePollux(kt, howManyDigitsIsTheKey, attackTime)
print(str(solution))
tj = morseDecrypt(decrypt(kt, howManyDigitsIsTheKey, solution))
print('TEKST (atak): ' + tj)
print('ns.score (atak): ' + str(ns.score(tj)))
attackOutput.add(tj)
sourceFile = open('pollux_atak_wyniki.txt', 'w')
print("\n".join(attackOutput), file=sourceFile)
sourceFile.close()
