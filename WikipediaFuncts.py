import sys, http.client, urllib.request, urllib.parse, urllib.error, json
from nltk.tokenize import TweetTokenizer
import re

def get_url( domain, url ) :
    # Headers are used if you need authentication
    headers = {}
    # If you know something might fail - ALWAYS place it in a try ... except
    try:
        conn = http.client.HTTPSConnection( domain )
        conn.request("GET", url, "", headers)
        response = conn.getresponse()
        data = response.read()
        conn.close()
        return data
    except Exception as e:
        # These are standard elements in every error.
        print("[Errno {0}] {1}".format(e.errno, e.strerror))
        # Failed to get data!
    return None

def is_word(token):
    #matches a token up against a regular expression to see if it a word
    #we need to do this, because we want to eliminate things like spaces and stuff
    #a word is just a sequence of one or more letter character
    pattern = re.compile('[a-zA-Z]+')
    match = pattern.match(token)
    if match:
        return True
    else: return False

def get_words( entity ):
    #this function basically goes to wikipedia and gets a list of all the words relating to an enitity
    
    #creates a query to send to wikipedia
    query = urllib.parse.quote_plus( entity )

    #communicates with wikipedia to get back some data
    url_data = get_url( 'en.wikipedia.org', '/w/api.php?action=query&list=search&format=json&srsearch=' + query )

    #if it doesn't find any then we just return this for now
    #this probably mean something's gone wrong in the get_url function :(
    if url_data is None :
        return(["ERROR ERROR ERROR"])


    #the code below goes through the data we found and extracts all the words
    
    words = []


    url_data = url_data.decode( "utf-8" )
    url_data = json.loads( url_data )
    #loops through all the search hits (we use keys in square brackets, because url_data
    #is a dictionary object
    try:
        for entry in url_data['query']['search']:
            #gets the "snippet", which is the bit with the words
            text = entry["snippet"]
            #removes the span tags, because they don't help at all
            text = text.replace("</span>","")
            text = text.replace("<span class=\"searchmatch\">","")
            #splits the remaining text into individual words
            text = TweetTokenizer().tokenize(text)
            #this loop checks every token to see if it is a word and only keeps words in the list 
            text = [token for token in text if is_word(token)]
            #it adds this to our word list
            words = words + text
    except Exception:
        return []
        
    

    return words
