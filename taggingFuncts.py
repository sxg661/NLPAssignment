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
import FileWritingFuncts
import SentenceTaggingFuncts
import TimeFunct



def get_named_entities(sent):
    print(sent)
    train_sents = brown.tagged_sents()[:1000]
    print("here1")
    emma_taggery = NamedEntityFindingFuncts.backoff_tagger(train_sents, [UnigramTagger,BigramTagger, TrigramTagger])
    name_taggery = NamedEntityFindingFuncts.NamesTagger(emma_taggery)

    print("here2")
    
    strict_entities = set(NamedEntityFindingFuncts.get_ne_strict_grammar(sent,name_taggery))

    print("here3")
    broad_entities = set(NamedEntityFindingFuncts.get_ne_broad_grammar(sent,name_taggery)).difference(strict_entities)

    print("here4")

    return strict_entities, broad_entities


#REMOVE THIS WHEN DONE TESTING
def test_tagger(sent):
    sent = TweetTokenizer().tokenize(sent)
    train_sents = brown.tagged_sents()[:1000]
    emma_taggery = NamedEntityFindingFuncts.backoff_tagger(train_sents, [UnigramTagger,BigramTagger, TrigramTagger])
    name_taggery = NamedEntityFindingFuncts.NamesTagger(emma_taggery)

    

    
    
    return name_taggery.tag(sent)

    





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

    #classified_entities = remove_sub_strings(classified_entities)


    sent = tag_entities(sent, classified_entities)

    return sent



def tag_all_entities(data):
    tokenizer = nltk.data.load('tokenizers/punkt/PY3/english.pickle')
    tokens = tokenizer.tokenize(data)
    tagged_tokens = []
    for token in tokens:
        tagged_tokens.append(tag_named_entities(token))
    return tokens,tagged_tokens

def get_in_dict(entities, tag_name):
    entities_dict = {}
    for entity in entities:
        entities_dict[entity] = tag_name
    return entities_dict
    
def tag_files():
    path = "untagged/"
    tokenizer = nltk.data.load('tokenizers/punkt/PY3/english.pickle')
    files = FileReadingFuncts.get_files(path)
    for file in files[36:]:
        data = FileReadingFuncts.read_file(path,file)

        #tags the times
        entities_to_tag = TimeFunct.get_end_time_examples(data)
        data = tag_entities(data, entities_to_tag)
        
        #tags the named entitites
        data = tag_named_entities(data)
        
        #tags the sentences
        sentences = SentenceTaggingFuncts.get_sentences(data)
        entities_to_tag = get_in_dict(sentences,"sentence")
        data = tag_entities(data, entities_to_tag)

        
        #tags the paragraphs
        paragraphs = SentenceTaggingFuncts.get_paragraphs(data)
        entities_to_tag = get_in_dict(paragraphs,"paragraph")
        data = tag_entities(data, entities_to_tag)

        FileWritingFuncts.writeTaggedFile(data,file)


    
    
    


