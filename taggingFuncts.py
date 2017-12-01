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
import SentenceTaggingFuncts



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

#tag_named_entities("Hi there I am Dr. Mark Lee, I am going down to Hamburg Hall 909A now for a lecture")
           
def tag_named_entities(sent):
    #goes through the sentence and finds everything that definitely is a named entitiy (strict)
    #and stuff that is less likely to be, but could be (broad)
    strict_entities,broad_entities = get_named_entities(sent)

    print(strict_entities)
    print(broad_entities)

    #MOVE THESE 2 LINES TO THE ACTUAL MAIN FUNCTION ONCE YOU'VE MADE IT!!!
    tag_names = ["speaker","location"]
    vocabs, tag_occurances = ClassificationFuncts.build_training_vocabs(tag_names)


    #reads in the example files created from the training data for the locations and the speakers
    examples = {}
    for tag_name in tag_names:
        examples[tag_name] = get_examples(tag_name)
    
    classified_entities = {}

    entities = [strict_entities, broad_entities]

    #classifies and tags each entitiy
    for i in range(0,len(entities)):

        for entity in entities[i]:

            #before doing bayes we can check if this is an entitiy that came up in the training data
            #by looking at the examples we rede in a little bit
            ent_type = ClassificationFuncts.classify__files(entity, tag_names, examples)

            # if we get a match from this we can automatically classify the entity
            if ent_type != None:
                classified_entities[entity] = ent_type
            # if not we can use our bayes classifier
            else:
                
                #(the bayes classifier will have a cutoff if the entitiy was not found using the strict grammar)
                strict = True;
                if i == 1:
                    strict = False

                
                ent_type = ClassificationFuncts.classify__bayes(entity, strict, tag_names, vocabs, tag_occurances)

                #if the entity is classified we give it this tag, overwise at this point we just throw it in the trash
                if ent_type != None:
                    classified_entities[entity] = ent_type

    classified_entities = remove_sub_strings(classified_entities)


    sent = tag_entities(sent, classified_entities)

    return sent
            

def get_in_dict(entities, tag_name):
    entities_dict = {}
    for entity in entities:
        entities_dict[entity] = tag_name
    return entities_dict
    
def main():
    path = "untagged/"
    tokenizer = nltk.data.load('tokenizers/punkt/PY3/english.pickle')
    FileReadingFuncts.get_files(path)
    for file in ["350.txt"]:
        data = FileReadingFuncts.read_file(path,file)
        #print(data)
        sentences = SentenceTaggingFuncts.get_sentences(data)

        #tags the sentences
        entities_to_tag = get_in_dict(sentences,"sentence")
        data = tag_entities(data, entities_to_tag)
        
        paragraphs = SentenceTaggingFuncts.get_paragraphs(data)

        #tags the paragraphs
        entities_to_tag = get_in_dict(paragraphs,"paragraph")
        data = tag_entities(data, entities_to_tag)

        
        print(data)

    
    
    


