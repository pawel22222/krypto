import random
import time
import ngram

ns = ngram.Ngram_score("english_bigrams.txt")

alf = ''.join( chr(97+i) for i in range(26) )
# print(alf)

def generateKey(alf):
    return( ''.join( random.sample(alf,26) ) )

key0 = generateKey(alf)

# print( key0 )

tekst_pocz = '''Congressional leaders in the US reached a bipartisan deal early this morning to provide $13.6bn to help Ukraine and European allies, reports the Associated Press.
President Joe Biden originally requested $10bn for military, humanitarian and economic aid, but the backing from both parties was so strong that the figure climbed to $12bn on Monday and $13.6bn yesterday.
“We’re going to support them against tyranny, oppression, violent acts of subjugation,” Biden said at the White House.
Party leaders are hoping to get the 2,741-page measure through the House today and the Senate by the end of the week, but the timing of the latter remains unclear.'''

# tekst_pocz = 'TE'

tekst_pocz = tekst_pocz.replace('\n','').replace('\t','').replace('\r','')
tekst_pocz = tekst_pocz.replace(' ','').replace('.','').replace(',','')
tekst_pocz = tekst_pocz.replace('!','').replace('?','').replace(';','')
tekst_pocz = tekst_pocz.lower()

tekst_pocz = ''.join( c if c in alf else '' for c in tekst_pocz )

# print(tekst_pocz)

def szyfrSubst2(tj, key):
    dc = {}
    for i in range(len(alf)):
        dc[ alf[i] ] = i
    kt = ''
    for c in tj:
        kt += key[ dc[c] ]
    return( kt )

def deszyfrSubst2(kt, key):
    dc = {}
    for i in range(len(key)):
        dc[ key[i] ] = i
    tj = ''
    for c in kt:
        tj += alf[ dc[c] ]
    return( tj )

def changeKey0( key ):
    r1, r2 = sorted( random.sample( range(26), 2 ) )
    keytmp = list(key)
    #print(' r1= ', r1, '   r2=',r2)
    keytmp[r1], keytmp[r2] = key[r2], key[r1]
    # print('Cgange key' + ''.join(keytmp))
    return ''.join(keytmp)

# podstawowa wspinaczka (HillClimbing)
def solveSubst1( kt, czas = 10 ):
    newKey = oldKey = generateKey(alf)  #
    newValue = oldValue = ns.score( deszyfrSubst2( kt, oldKey) )

    t0 = time.time()
    while time.time() - t0 < czas:
        newKey = changeKey0(oldKey)     #
        newValue = ns.score( deszyfrSubst2( kt, newKey) )
        if newValue > oldValue:
            print(oldValue,end='\t' )
            oldKey, oldValue = newKey, newValue
    print( 'spent time = ', time.time()-t0,' sec ' )
    return oldKey


kt = szyfrSubst2( tekst_pocz,key0 )
print( "ns.score(kt) = ",  ns.score(kt) )
print( '\n' + kt )
tj = deszyfrSubst2( kt, key0 )
print( "ns.score(tj) = ",  ns.score(tj) )
print( '\n' + tj )



solution = solveSubst1( kt )
tj = deszyfrSubst2( kt, solution )
print(  '\n' +str( ns.score( tj)) + '\n' + tj )


