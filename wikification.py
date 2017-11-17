import sys, http.client, urllib.request, urllib.parse, urllib.error, json
from nltk.corpus        import names
from collections         import Counter
from nltk.tokenize import TweetTokenizer
import re
from os                 import listdir
from os.path            import isfile, join
import math


    
#These functions allow us to access wikipedia

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

    return words


#These functions do training on the training data
    
def trim_first_last(string):
    #just removes the first and last character from a string
    return string[1:len(string)-1]


def lose_tags(tag_string):
    #takes a string with tags and gets rid of the tags
    #e.g. "<speaker>Aikaterini</speaker>" -> "Aikaterini"

    #from my example above, this regular expression would extract:
    #>Aikaterini<
    #then all we need to do is trim the first and later characters off of this
    #(the .* basically means any number of character any number of times)
    pattern = re.compile(">.*<")
    tagless = pattern.findall(tag_string)[0]
    return trim_first_last(tagless)
    

def get_tag_examples(tag_name, data, tag_dict):
    #takes the data from a file and finds all the specific tagged entities

    #gets rid of all the "</sentence>" because they sometimes overlap with
    #the location/speaker tags e.g. <location>The Muirhead Tower</sentence></location>
    #this isn't a real example. I can't find any now I'm actually looking, so I'm not sure
    #if I just made this up, but it can't hurt to add it in, just to be sure
    data = data.replace("</sentence>","")

    #uses a regular expression to find all the tagged entities with the given tag name
    opening_tag = "<{}>".format(tag_name)
    closing_tag = "</{}>".format(tag_name)
    #[^<] means any character except for <. I added this to avoid capturing things like:
    #"<location>The Muirhead Tower</location> and <location>The Aston Webb</location>"
    #which also have <tag_name> at the start and </tag_name> at the end
    pattern = re.compile("{}[^<]*{}".format(opening_tag,closing_tag))
    matches = pattern.findall(data)

    #removes the tags from every single match
    matches_notags = []
    for match in matches:
        #we'll just get rid of newlines now to make everything easier
        match = match.replace("\n"," ")
        match_nt = lose_tags(match)
        matches_notags.append(match_nt)

        #adds this tag to the dictionary
        #the while loop makes sure we get a unique key which isn't
        #in the dictionary (keep adding zs until it's not in there)
        while match_nt in tag_dict:
            match_nt = match_nt + "z"
        tag_dict[match_nt] = tag_name
    
    return matches_notags, tag_dict

def build_single_file_vocab(tag_name, data, tag_dict):
    print("entered")
    #takes all the entities with a certain tag name from one string of data from a single file
    #then it goes on wikipedia and gets all the words that come up when you search that string

    tag_examples, tag_dict = get_tag_examples(tag_name, data, tag_dict)

    words = []

    #we need this to help calculate our prior probabilities
    #for bayes later on

    for entity in tag_examples:
        
        words = words + get_words(entity)

    return words, tag_dict


def get_files(path):
    #gets the file paths to the training data
    files = [f for f in listdir(path) if isfile(join(path, f))]
    try :
        del( files[files.index( '.DS_Store' )] )
    except :
        pass
    return files

def read_file(path, file):
    #reads all the text out of a file in a string object
    file_handle = open( join(path, file), 'r' )
    data = file_handle.read()
    file_handle.close()
    return data


def build_training_vocabs(tag_names):
    path = "training/"
    #gets all our file path
    #I only took the first 20 otherwise we're going to be here all day
    #(This code code isn't very efficient)
    files = get_files(path)[:30]
    
    #this will contain all the words we get from wikipedia
    vocabs = {}

    #this will contain info about all the tags we find
    tag_dict = {}


    #for all our file paths, we can get the data from the files
    #run all of them through the build_single_file_vocab() function
    #and add to our vocab

    for file in files:
        data = read_file(path,file)
        for tag_name in tag_names:
            tag_vocab, tag_dict = build_single_file_vocab(tag_name, data, tag_dict)
            if tag_name in vocabs:
                vocabs[tag_name] = vocabs[tag_name] + tag_vocab
            else: vocabs[tag_name] = tag_vocab
            


    return vocabs, Counter(tag_dict.values())



#Counter(<dictionary_name>.values())
#Counter(<list_name>)


def log_likelihood(word, vocab, classDict, classWords):
    count_word_in_class = 0
    if word in classDict:
        count_word_in_class = classDict[word]
    else: count_word_in_class = 0

    prob_in_class = (count_word_in_class + 1) / ( len(set(classWords) ) + len(vocab) )
    return math.log10(prob_in_class)


def naive_bayes(wiki_words, logPrior, vocab, classDict, classWords):
    sumProbs = logPrior
    for word in wiki_words:
        if word in vocab:
            sumProbs += log_likelihood(word, vocab, classDict, classWords)
    return sumProbs


def classify(entity, vocabs, tag_occurances, tag_names):

    
    current_max = [None,None]

    number_tags = 0
    vocab = []
    for tag_name in tag_names:
        number_tags += tag_occurances[tag_name]
        vocab = vocab + vocabs[tag_name]
    vocab = set(vocab)

    

    for tag_name in tag_names:
        wiki_words = get_words(entity)
        logPrior = math.log10(tag_occurances[tag_name] / number_tags)
        classDict = Counter(vocabs[tag_name])
        classWords = vocabs[tag_name]
        sumProbs = naive_bayes(wiki_words,logPrior,vocab,classDict,classWords)
        if current_max[1] == None or current_max[1] < sumProbs:
            current_max = [tag_name,sumProbs]

    return current_max[0]
        
        
    
def classify_test(entity):
    tag_names = ["speaker","location"]
    vocabs, tag_occurances = build_training_vocabs(tag_names)
    return classify(entity,vocabs,tag_occurances,tag_names)
    
tag_names0 = ["speaker","location"]
vocabs0,tag_occurances0    = build_training_vocabs(tag_names0)

        
        
        
    


    






