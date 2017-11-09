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


def classifiy(named_entitiy):
    #I haven't implented this function.
    #I intend to classify the entity using wikification
    #for now I'll just return name so that I can
    #write the tagging function
    return "name"



def check_match(current_run, named_entity):
    ne_tokens = TweetTokenizer().tokenize(named_entity)
    i = 0
    while i < len(current_run) and i < len(ne_tokens):
        if current_run[i] != ne_tokens[i]:
            return "no match"
        i += 1
    #(we don't need to worry about if it is more than this,
    #because the current run will be detected at not a match before
    #it gets that long)
    if len(current_run) < len(ne_tokens):
        return "partial match"
    else:
        return "match"

def get_tag_locations(words, named_entities):
    #finds the locations that different tags have to go in
    #doesn't work yet
    tag_locations = []
    for i in range(len(words)):
        for ne in named_entities:
            print(words[i])
            word_run = []
            word_run.append(words[i])
            j = i + 1
            print(join(word_run) + " : " + check_match(word_run,ne[0]))
            while check_match(word_run,ne[0])== "partial match" and j < len(words):
                word_run = word_run.append(words[j])
                j += 1
            if check_match(word_run,ne[0]) == "match":
                tag_locations.append( ((i,j-1),ne[1]) )
    return tag_locations
    
def tag_named_entities(sent, named_entities):
    #THIS FUNCTION IS INCOMPLETE
    #this function takes the classified named entities
    #and builds new sentence with the tags in place
    
    #splits the sentence into seperate words
    tknzr = TweetTokenizer()
    words = tknzr.tokenize(sent)

    #records the start index of the current run if there is one
    start_run_index = -1

    #stores the locations to put all the tag pairs
    tag_locations = []
    
               
           
        
        
        

def main():
    path = "untagged/"
    tokenizer = nltk.data.load('tokenizers/punkt/PY3/english.pickle')
    for file in get_files(path):
        data = read_file(path,file)
        dataTokens= tokenizer.tokenize(data)
        print(dataTokens)

    
    
    


