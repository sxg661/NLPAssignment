import math
from collections         import Counter
import WikipediaFuncts
import TagExtractingFuncts
import FileReadingFuncts
import re



def get_examples(tag_name):
    inputFile = "tagFiles/" + tag_name + ".txt"
    examples = FileReadingFuncts.read_all_lines(inputFile)
    return examples



def build_vocab(tag_name, tag_dict):
    print("entered")
    #takes all the entities with a certain tag name from one string of data from a single file
    #then it goes on wikipedia and gets all the words that come up when you search that string

    examples = get_examples(tag_name)

    word_file = "wiki/{}.txt".format(tag_name)
    words = FileReadingFuncts.read_wiki(word_file)

    for example in examples:
        key = example
        if key in tag_dict:
            key = key + "z"
        tag_dict[key] = tag_name
    
    return words, tag_dict



def build_training_vocabs(tag_names):
    
    #this will contain all the words we get from wikipedia
    vocabs = {}

    #this will contain info about all the tags we find
    tag_dict = {}


    #builds a vocab for each tag_name
    #I've already extracted the tags with a function
    #in FileWritingFuncts, so all we need to do is read the
    #text file
    for tag_name in tag_names:
        tag_vocab, tag_dict = build_vocab(tag_name, tag_dict)
        vocabs[tag_name] = tag_vocab
            

    #the values in the dictionary are that tag types, so we can use the Counter type to
    #store how many times each tag occured
    return vocabs, Counter(tag_dict.values())





def log_likelihood(word, vocab, classDict, classWords):
    #works out the liklihood of a word occuring for a specific class
    count_word_in_class = 0
    if word in classDict:
        count_word_in_class = classDict[word]
    else: count_word_in_class = 0

    prob_in_class = (count_word_in_class + 1) / ( len(set(classWords) ) + len(vocab) )
    return math.log10(prob_in_class)


def naive_bayes(wiki_words, logPrior, vocab, classDict, classWords):
    #works out the liklihood for each class and sums the results to get an overall
    #liklihood of the word having that tag
    sumProbs = logPrior
    for word in wiki_words:
        if word in vocab:
            sumProbs += log_likelihood(word, vocab, classDict, classWords)
    return sumProbs

class ResultInfo:
    def __init__(self, tag_name, sumProb):
        self.tag_name = tag_name
        self.sumProb = sumProb

    def get_tag_name(self):
        return self.tag_name

    def get_sumProb(self):
        return self.sumProb


def classify(entity, vocabs, tag_occurances, tag_names):
    #takes an entity with the prebuild vocabs and classifies it using naive bayes

    #stores the total number of tags
    number_tags = 0
    #stors the overall vocab
    vocab = []
    for tag_name in tag_names:
        #adds the number of tags for this tag_name to the overall number of tags
        number_tags += tag_occurances[tag_name]
        #adds the vocab to this tag_name for the overall vocab
        vocab = vocab + vocabs[tag_name]
    #(we only want each word once)
    vocab = set(vocab)

    #contains the current most likely classification
    current_max = ResultInfo(None,None)
    #so that we can tell how close it is, we also want to return the 2nd max
    current_second_max = ResultInfo(None,None)

    for tag_name in tag_names:
        #gets all the paramters for naive bayes
        wiki_words = WikipediaFuncts.get_words(entity)
        logPrior = math.log10(tag_occurances[tag_name] / number_tags)
        classDict = Counter(vocabs[tag_name])
        classWords = vocabs[tag_name]

        #performs naive bayes updates the current max and second max accoridngly
    
        sumProb = naive_bayes(wiki_words,logPrior,vocab,classDict,classWords)
    
        if current_max.get_sumProb() == None or sumProb > current_max.get_sumProb():
            
            current_second_max = ResultInfo(current_max.get_tag_name(), current_max.get_sumProb())
            current_max = ResultInfo(tag_name,sumProb)
                                            
        elif current_second_max.get_sumProb() == None or sumProb > current_second_max.get_sumProb():
                                            
            current_second_max = ResultInfo(tag_name, sumProb)


    return current_max, current_second_max



def classify__bayes(entity, strict, tag_names, vocabs, tag_occurances):

    best_match, second_match = classify(entity, vocabs, tag_occurances, tag_names)
   
    if strict:
        return best_match.get_tag_name()
    else:
        if abs(best_match.get_sumProb() - second_match.get_sumProb()) > 50:
            return best_match.get_tag_name()
        else: return None
        
    return "name"


def classify__files(entity, tag_names, examples):
    for tag_name in tag_names:
        if entity in examples[tag_name]:
            return tag_name
    return None


