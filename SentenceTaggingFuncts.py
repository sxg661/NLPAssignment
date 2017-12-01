import re
import os
import sys
import nltk
import nltk.data




def get_sentences(data):
    #one thing i've noticed is that sentences seem to almost never have certain substrings e.g. two spaces in a row
    #whereas things which are not sentences almost always have atleast one, so I am going to find the setences that way :)

    #this tokenizer splits the data rougly into sentences
    tokenizer = nltk.data.load('tokenizers/punkt/PY3/english.pickle')
    tokens = tokenizer.tokenize(data)

    #now we can check for spaces:
    
    illegalSentenceStrings = ["--","  ","**","==","\n\n"]

    #anything in the format <Word>:<something else> is also not going to be a sentence
    illegalRegEx = re.compile("[a-zA-Z]+:.*")

    sentences = []

    for token in tokens:
        if not illegalRegEx.match(token):
            illegal = False

            for string in illegalSentenceStrings:
                if string in token:
                    illegal = True

            if not illegal:
                sentences.append(token)

    return sentences

def get_paragraphs(data):
    paragraphs = []


    paragraphRegEx = re.compile("<sentence>.*</sentence>")

    pargraphs = paragraphRegEx.findall(data)

    for i in range(0,len(paragraphs)):
        print(i)
        #just trims off thr new lines
        paragraph[i] = paragraph[i][:len(paragraph[i])]
    

    return paragraphs
