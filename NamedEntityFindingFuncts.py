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

def backoff_tagger(train_sents, tagger_classes):
        backoff = DefaultTagger('NN')
        for cls in tagger_classes :
                backoff = cls(train_sents, backoff=backoff)
        return backoff




def join(word_list):
    stringy = ""
    for word in word_list:
        stringy = stringy + " " + word[0]
    return stringy[1:]


def get_ne_broad_grammar(sent,tagger):
    grammar = """
                    
                    NE :
                    {<AT|PP\$>?<NNP|NN|NP|NN-TL|NP-TL>+<IN|IN-TL><NNP|NN|NP|NN-TL|NP-TL>+}
                    {<AT|PP\$>?<NNP|NN|NP|NN-T|NP-TL>+}
                    
                         """
    return find_named_entities(sent, grammar, tagger)

def get_ne_strict_grammar(sent,tagger):
    grammar = """
                    NE :
                    {<AT|PP\$>?<NNP|NP|NP-TL>+<IN|IN-TL><NNP|NP|NP-TL>+}
                    {<AT|PP\$>?<NNP|NP|NP-TL>}
                         """
    return find_named_entities(sent, grammar, tagger)

def find_named_entities(sent, grammar, tagger):
    tknzr = TweetTokenizer()
    sent_tokens = tknzr.tokenize(sent)

    tagged_sent = tagger.tag(sent_tokens)

    parser = nltk.RegexpParser(grammar)
    parse_tree = parser.parse(tagged_sent)
    return extract_entities(parse_tree)

def extract_entities(parse_tree):
    words = []
    for child_node in parse_tree:
        if type(child_node) == nltk.tree.Tree:
            words.append(join(child_node.leaves()))
    return words

