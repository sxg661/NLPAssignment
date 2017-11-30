# check functionality at your leisure

import re

# IT DOESN'T WORK IF I JUST DO \.
def find_time_matches(data):
    time = re.compile('[0-9][0-9]?\:[0-9][0-9][ ][am|AM|pm|PM|a.m|A.M|p.m|P.M]{2,3}')
    matches = time.findall(data)
    return matches

# fills a dictionary with time entries with tag_name = 'stime'
def get_time_examples(data, time_dict):
    matches = find_time_matches(data)

    for match in matches:
            # what are we going to do about duplicates?
            time_dict[match] = 'stime'

    return time_dict

# finds all end times of the form ' - x:xx PM/AM' etc...
# which is why we'll later need to trim the ' - ' part
def find_end_time_matches(data):
    time_end = re.compile('[ ][-][ ][0-9][0-9]?\:[0-9][0-9][ ][am|AM|pm|PM|a.m|A.M|p.m|P.M]{2,3}')
    matches_end = time_end.findall(data)
    return matches_end

# spots every specific end time and replace its tag with 'endtime'
def get_end_time_examples(data):
    full_time_dict = get_time_examples(data, {}) # first a dict of all times
    full_end_time_dict = find_end_time_matches(data) # a dict of all end times
    for time in full_end_time_dict: # for every time in end dict
        time_trim = trim_first_three(time) # trim it
        if is_in_dict(time_trim, full_time_dict): # if that end time is in the dict of all times
            full_time_dict[time_trim] = 'endtime' # change its tag from 'stime' to 'endtime'
    return full_time_dict # return the modified dict of all times with all the right tags

# checks if a certain time is in a certain dict
def is_in_dict(time_check, time_dict):
    if time_check in time_dict:
        return True
    else:
        return False

# takes a string and returns it without its first three characters
def trim_first_three(end_time):    
    return end_time[3:len(end_time)]

#EXAMPLE INPUT - OUTPUT:
# get_end_time_examples('I will be going to the gym from 6:00 PM - 8:00 PM. Then I will visit my friends from 8:00 PM - 11:00 PM. And then I will be sleeping from 11:00 PM - 9:00 AM.')
# {'6:00 PM': 'stime', '8:00 PM.': 'endtime', '8:00 PM': 'stime', '11:00 PM.': 'endtime', '11:00 PM': 'stime', '9:00 AM.': 'endtime'}
