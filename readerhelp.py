import re
import os
import sys
import nltk
import nlkt_data

from nltk.corpus.reader import WordListCorpusReader
from os                 import listdir
from os.path            import isfile, join



# My function to clear screen - I want it to work on all Operating Systems.
def cls(): print ("\n" * 50)



cls()
message = 'Replace value of "path" with path to your data folder containing files from: https://canvas.bham.ac.uk/courses/27273/files/folder/Data?preview=4298143'

path    = message  ### REPLACE HERE!

if path == message :
    print( path )
    sys.exit()


print ( """
We first extract a list of files from the folder. 
We can do this using two different methods: 
    The usual loop 
    A smart loop that python provides. 

Let's start with the usual loop, it looks like so: 


all_files = listdir( path ) ## listdir is a function that lists all files in 'path'
print( listdir(path) )      ## Lets print to see what's in this. 

# This might have some folders in it - we want to get rid of that and store only files into 'clean_file_info':
clean_file_info = list()
for single_file in all_files :
    # Lets see what join( path, single_file ) provides - notice it's a single file. 
    print( join( path, single_file ) )
    # if this is a file
    if isfile( join( path, single_file ) ) :
        # Add it to 'clean_file_info'
        clean_file_info.append( single_file ) 

  

Now Press ENTER Key to run this code ... 
""" )

discard = input( "" )


all_files = listdir( path ) 
print( listdir(path) )
print()
print( "Printed listdir(path), press ENTER to continue" )
discard = input( "" )

printed = False
clean_file_info = list()
for single_file in all_files :
    print( join( path, single_file ) )
    if not printed : 
        print( "Ran, print( join( path, single_file ) ), press ENTER to continue" )
        discard = input( "" )
        printed = True

    if isfile( join( path, single_file ) ) :
        clean_file_info.append( single_file ) 


print( """

Great, so now we have just the files. Let's do this using the "smart" Python way: 
files = [f for f in listdir(path) if isfile(join(path, f))]

Press ENTER to run this command. 
""" ) 
discard = input( "" )

files = [f for f in listdir(path) if isfile(join(path, f))]

print( """

Now lets check if they are equal: 

print( files == clean_file_info )

Press ENTER to run this command.

""" ) 
discard = input( "" )


print( files == clean_file_info )


print( """

Indeed they are!

Now let's check to see if this contains the file .DS_Store!

print( '.DS_Store' in files ) 

Press ENTER to run this command.

""" )
discard = input( "" )

cls()
print( '.DS_Store' in files ) 

print( """
Again, yes!

Now let's run the following code to get rid of it

try : 
    del( files[files.index( '.DS_Store' )] )
except :
    pass

print( '.DS_Store' in files ) 

Notice how it's been placed in a try block - This is in-case the file does not exist!
Why have our code crash when looking for an error that does not exist!

At the end of it, we check again to see if there the file is in the list!

Press ENTER to run this command. 

""" ) 
discard = input( "" )
cls()


try : 
    del( files[files.index( '.DS_Store' )] )
except :
    pass


print( '.DS_Store' in files ) 


print( """

Great, so we've gotten rid of that!

Now we need to loop through each of the files and extract the information we want from them. 

The following piece of code will do that for you. 

NOTE: There is a better way of doing this using WordListCorpusReader. This bit does not use it
      for simplicity. You are encouraged to use WordListCorpusReader.


for single_file in files :
    file_handle = open( join( path, single_file ), 'r' )
    data = f.read()
    file_handle.close()

    print( data ) 

    break


# Notice join(path, single_file) can be written as: 
#     path + "/" + single_file.
#  What if we are on Windows though that requires "\\" instead of "/"?
#  join() is a "smart" way of making sure you add the correct slash. 

#  I've added a break there so we can read what's in data - of course 
#     you will not do this otherwise. 


Now press ENTER to run this bit. 

""" ) 

discard = input( "" )



for single_file in files :
    file_handle = open( join( path, single_file ), 'r' )
    data = file_handle.read()
    file_handle.close()

    print( data ) 
    
    break



print()
print( "Press Enter to continue" )
discard = input( "" )

cls()

print( """

Now that we have one file stored in data, we need to be able to tokenize it.

The best way to do this is to use the NLTK nltk.tokenize package. 

You should use it to tokenize this file, learn more here: 
http://www.nltk.org/api/nltk.tokenize.html

Press Enter to continue
""" )
discard = input( "" )
cls()

print( """

Now, let's see how we can use regular expressions. 

Regular expressions are available in the package "re" 

You need to import it like so: 

import re

Now, I'm going to create some dummy data so we can experiment: 


    data = \"\"\" 
It was the best of times, it was the worst of times, <my_tag_one>it was the age of wisdom</my_tag_one>, it was the age of foolishness, it was the epoch of belief, it was the epoch of incredulity, it was the season of Light, <my_tag_one>it was the season of Darkness, it was the spring of hope</my_tag_one>, it was the winter of despair, we had everything before us, we had nothing before us, we were all going direct to Heaven, we were all going direct the other way – in short, the period was so far like the present period, that some of its noisiest authorities insisted on its being received, for good or for evil, in the superlative degree of comparison only.
\"\"\" 


Press Enter to continue 
""" )
discard = input( "" )
cls()

