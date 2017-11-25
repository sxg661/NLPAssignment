import re

def findTime(sent):
    time = re.compile('[0-9][0-9]?\:[0-9][0-9][ ][am|AM|pm|PM|a.m|A.M|p.m|P.M]{2,3}')
    matches = time.findall(sent)
    return matches

# I've only included \: (as in 12:34) because at the moment
# I'm not sure how to express also a . (as in 12.34)
