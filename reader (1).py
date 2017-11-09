import re
import os
import sys
import nltk
import nltk.data

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



def main():
    path = "untagged/"
    tokenizer = nltk.data.load('tokenizers/punkt/PY3/english.pickle')
    for file in get_files(path):
        data = read_file(path,file)
        dataTokens= tokenizer.tokenize(data)
        print(dataTokens)




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

train_sents = brown.tagged_sents()[:20000]
taggery = backoff_tagger(train_sents, [UnigramTagger,BigramTagger, TrigramTagger])

def tag_named_entities(sent):
    tknzr = TweetTokenizer()
    sent_tokens = tknzr.tokenize(sent)

    tagged_sent = taggery.tag(sent_tokens)

    grammar = """NE : {<DT|PP\$>?<NP>+}
                      {<DT|PP\$>?<NP>+<IN><NP>+}"""

    parser = nltk.RegexpParser(grammar)
    parse_tree = parser.parse(tagged_sent)
    print(parse_tree)

    
    
    


