from dataclasses import replace
from googletrans import Translator, LANGUAGES
from random import choice
from random import sample
from multiprocessing import Pool
from time import time

def load_synonyms(path): 
    syn = {}
    with open(path, 'r') as f:
        line = f.readline()
        while line:
            if line[-1] == "\n": line = line[:-1]
            line = line.lower().split(" <=> ")
            line[1] = line[1].split(", ")
            syn[line[0]] = line[1]
            line = f.readline()
    return syn

syn = load_synonyms("synonyms.txt")

def synonym_replace(word_list):
    replace_list = []
    for index, word in enumerate(word_list):
        if word in syn:
            a = synonym_replace(word_list[index+1:])
            for x in a:
                replace_list.append(word_list[:index] + [word] + x)
                for y in syn[word]:
                    replace_list.append(word_list[:index] + [y] + x) 
            return replace_list
    replace_list.append(word_list)
    return replace_list

def translate(text):
    lang = choice(list(LANGUAGES))
    translator = Translator()
    intermediary = translator.translate(text, src="en", dest=lang)
    result = translator.translate(intermediary.text, src=lang, dest="en")
    return result.text

#b = synonym_replace(["come", "and", "go"])
#for x in b: print(x)
#print(len(b))

def generate_mutations(prompt, max_number):
    start = time()
    mutations = synonym_replace(prompt.split(" "))
    result = [" ".join(x) for x in mutations]
    result = sample(result, min(len(result), max_number))
    lr = len(result)
    while len(result) < max_number:
        result.append(result[-lr])

    with Pool(max_number) as p:
        result = p.map(translate, result)

    print(f"{time()-start}s")
    return result
