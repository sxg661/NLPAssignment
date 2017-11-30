# IMPLEMENT MULTIWORD TOPICS
# GET THE LEMMA SO THAT I CAN CHECK WHETHER THIS IS THE DESIRED ONTOLOGY
# TRY TO GET THE HYPER_LOOP TO BE AN ACTUAL LOOP[

from nltk.corpus.reader.wordnet import Synset
from nltk.corpus import wordnet
import re

ontologies = [Synset('discipline.n.01')]

def collect_topics(data):
    topic = re.compile('Topic:    ' + '[^/n]*')
    topics = topic.findall(data)
    for topic in topics:
        return trim_header(topic)

def trim_header(topic):    
    return topic[10:len(topic)]

def get_synsets(topic):
    topic_syns = wordnet.synsets(topic)
    return topic_syns

def assign_synset(topic_syns):
    syn_pick = topic_syns[0]
    return syn_pick

def find_hypernym(syn_pick):
    t_hyper = syn_pick.hypernyms()
    return t_hyper

def assign_hypernym(t_hyper):
    hyper_pick = t_hyper[0]
    return hyper_pick

def hyper_loop(data):
    topic = collect_topics(data)
    print(topic)
    topic_syns = get_synsets(topic)
    print(topic_syns)
    syn_pick = assign_synset(topic_syns)
    print(syn_pick)
    f_hyper = find_hypernym(syn_pick)
    print(f_hyper)
    hyper_pick = assign_hypernym(f_hyper)
    print(hyper_pick)
    if (hyper_pick in ontologies):
        print(hyper_pick + "is our ontology!")
    else:
        print(hyper_pick + "is not out ontology! Carrying on...")
        h_hyper = find_hypernym(hyper_pick)
        print(h_hyper)
        hp_hyper = assign_hypernym(h_hyper)
        print(hp_hyper)
        h_h_hyper = find_hypernym(hp_hyper)
        print(h_h_hyper)
        hpp_hyper = assign_hypernym(h_h_hyper)
        print(hpp_hyper)
