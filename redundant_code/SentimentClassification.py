import math
from nltk.tokenize import TweetTokenizer


def main():
    tknzr = TweetTokenizer()


    posDocs = ["a tasty pizza", "gloriuos cheese", "the best restaurant ever", "i was blown away", "fabulous, just fabulous, best pizza ever", "I'm going back tomorrow!"]
    negDocs = ["cold and gloopy", "poor and slow service", "unbelievably bad", "tasted like shit", "waiter was extremely rude", "i feel sick just thinkig about it"]

    logPriorPos = math.log10( len(posDocs) / ( len(posDocs) + len(negDocs) ) )
    logPriorNeg = math.log10( len(negDocs) / ( len(posDocs) + len(negDocs) ) )

    #gets dicitonaries of all the words that are in the class and how often they occur
    posWords = get_word_array(posDocs, tknzr)
    negWords = get_word_array(negDocs, tknzr)
    
    vocab = set(posWords).union( set(negWords) )
    posDict = get_word_dict(posWords)
    negDict = get_word_dict(negWords)

    test_sent = tknzr.tokenize("my friend said this place was fabulous, but I thought it was unbelivably shit and bad")
    posTest = test_naive_bayes(test_sent, logPriorPos, vocab, posDict, posWords)
    negTest = test_naive_bayes(test_sent, logPriorNeg, vocab, negDict, negWords)

    if negTest > posTest:
        print("Negative")
    elif negTest < posTest:
        print("Postive")
    else: print("Neutral")
        
    


def test_naive_bayes(sentence, logPrior, vocab, classDict, classWords):
    sumProbs = logPrior
    for word in sentence:
        if word in vocab:
            sumProbs += log_likelihood(word, vocab, classDict, classWords)
    return sumProbs
        
        
        

def log_likelihood(word, vocab, classDict, classWords):
    count_word_in_class = 0
    if word in classDict:
        count_word_in_class = classDict[word]
    else: count_word_in_class = 0

    prob_in_class = (count_word_in_class + 1) / ( len(set(classWords) ) + len(vocab) )
    return math.log10(prob_in_class)
    

def get_word_array(docs, tknzr):
    words = []
    for doc in docs:
        for word in tknzr.tokenize(doc):
            words.append(word)
    return words

def get_word_dict(word_array):
    wordDict = {}
    for word in word_array:
        if word in wordDict:
            wordDict[word] += 1
        else:
            wordDict[word] = 1
    return wordDict
        

