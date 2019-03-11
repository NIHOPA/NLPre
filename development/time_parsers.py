import nlpre
import timeit
import pandas as pd

doc2 = open("../tests/doc2").read()

keys = [
    'decaps_text',
    'dedash',
    'unidecoder',
    'identify_parenthetical_phrases',
    'pos_tokenizer',
    'replace_acronyms',
    'separated_parenthesis',
    'titlecaps',
    'token_replacement',
    'replace_from_dictionary',
]


POS_Blacklist = ["connector","cardinal",
                 "pronoun","adverb",
                 "symbol","verb",
                 "punctuation",]

ABR = nlpre.identify_parenthetical_phrases()(doc2)
key0 = (('systemic', 'lupus', 'erythematosus'), 'SLE')
for n in range(50000):
    ABR[(key0[0],key0[1]+str(n))] += 1

n = 50
data=[]
for key in keys:
    if key =='pos_tokenizer':
        parser = nlpre.pos_tokenizer(POS_Blacklist)
    elif key == "replace_acronyms":
        parser = nlpre.replace_acronyms(ABR)
    else:
        parser = getattr(nlpre, key)()

    if key=='unidecoder':
        func = lambda : [parser(x) for x in [doc2]]
    else:
        func = lambda : [parser(x) for x in [doc2]]
    cost = timeit.timeit(func, number=n) / n
    item = {'function':key, "time":cost}
    print (item)
    data.append(item)
df = pd.DataFrame(data)
df = df.set_index('function').sort_values('time')
df["frac"] = df.time / df.time.sum()

print (df)



