import sys, http.client, urllib.request, urllib.parse, urllib.error, json
from nltk.corpus        import names

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

def classify( entity ):
    query = urllib.parse.quote_plus( entity )
    url_data = get_url( 'en.wikipedia.org', '/w/api.php?action=query&list=search&format=json&srsearch=' + query )

    if url_data is None :
        return("undefined")

    url_data = url_data.decode( "utf-8" )
    url_data = json.loads( url_data )
    print(print(url_data['query']['search'][.type()))
    print(entity in names.words())
