import sys, http.client, urllib.request, urllib.parse, urllib.error, json
from nltk.corpus        import names
from collections         import Counter
from nltk.tokenize import TweetTokenizer
import re
import math
import FileReadingFuncts
import WikipediaFuncts


    


#These functions do training on the training data
    
def trim_first_last(string):
    #just removes the first and last character from a string
    return string[1:len(string)-1]


def lose_tags(tag_string):
    #takes a string with tags and gets rid of the tags
    pattern = re.compile(">.*<")
    tagless = pattern.findall(tag_string)[0]
    return trim_first_last(tagless)
    


def find_tag_matches(tag_name,data):
    #takes the data from a file and finds all the specific tagged entities


    #uses a regular expression to find all the tagged entities with the given tag name
    opening_tag = "<{}>".format(tag_name)
    closing_tag = "</{}>".format(tag_name)


    pattern = re.compile("{}[^<]*{}".format(opening_tag,closing_tag))
    matches = pattern.findall(data)

    return matches



def get_tag_examples(tag_name, data, tag_dict):
    matches = find_tag_matches(tag_name,data)

    #removes the tags from every single match
    for match in matches:
        #we'll just get rid of newlines now to make everything easier
        match = match.replace("\n"," ")
        match_nt = lose_tags(match)

        #adds this tag to the dictionary
        #(as a unique key, it honestly doesn't matter what the key is
        #so i just keep adding zs)
        while match_nt in tag_dict:
            match_nt = match_nt + "z"
        tag_dict[match_nt] = tag_name
    
    return tag_dict








        
        


        
        
        
    


    






