# We are going to use WordNet in order to find the ontology of the emails.
# Each word has a number of 'senses'. For example, the word 'chemistry' can mean
# the science, or the 'chemistry' between two people. Each word sense is known as
# a 'synset' in WordNet. What we are aiming to do is extract what is in the Topic
# header in each emails. This can either be one word (for example, Topic: Chemistry)
# or multiple words (such as Topic: Catalytic reactors). We are using regular expressions
# in order to make a successful extraction of the topic. If the topic is one word,
# we look for the synsets corresponding to this one word. If the topic consists of many
# words, we look for the synsets corresponding to the last word of the topic string.
# We proceed to find the synsets connected to the first or last word of the topic, depending
# on the one-word or multiword case. We go by this convention: out of all the synsets
# found for the topic, we shall assign it the very first one. Beyond that, we will proceed
# to find all hypernyms related to this synset we picked. We shall once again assign the first
# one to the synset by convention. We shall keep doing this until we reach a hypernym
# which is in our list 'ontologies'. When this happens, we shall terminate the execution
# and declare that hypernym as being our ontology under which our email is classified.

from nltk.corpus import wordnet
from nltk.tokenize import word_tokenize
import re

# our list of things we will consider our ontology once reached
ontologies = ['discipline.n.01', 'communication.n.02', 'act.n.02', 'device.n.01', 'artifact.n.01', 'whole.n.02', 'instrumentality.n.01', 'journey.n.01', 'time_period.n.01', 'problem_solving.n.02', 'attitude.n.01', 'substance.n.01', 'physical_entity.n.01', 'feeling.n.01', 'meeting.n.01', 'passage.n.01', 'attribute.n.02', 'location.n.01', 'process.n.02', 'person.n.01', 'ordering.n.01', 'language_unit.n.01', 'condition.n.01']

# gathering what the topic is from the "Topic:    " part of the email
def collect_topics(data):
    topic = re.compile('Topic:    (.+?)Dates')  # the regex
    topics = topic.findall(data)                # find and list the words of the topic
    for topic in topics:                        
        topics_split = word_split(topics)  # splitting the words of a possibly multiword topic (doesn't do anything if the topic is one word, eg. Chemistry)
    return topics_split

# the word splitting function       
def word_split(strings):
    for string in strings:
        words = word_tokenize(string)
    return words

# if we only have a one-word topic, use this
def get_synsets_first(topics_split):
    for topic in topics_split:
        topic_syns = wordnet.synsets(topic) # get the synsets connected to this topic
    return topic_syns

# if we have a multiword topic use this
def get_synsets_last(topics_split):
    topic = topics_split[len(topics_split)-1]   # get the synsets connected to the last word of the topic
    topic_syns = wordnet.synsets(topic)
    return topic_syns

# from our synsets, pick the first one and assign it to the topic
def assign_synset(topic_syns):
    try:
        topic_syn_pick = topic_syns[0]
        return topic_syn_pick
    except:
        pass
    
# find the hypernym of the topic (works for both one-word and multi-word without variation)
def find_hypernym(syn_pick):
    t_hyper = syn_pick.hypernyms()
    return t_hyper

# from our hypernyms, pick the first one and assign it to the topic
def assign_hypernym(t_hyper):
    hyper_pick = t_hyper[0]
    return hyper_pick

# big function to pick the synset (made to work for both one-word and multi-word)
def make_syn_pick(data):
    topics_split = collect_topics(data)    # find the topic of email
    if (len(topics_split) == 1):
        topic_syns = get_synsets_first(topics_split) # find corresponding synsets
        syn_pick_first = assign_synset(topic_syns)
        return syn_pick_first
    else:
        topic_syns = get_synsets_last(topics_split)
        syn_pick_last = assign_synset(topic_syns) # assign the first of those synsets to the topic
        return syn_pick_last

# pseudo-recursion
# keep finding and assigning hypernyms until one of the hypernym's reached is the ontology    
def hyper_loop_rec(data):
    hyper_pick = wordnet.synset('dog.n.01') # couldn't initialise to None so I am using a generic synset we are guaranteed not to use to start
    syn_pick = make_syn_pick(data)
    try:
        while (hyper_pick.name() not in ontologies):
            f_hyper = find_hypernym(syn_pick)
            hyper_pick = assign_hypernym(f_hyper)
            syn_pick = hyper_pick
            if (hyper_pick.name() in ontologies):
                return hyper_pick.name()
    except:
            pass
