'''
Silly joke, "gerp", greps for spelling errors due to transpostoin mistakes.
Basically just a subset of the functionality Norvig explains in:
http://norvig.com/spell-correct.html
'''
import re, collections
import sys

def words(text): return re.findall('[a-z]+', text.lower())

def train(features):
    model = collections.defaultdict(lambda: 1)
    for f in features:
        model[f] += 1
    return model

NWORDS = train(words(file('big.txt').read()))

alphabet = 'abcdefghijklmnopqrstuvwxyz'

def edits1(word):
    splits     = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    #deletes    = [a + b[1:] for a, b in splits if b]                      #we
    transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b)>1]
    #replaces   = [a + c + b[1:] for a, b in splits for c in alphabet if b]#wont
    #inserts    = [a + c + b     for a, b in splits for c in alphabet]     #need
    #return set(deletes + transposes + replaces + inserts)                 #these!
    return set(transposes)


def known_edits2(word):
    return set(e2 for e1 in edits1(word) for e2 in edits1(e1) if e2 in NWORDS)

def known(words): return set(w for w in words if w in NWORDS)

def correct(word):
    ''' Tries to correct word'''
    candidates = known([word]) or known(edits1(word)) or known_edits2(word) or [word]
    corrected = max(candidates, key=NWORDS.get)
    if corrected != word:
        return highlight_errors(word,corrected)
    return corrected


def highlight_errors(word,corrected):
    '''Makes the modified characters uppercase '''
    highlighted = []
    for original,new in zip(word,corrected):
        if original != new:
            highlighted.append(new.upper())
        else:
            highlighted.append(new)
    return ''.join(highlighted)

def porcess_line(line,num=''):

    ws = line.lower().split()
    corrected = [correct(w) for w in ws]
    if ws != corrected:
        print '%s:%s'% (num,' '.join(corrected))

if __name__ == '__main__':
    with open(sys.argv[1]) as f:
        lines = f.readlines()
        num_width = len(str(len(lines)))#huh

        for i,line in enumerate(lines):
            porcess_line(line,str(i).zfill(num_width))
