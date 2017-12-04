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

import TimeFunct


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

def backoff_tagger(train_sents, tagger_classes):
        backoff = DefaultTagger('NN')
        for cls in tagger_classes :
                backoff = cls(train_sents, backoff=backoff)
        return backoff


def join(word_list):
    stringy = ""
    for word in word_list:
        word_to_add = word[0]
        #I don't want a space if the word is a dot, because of Dr. and Mrs. etc
        if word_to_add != ".":
            word_to_add = " " + word_to_add 
        stringy = stringy + word_to_add
    return stringy[1:]



def find_named_entities(sent, grammar, tagger):
    tknzr = TweetTokenizer()
    sent_tokens = tknzr.tokenize(sent)

    print("6.1")

    tagged_sent = tagger.tag(sent_tokens)

    print("6.2")

    parser = nltk.RegexpParser(grammar)

    print("6.3")
    
    parse_tree = parser.parse(tagged_sent)

    print("6.4")
    
    return extract_entities(parse_tree)



def extract_entities(parse_tree):
    words = []
    for child_node in parse_tree:
        if type(child_node) == nltk.tree.Tree:
            words.append(join(child_node.leaves()))
    return words


def filter_out_garbage(entities, tagger):
    #my broad grammer tends to pick up a lot of a garbage...

    ok_entities = []
       
    for entity in entities:
        words = TweetTokenizer().tokenize(entity)
        garbage = False

        if entity == "Dr":
            garbage = True

        for word in words:
            
            if get_tag(word, tagger) in ["NNP","NN","NP","NN-TL","NP-TL"]:
                #no nouns without capitals at the front are allowed!
                valid_noun_regex = re.compile("[A-Z].*")
                garbage = not valid_noun_regex.match(word)
            else:
                #no times are allowed!!!
                timeRegEx = re.compile("[0-9][0-9]?\:[0-9][0-9]")
                garbage = timeRegEx.match(word)

            if garbage:
                break

        if not garbage:
            ok_entities.append(entity)

    return ok_entities
                


def get_tag(entity, tagger):
    return tagger.tag(entity)[0][1]
   

def get_ne_broad_grammar(sent,tagger):
    print("here5")
    nouns = "(<OD>?<NNP|NN|NP|NN-TL|NP-TL>+<OD>?)"
    
    grammar = """
                    
                    NE :
                    {<NNP|NN|NP|NN-TL|NP-TL><NNP|NN|NP|NN-TL|NP-TL>}
                    {<NNP|NN|NP|NN-TL|NP-TL><NNP|NN|NP|NN-TL|NP-TL><NNP|NN|NP|NN-TL|NP-TL>}
                    {<AT|PP\$>?%+}
                    {(<NN><.>)?%+}
                    {<AT|PP\$>?(%+<IN|IN-TL|,>%+)+}
                    
                    
                    
                         """.replace("%",nouns)

    print("here6")

    entities = find_named_entities(sent, grammar, tagger)

    print("here7")
    
    return filter_out_garbage(entities, tagger)


 


    

    
#{<NN.>(%+<IN|IN-TL|,>%+)+}
#{<AT|PP\$>?(%+<IN|IN-TL|,>%+)+}
# {<AT|PP\$>?%+}

def get_ne_strict_grammar(sent,tagger):
    nouns = "(<OD>?<NNP|NN|NP|NN-TL|NP-TL>*<NNP|NP|NP-TL><NNP|NN|NP|NN-TL|NP-TL>*<OD>?)"
    
    
    grammar = """
                    NE :
                    {(<NN><.>)?%+}
                         """.replace("%",nouns)
    
    return find_named_entities(sent, grammar, tagger)






