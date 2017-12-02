# IMPLEMENT MULTIWORD TOPICS
# - seperated multi-word topics into seperate words

from nltk.corpus import wordnet
from nltk.tokenize import word_tokenize
import re

ontologies = ['discipline.n.01']

def collect_topics(data):
    topic = re.compile('Topic:    ' + '[^/n]*')
    topics = topic.findall(data)
    for topic in topics:
        topics_trim = trim_header(topic)
        topics_split = word_split(topics_trim)
    return topics_split
        
def word_split(string):
    words = word_tokenize(string)
    return words

def trim_header(topic):    
    return topic[10:len(topic)]


## FIX!!!!
def get_synsets(topics_split):
    for topic in topics_split:
        topic_syns = wordnet.synsets(topic)
        return topic_syn

def assign_synset(topic_syns):
    syn_pick = topic_syns[0]
    return syn_pick

def find_hypernym(syn_pick):
    t_hyper = syn_pick.hypernyms()
    return t_hyper

def assign_hypernym(t_hyper):
    hyper_pick = t_hyper[0]
    return hyper_pick

def make_syn_pick(data):
    topic = collect_topic(data)    # find the topic of email
    print(topic)
    topic_syns = get_synsets(topic) # find corresponding synsets
    print(topic_syns)
    syn_pick = assign_synset(topic_syns) # assign the first of those synsets to the topic
    return syn_pick
    
def hyper_loop_rec(data):
    hyper_pick = wordnet.synset('dog.n.01')
    syn_pick = make_syn_pick(data)    
    while (hyper_pick.name() not in ontologies):
        f_hyper = find_hypernym(syn_pick)
        hyper_pick = assign_hypernym(f_hyper)
        syn_pick = hyper_pick
        if (hyper_pick.name() in ontologies):
            print("Ontology found! Our ontology is: " + hyper_pick.name())
        else:
            print("We have not reached the desired ontology. Carrying on the search...")
