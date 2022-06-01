from itertools import product
from MorseAlphabet import *
import enchant


def pollux_attack(polluxEncryptedText, dict_language):
    output = set()
    outputDictionaryFilter = set()

    for combo in product(['.', '-', ' '], repeat=10):
        if '.' not in str(combo) or '-' not in str(combo) or ' ' not in str(combo):
            continue
        outputTextInMorse = ""
        for c in polluxEncryptedText:
            outputTextInMorse += combo[int(c)]
        decryptedTextInMorseAlphabet = morseDecrypt(outputTextInMorse)
        if decryptedTextInMorseAlphabet is not None:
            if ' ' not in decryptedTextInMorseAlphabet.rstrip(): output.add(decryptedTextInMorseAlphabet)
    sourceFile = open('polux_atak_wszystko.txt', 'w')
    print("\n".join(output), file=sourceFile)
    sourceFile.close()
    d = enchant.Dict(dict_language)
    for text in output:
        if d.check(text.strip()): outputDictionaryFilter.add(text)
    sourceFile = open('polux_atak_filtrowanie_slownikowe.txt', 'w')
    print("\n".join(outputDictionaryFilter), file=sourceFile)
    sourceFile.close()
