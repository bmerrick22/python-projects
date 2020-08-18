#!/usr/bin/env python3

import os
import sys
import pprint
import requests

# Globals
URL      = 'https://www.reddit.com/r/{i}/.json'
ISGD_URL = 'http://is.gd/create.php'



# Functions

#function that shows how to use the program
def usage(status=0):
    ''' Display usage information and exit with specified status '''
    print('''Usage: {} [options] URL_OR_SUBREDDIT

    -s          Shorten URLs using (default: False)
    -n LIMIT    Number of articles to display (default: 10)
    -o ORDERBY  Field to sort articles by (default: score)
    -t TITLELEN Truncate title to specified length (default: 60)
    '''.format(os.path.basename(sys.argv[0])))
    sys.exit(status)


#Loads the data from a URL using requests
def load_reddit_data(url=URL):
    ''' Load reddit data from specified URL into dictionary '''

    headers  = {'user-agent': 'reddit-{}'.format(os.environ.get('USER', 'cse-20289-sp19'))}
    response = requests.get(url, headers=headers)
    data = response.json() 
    return data
    pass


#Displays the data in a nice format by the order, default is score
def dump_reddit_data(data, limit, orderby, titlelen, shorten):
    ''' Dump reddit data based on specified attributes '''
    
    listData = data['data']['children']

    if orderby == 'score':
        data2 = sorted(listData, key=lambda x: x['data'].get(orderby, 0),reverse = True)
    else:
        data2 = sorted(listData, key=lambda x: x['data'].get(orderby, 0))
        
   
 
    for index, entry in enumerate(data2,1):
        if index > 1:
            print()

        if limit < index:
            break 

        title = entry['data']['title']
        tempURL = entry['data']['url']
        order = entry['data']['score']

        if shorten == True:
            tempURL = shorten_url(tempURL)

        print('{:4}.\t{} (Score: {})'.format(index, title[:titlelen], order))
        print('\t{}'.format(tempURL))
    


#Function to shorten the URL
#Parses through json to get the url
def shorten_url(url):
    ''' Shorten URL using yld.me '''
    response = requests.get(ISGD_URL, params={'format': 'json', 'url': url})
    shortData = response.json()
    
    return shortData['shorturl']
    pass



# Parse Command-line Options
limit = 10
orderby = 'score'
titlelen = 60
shortURL = False

args = sys.argv[1:]
while len(args) and args[0].startswith('-') and len(args[0]) > 1:
    arg = args.pop(0)
    
    if arg == '-n':
        limit = int(args[0])
        args.pop(0)
    elif arg == '-s':
        shortURL = True
    elif arg == '-o':
        orderby = args[0]
        args.pop(0)
    elif arg == '-t':
        titlelen = int(args[0])
        args.pop(0)
    else:
        usage(1)

#If there are bad arguments, usage
if(len(args) == 0):
    usage(0)

#Check for certain case there is a provided URL
if args[0].startswith('https'):
    URL = args[0]
else:
    URL = URL.format(i=args[0])

# Main Execution
data = load_reddit_data(URL)
dump_reddit_data(data, limit, orderby, titlelen, shortURL)



