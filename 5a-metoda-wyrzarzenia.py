text = " Data Repository is free-to-use and open access. It enables you to deposit any research data (including raw and processed data, video, code, software, algorithms, protocols, and methods) associated with your research manuscript. Your datasets will also be searchable on Mendeley Data Search, which includes nearly 11 million indexed datasets. For more information, visit ."

import string
import random
import time
import math
from ngram import Ngram_score

alfabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
ns = Ngram_score("english_bigrams.txt")


def encrypt(M,key):
    dic = {}
    for i in range(len(alfabet)):
        dic[alfabet[i]] = key[i]

    C = ""
    for c in M:
        C += dic[c]
    return (C)


def inverseKey(key):
    lista = [[key[i], alfabet[i]] for i in range(len(alfabet))]
    lista.sort()
    return "".join([lista[i][1] for i in range(len(alfabet))])

def inverseKey2(key):
    dic = {}
    for i in range(len(alfabet)):
        dic[key[i]] = alfabet[i]
    invKey = ""
    for c in list(alfabet):
        invKey += dic[c]
    return (invKey)

def twist2(key):
    r = random.sample(list(range(26)), 2)
    r.sort()
    r1 = r[0]
    r2 = r[1]
    newKey = key[:r1] + key[r2] + key[r1+1:r2] + key[r1] + key[r2+1:]
    return newKey

def shift(key):
    r = random.choice(list(range(26)))
    return key[r:] + key[:r]

def twist3(key):
    r = random.sample(list(range(26)), 3)
    r.sort()
    r1 = r[0]
    r2 = r[1]
    r3 = r[2]
    newKey = key[:r1] + key[r3] + key[r1+1:r2] + key[r1] + key[r2+1:r3] + key[r2] + key[r3+1:]
    return newKey

def reverse(key):
    #r = random.sample(list(range(26)), 3)
    nk =list(key)
    nk.reverse()
    return("".join(nk))

import time
import statistics

def AcceptanceFunction(valueOld, valueNew, temp):
    if random.random() < math.exp((valueNew-valueOld)/temp):
        return True
    else:
        return False

def changeKey(key):
    r = random.random()
    if r < 0.9:
        return ( twist2(key) ) #zamiana 2 liter miejscami
    elif r < 0.94:
        return ( shift(key) ) #przesunięcie klucza o kilka pozycji w stronę
    elif r < 0.98:
        return ( twist3(key) ) #zamiana 3 liter miejscami
    else:
        return( reverse(key) ) #odwrócenie kolejności liter w kluczu

def KeySimilarity(key1,key2):
    d = 0
    for i in range(len(key1)):
        if key1[i] == key2[i]:
            d += 1
    return d

# wariant 'zamrażania' (Simulated Annealing Algorithm) dla metody 'wspinania się':
# kiedy zmieniając klucz, otrzymujemy gorszy wynik, my nie odrzucamy jego,
# ale wywołujemy funkcje AcceptanceFunction, która z niektórym niezerowym prawdopodobieństwem
# (im wyższym, czym wyższa temperatura) zgadza się na pogorszenie wyniku
# z celą unikać problemu lokalnych maksimum
#
# Dla szyfru zamiany działa co najmniej kilkakrotnie wolniej, a niż zwykle wspinanie się.
# Ale dla innych szyfrów (dla których tych lokalnych maksimumów jest bardzo dużo) może dać
# lepszy wynik.
# Też tej metody można używać dla otrzymania początkowych approksymacji, które póżniej
# próbuje się ulepszyć inną metodą.
#
# Tutaj mamy wersje hibrydową - na nastepnych krokach my raczej spróbujemy ulepszyć
# jeden z dobrych już odnalezionych kluczy (80% bierzemy jeden z lepszej połowy już odnalezionych),
# a niż będziemy losować od nowa (20%).

