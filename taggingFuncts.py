import re
import os
import sys
import nltk
import nltk.data

from nltk.tag           import SequentialBackoffTagger
from nltk.corpus        import names
from nltk.corpus        import treebank
from nltk.corpus        import brown
from nltk.tag           import DefaultTagger
from nltk.tag           import UnigramTagger
from nltk.tag           import BigramTagger
from nltk.tag           import TrigramTagger
from nltk.chunk.regexp  import *
from nltk.corpus.reader import WordListCorpusReader
from nltk.tokenize      import sent_tokenize
from nltk.tokenize      import TweetTokenizer
from os                 import listdir
from os.path            import isfile, join

import NamedEntityFindingFuncts
import ClassificationFuncts



def get_named_entities(sent):
    train_sents = brown.tagged_sents()[:1000]
    emma_taggery = NamedEntityFindingFuncts.backoff_tagger(train_sents, [UnigramTagger,BigramTagger, TrigramTagger])
    name_taggery = NamedEntityFindingFuncts.NamesTagger(emma_taggery)
    
    strict_entities = set(NamedEntityFindingFuncts.get_ne_strict_grammar(sent,name_taggery))
    broad_entities = set(NamedEntityFindingFuncts.get_ne_broad_grammar(sent,name_taggery)).difference(strict_entities)

    return strict_entities, broad_entities



    

    


def classify(entitiy, strict):
    tag_names = ["speaker","location"]
    vocabs, tag_occurances = ClassificationFuncts.build_training_vocabs(tag_names)
    best_match, second_match = ClassificationFuncts.classify(entity, vocabs, tag_occurances, tag_names)
   
    if strict:
        return best_match.get_tag_name()
    else:
        if abs(best_match.get_sumProb - second_match.get_sumProb) > 30:
            return best_match.get_tag_name()
        else: return None
        
    return "name"





def tag_named_entities(sent, named_entities):
    for entity in named_entities:
        entity_type = classify(entity)
        if entity_type != "undefined":
            tag = "<{}>".format(entity_type)
            sent= sent.replace(entity, "{}{}{}".format(tag,entity,tag))
    return sent
              
           
        
        
        

def main():
    path = "untagged/"
    tokenizer = nltk.data.load('tokenizers/punkt/PY3/english.pickle')
    for file in get_files(path):
        data = read_file(path,file)
        dataTokens= tokenizer.tokenize(data)
        print(dataTokens)

    
    
    


