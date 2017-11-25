import re

# extracts the time based on the regular expression
# I've only included \: (as in 12:34) because at the moment
# I'm not sure how to express a . (as in 12.34)
# It only returns something like 12:34 not <stime>12:34</time?
# Don't know if this is any good
def find_time_matches(data):
    time = re.compile('[0-9][0-9]?\:[0-9][0-9][ ][am|AM|pm|PM|a.m|A.M|p.m|P.M]{2,3}')
    matches = time.findall(data)
    return matches

# takes an initially empty dictionary and fill it with
# time entries, where tag_name = 'stime'
time_dict = {}
def get_time_examples(tag_name, data, time_dict):
    matches = find_time_matches(data)

    for match in matches:
            # what are we going to do about duplicates?
            time_dict[match] = tag_name

    return time_dict

# This command:
# get_time_examples('stime', "I will go see my friends at 9:34 PM tonight. But I will be home by 3:24 p.m. Then I'll wake up tomorrow at 1:11 pm.", time_dict)
# returns:
# {'9:34 PM': 'stime', '3:24 p.m': 'stime', '1:11 pm.': 'stime'}