# symulowanego wyżarzenia (simulated annealing)
def AnnealingHC_podstawowy(ct):
    t1 = time.time()
    starttemp = 100
    endtemp = 0.5
    temp = starttemp
    tempDelta = -0.01

    keyMax = keyOld = "".join(random.sample(list(alfabet), len(alfabet)))
    scoreMax = scoreOld = ns.score(encrypt(ct, keyOld))

    while temp >= endtemp:
        keyNew = changeKey(keyOld)
        scoreNew = ns.score(encrypt(ct, keyNew))
        if scoreNew > scoreOld:
            keyOld = keyNew
            scoreOld = scoreNew
            if scoreOld > scoreMax:
                scoreMax, keyMax = scoreOld, keyOld
                print(scoreMax, keyMax)
        elif AcceptanceFunction(scoreOld,scoreNew,temp):
            keyOld = keyNew
            scoreOld = scoreNew
        temp += tempDelta

    print('zatracono ', time.time()-t1, ' sekund')
    return [scoreMax, keyMax, encrypt(ct, keyOld)]




#text = " Data Repository is free-to-use and open access. It enables you to deposit any research data (including raw and processed data, video, code, software, algorithms, protocols, and methods) associated with your research manuscript. Your datasets will also be searchable on Mendeley Data Search, which includes nearly 11 million indexed datasets. For more information, visit ."
#text = "Both sides discovered that their initial strategies did not work. The Romans were shocked by a series of disastrous military defeats and faced the greatest challenge in Roman history. Hannibal achieved his initial goals, getting his army over the Alps and winning a series of dramatic victories, still studied today by ambitious young military officers all over the world. But his strategy failed. Even after his overwhelming victory at Cannae, only a handful of Italian city states went over to his side. Roman power survived, and the war dragged on. World War I started out in much the same way. The French and the Germans had both planned what they hoped would be decisive attacks, the French over their eastern border and the Germans with the Schlieffen plan for an attack through Belgium that would capture Paris. Both offensives fell short, leaving the countries locked in a conflict that neither side knew how to win and neither was willing to lose.Something similar seems to be happening with Mr. Putin’s war. The original Russian plan was to break the Ukrainian state by quickly taking the capital and major cities such as Kharkiv. It failed. Ukraine hoped that the shock of military setbacks plus major economic sanctions would either force Mr. Putin to accept peace terms favorable to Ukraine or lead to his overthrow. That plan also seems to have failed, at least for now."
tekst_pocz= '''Congressional leaders in the US reached a bipartisan deal early this morning to provide $13.6bn to help Ukraine and European allies, reports the Associated Press.
President Joe Biden originally requested $10bn for military, humanitarian and economic aid, but the backing from both parties was so strong that the figure climbed to $12bn on Monday and $13.6bn yesterday.
“We’re going to support them against tyranny, oppression, violent acts of subjugation,” Biden said at the White House.
Party leaders are hoping to get the 2,741-page measure through the House today and the Senate by the end of the week, but the timing of the latter remains unclear.'''

#tj = text.upper().replace(" ", "").replace("1", "").replace("(",
 #           "").replace(")", "").replace(".", "").replace(",","").replace("!", "").replace("?",
   #         "").replace("-", "").replace("$","")
tekst_pocz = tekst_pocz.replace('\n','').replace('\t','').replace('\r','')
tekst_pocz = tekst_pocz.replace(' ','').replace('.','').replace(',','')
tekst_pocz = tekst_pocz.replace('!','').replace('?','').replace(';','')
tekst_pocz = tekst_pocz.upper()

tekst_pocz = ''.join( c if c in alfabet else '' for c in tekst_pocz )

tj = text = tekst_pocz
alfabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

klucz = "".join(random.sample(list(alfabet), 26))
print('losowy klucz: ')
print(alfabet)
print(klucz)
print()
print('szukamy odwrócony (dla deszyfrowania) klucz: ', inverseKey2(klucz))
ct = encrypt(tj, klucz)
print(ct)
# UWAGA. Działa WOLNO! Potrzebuje kilka minut dla dobrego wyniku.

print(AnnealingHC_podstawowy(ct))
print(klucz)
