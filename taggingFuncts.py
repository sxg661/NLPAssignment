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
import FileReadingFuncts



def get_named_entities(sent):
    train_sents = brown.tagged_sents()[:1000]
    emma_taggery = NamedEntityFindingFuncts.backoff_tagger(train_sents, [UnigramTagger,BigramTagger, TrigramTagger])
    name_taggery = NamedEntityFindingFuncts.NamesTagger(emma_taggery)
    
    strict_entities = set(NamedEntityFindingFuncts.get_ne_strict_grammar(sent,name_taggery))
    broad_entities = set(NamedEntityFindingFuncts.get_ne_broad_grammar(sent,name_taggery)).difference(strict_entities)

    return strict_entities, broad_entities


#REMOVE THIS WHEN DONE TESTING
def test_tagger(sent):
    sent = TweetTokenizer().tokenize(sent)
    train_sents = brown.tagged_sents()[:1000]
    emma_taggery = NamedEntityFindingFuncts.backoff_tagger(train_sents, [UnigramTagger,BigramTagger, TrigramTagger])
    name_taggery = NamedEntityFindingFuncts.NamesTagger(emma_taggery)
    
    return name_taggery.tag(sent)

    
def remove_sub_strings(entity_dict):
    #removes an entity if it is a substring of another entity that has been picked up
    new_entity_dict = {}

    entity_keys = entity_dict.keys()
    
    for entity1 in entity_keys:
        sub = False
        for entity2 in entity_keys:
            if entity1 in entity2 and entity1 != entity2:
                sub = True
        if not sub:
            new_entity_dict[entity1] = entity_dict[entity1]

    return new_entity_dict




#MOVE TO CLASSIFY MODULE
def classify__bayes(entity, strict, tag_names, vocabs, tag_occurances):

    best_match, second_match = ClassificationFuncts.classify(entity, vocabs, tag_occurances, tag_names)
   
    if strict:
        return best_match.get_tag_name()
    else:
        if abs(best_match.get_sumProb() - second_match.get_sumProb()) > 20:
            return best_match.get_tag_name()
        else: return None
        
    return "name"

#MOVE TO CLASSIFY MODULE
def classify__files(entity, tag_names, examples):
    for tag_name in tag_names:
        if entity in examples[tag_name]:
            return tag_name
    return None

def get_examples(tag_name):
    file = "tagFiles/{}.txt".format(tag_name)
    examples = FileReadingFuncts.read_all_lines(file)
    return examples


def tag_entities(sent, entities):
    for entity in entities.keys():
        open_tag = "<{}>".format(entities[entity])
        close_tag = "</{}>".format(entities[entity])
        sent= sent.replace(entity, "{}{}{}".format(open_tag,entity,close_tag))
    return sent


           
def tag_named_entities(sent):
    strict_entities,broad_entities = get_named_entities(sent)

    print(strict_entities)
    print(broad_entities)

    #MOVE THESE 2 LINES TO THE ACTUAL MAIN FUNCTION ONCE YOU'VE MADE IT!!!
    tag_names = ["speaker","location"]
    vocabs, tag_occurances = ClassificationFuncts.build_training_vocabs(tag_names)

    examples = {}
    for tag_name in tag_names:
        examples[tag_name] = get_examples(tag_name)
    
    classified_entities = {}
    
    for entity in strict_entities:
        ent_type = classify__files(entity, tag_names, examples)

        if ent_type != None:
            classified_entities[entity] = ent_type
        else:
            ent_type = classify__bayes(entity, True, tag_names, vocabs, tag_occurances)
            classified_entities[entity] = ent_type

    for entity in broad_entities:
        ent_type = classify__files(entity, tag_names, examples)

        if ent_type != None:
            classified_entities[entity] = ent_type
        else:
            ent_type = classify__bayes(entity, False, tag_names, vocabs, tag_occurances)
            if ent_type != None:
                classified_entities[entity] = ent_type

    classifed_entities = remove_sub_strings(classified_entities)

    sent = tag_entities(sent, classified_entities)

    return sent
            
        
def main():
    path = "untagged/"
    tokenizer = nltk.data.load('tokenizers/punkt/PY3/english.pickle')
    for file in get_files(path):
        data = read_file(path,file)
        dataTokens= tokenizer.tokenize(data)
        print(dataTokens)

    
    
    