print( """
Here is the regex (short for regular expression) that I use to extract what's between <my_tag_one> and </my_tag_one>

    re.findall( r'<my_tag_one>.*?</my_tag_one>', data, re.M )

Note that what's between r'' is the regular expression. 

The . represents "any character" 
The * says, 0 or more times. 
so .* says, pick up any character, occurring one 0 or more times. 

But notice how we have two of these tags - * is by default "greedy". This means that it will keep "matching" 
until if finds the "last" </my_tag_one>. We don't want this. We want it to stop the first time it sees a 
</my_tag_one>. We achieve this by adding the ?

Notice the final parameter (re.M). This says that we want to match across multiple lines. 

You can (and really should) read more about regular expressions. You can find that here: 
https://docs.python.org/3/howto/regex.html

Let's see what this does - Press ENTER to run this bit. 

""" )

discard = input( "" )

data = """ 
It was the best of times, it was the worst of times, <my_tag_one>it was the age of wisdom</my_tag_one>, it was the age of foolishness, it was the epoch of belief, it was the epoch of incredulity, it was the season of Light, <my_tag_one>it was the season of Darkness, it was the spring of hope</my_tag_one>, it was the winter of despair, we had everything before us, we had nothing before us, we were all going direct to Heaven, we were all going direct the other way – in short, the period was so far like the present period, that some of its noisiest authorities insisted on its being received, for good or for evil, in the superlative degree of comparison only.
""" 

print( re.findall( r'<my_tag_one>.*?</my_tag_one>', data, re.M ) ) 
print()
print( "Press Enter to continue" ) 
discard = input( "" )
cls()

print( """
I'm just going to add a few things here that might help: 

the split function is a nice way of extracting bits from a string, usage:
string.split( 'what to split by' ) 

DO NOT USE THIS TO TOKENIZE!!! (Think about why not)

let's run
print( data.split( ',' ) ) 

""" )

print( data.split( ',' ) )

print()
print( "Press Enter to continue" ) 
discard = input( "" )
cls()


print( """
Notice that split keeps \\n (or newlines) 

Another useful thing to remember is re.sub
This function can be used to replace things using a regular expression. 

Let's use our previous ragas: 
    print( re.sub( r'<my_tag_one>.*?</my_tag_one>', '', data, re.M ) )

Let's see what this does:
""" ) 

print( re.sub( r'<my_tag_one>.*?</my_tag_one>', '', data, re.M ) )

print()
print( "Press Enter to continue" ) 
discard = input( "" )
cls()

print( """
Finally, everything I print can be assigned to a variable: 
   my_var = re.sub( r'<my_tag_one>.*?</my_tag_one>', '', data, re.M ) 
   print( my_var ) 

Here is the output: 
""" ) 

my_var = re.sub( r'<my_tag_one>.*?</my_tag_one>', '', data, re.M ) 
print( my_var ) 

print()
print( "Press Enter to continue" ) 
discard = input( "" )
cls()


print( """
Now you should use the POS tagger we looked at in the lab to tag the document you have
stored in 'data'. 

Note that you have been provided code to do this, you should read more about it
on: https://canvas.bham.ac.uk/courses/27273/pages/first-steps-in-the-assignment

I'm going to cheat and place previously tagged information into 'data'

data = [("the", "DT"), ("little", "JJ"), ("yellow", "JJ"),  ("dog", "NN"), ("barked", "VBD"), ("at", "IN"),  ("the", "DT"), ("cat", "NN")]

This is taken directly from the NLTK tutorial on Named Entity Recognition, available at: 
http://www.nltk.org/book/ch07.html

The output from your POS tagger should look something like this. 

""" ) 

data = [("the", "DT"), ("little", "JJ"), ("yellow", "JJ"),  ("dog", "NN"), ("barked", "VBD"), ("at", "IN"),  ("the", "DT"), ("cat", "NN")]

print()
print( "Press Enter to continue" ) 
discard = input( "" )
cls()

print( """
Great - now what good it is this? 

It so happens that you can define a regular expression based on the tags provided by the POS tagger!

You can do this using NLTK like so: 

grammar = "NP: {<DT>?<JJ>*<NN>}" 
cp = nltk.RegexpParser(grammar)
result = cp.parse(data)

print( result ) 


You can check the data type of 'result' using: 
print( type( result ) ) 

Press ENTER to run this bit. 
""" ) 
discard = input( "" )

grammar = "NP: {<DT>?<JJ>*<NN>}" 
cp = nltk.RegexpParser(grammar)
result = cp.parse(data)
print( result ) 
print( type( result ) ) 


print( """ 

Now how do we access the bits that we are interested in?

Loop through each of the elements in 'result' and check if the
type of the result is of type Tree (which is how matched elements are stored)

If it is, then you can extract the words using the leaves() function

for elem in result : 
   if type( elem ) == nltk.tree.Tree : 
      print( elem.leaves() )

Press ENTER to run this bit. 
""" ) 
discard = input( "" )


for elem in result :
    if type( elem ) == nltk.tree.Tree : 
        print( elem.leaves() )



print( """

Now remember you need to find the "kind" of Named Entity this is: 

You can use the data you extract from the training set as a database you check against. 

You can also use the names dataset to check for people!

Press ENTER to continue ... 

""" )
discard = input( "" )

cls()
print( """
Some final notes: 

Remember to make sure you use functions! You must place each independent section in a
function. 

Remember that you need to have two different bits - One is the training bit that 
extracts useful information and the other is the bit that actually tags
previously untagged information. 

DO NOT USE AN EXISTING Named Entity Recognition tool!

DO NOT COPY large sections of this file into your final code. 

Your code WILL be tested against this file and you will lose a lot of (if not all) 
marks if significant overlap is found. 


You can send in your questions to: H.T.Madabushi@cs.bham.ac.uk


Best of luck ... 

""" )



## Version 0.2 -- identification marker: 458.
