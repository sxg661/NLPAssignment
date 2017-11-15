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



class NamesTagger(SequentialBackoffTagger):
    def __init__(self, *args, **kwargs):
        SequentialBackoffTagger.__init__(self, *args, **kwargs)
        self.name_set = set([n.lower() for n in names.words()])

    def choose_tag(self, tokens, index, history) :
        word = tokens[index]

        if word.lower() in self.name_set:
            return 'NNP'
        else :
            return None



# My function to clear screen - I want it to work on all Operating Systems.
def cls(): print ("\n" * 50)

#gets the idividual path of all the files
def get_files(path):
    files = [f for f in listdir(path) if isfile(join(path, f))]
    try :
        del( files[files.index( '.DS_Store' )] )
    except :
        pass
    return files

def read_file(path, file):
    file_handle = open( join(path, file), 'r' )
    data = file_handle.read()
    file_handle.close()
    #print( data )
    return data

def backoff_tagger(train_sents, tagger_classes):
        backoff = DefaultTagger('NN')
        for cls in tagger_classes :
                backoff = cls(train_sents, backoff=backoff)
        return backoff

train_sents = brown.tagged_sents()[:1000]
emma_taggery = backoff_tagger(train_sents, [UnigramTagger,BigramTagger, TrigramTagger])
name_taggery = NamesTagger(emma_taggery)


def join(word_list):
    stringy = ""
    for word in word_list:
        stringy = stringy + " " + word[0]
    return stringy[1:]

def extract_entities(parse_tree):
    words = []
    for child_node in parse_tree:
        if type(child_node) == nltk.tree.Tree:
            words.append(join(child_node.leaves()))
    return words


def find_named_entities(sent):
    tknzr = TweetTokenizer()
    sent_tokens = tknzr.tokenize(sent)

    tagged_sent = name_taggery.tag(sent_tokens)

    grammar = """
                    
                    NE :
                    {<AT|PP\$>?<NNP|NN|NP|NN-TL|NP-TL>+<IN|IN-TL><NNP|NN|NP|NN-TL|NP-TL>+}
                    {<AT|PP\$>?<NNP|NN|NP|NN-T|NP-TL>+}
                    
                         """

    parser = nltk.RegexpParser(grammar)
    parse_tree = parser.parse(tagged_sent)
    return extract_entities(parse_tree)


def classify(named_entitiy):
    #I haven't implented this function.
    #I intend to classify the entity using wikification
    #for now I'll just return name so that I can
    #write the tagging function
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

    
    
    


