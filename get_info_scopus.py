#######################################
# Created by        Alessandro Bigiotti 

# import the query link
from link_query_search import *
# import the KeyWords
from my_scopus import *
# import the requests package
import requests
# import the json to read the file
import json

# function to retrieve the information from scopus_id Abstract Retrieve Search:
# input: a specific Scopus id, can be in the form: SCOPUS_ID:XXXXXXXX, or simply XXXXXXXXXX
# output: a set that contain: Authors, KeyWords, Publication
def get_scopus_abstract_info(SCOPUS_ID):
    # this try block allow to check if there are some ValueError

    print ("Searching for " + str(SCOPUS_ID) + "...")

    # construct the right query to retrieve the information
    # specify the kind of query, see link_query_search.py
    # specific Scopus_id for research
    # option to view the result, could be also: ?field= val1, val2, ...
                                                                  # where val1, val2, ...
                                                                  # are as: authors, dc:title,....
                                                                  # see Search View Documentation
    url = (abstract_retrieval + str(SCOPUS_ID) + "?view=FULL")

    # make the http request on Scopus Abstract Retrivial link
    page_request = requests.get(url,                                    #<--- In the headers we must specify:
                    headers={'Accept':'application/json',               #    -The type of application (possible: /json, /xml, /atom+xml)
                             'X-ELS-APIKey': MY_API_KEY})               #    -The API_KEY for authentication (See Documentation MY_API_KEY)

    # read the results as json
    informations = json.loads(page_request.content.decode('utf-8'))
    # to see the varius TAG :
    "print informations"

    # select Authors
    # we must check if the tag field is empty, to avoid errors
    try:
        if informations['abstracts-retrieval-response']['authors'] is not None:
            # this field generalli containe more the one value; we need to iterate the tag in the
            # xml page to select all author
            authors = ', '.join([str(au['ce:indexed-name']) for au in informations['abstracts-retrieval-response']['authors']['author']])
            #           ^                       ^          ^                                    ^
            #           |                       |   codify always the field                     |   search for each author in authors tag
            # select separator value # select the name author tag                Acces to tag in the json loaded page
        else:
            # if is None assign this value
            authors = "NoAuthorsPresent"
    # catch all possible value
    except KeyError:
        authors = "NoAuthorsPresent"
    except ValueError:
        authors = "NoAuthorsPresent"
    except AttributeError:
        authors = "NoAuthorsPresent"
    # select the Keywords
    # as the Authors field also Keywords containe more than one value
    # Check if tag is empty

    # check if
    try:
        if informations['abstracts-retrieval-response']['authkeywords'] is not None:
            # iterate the value in this tag like as for Author tag
            keywords = ', '.join([str(keyword['$']) for keyword in informations['abstracts-retrieval-response']['authkeywords']['author-keyword']])
        else:
            # if is None assign this value
            keywords = "NoKeyWordsPresent"
    # catch all possible value
    except KeyError:
        keywords = "NoKeyWordsPresent"
    except ValueError:
        keywords = "NoKeyWordsPresent"
    except AttributeError:
        keywords = "NoKeyWordsPresent"

    # select the Journal
    # Check if is empty
    # check if prism:publicationName isn't present
    try:
        if informations['abstracts-retrieval-response']['coredata']['prism:publicationName'] is not None:
            # this value containe exactly one value, than select it
            publications = str(informations['abstracts-retrieval-response']['coredata']['prism:publicationName'])
        else:
            # there is the tag but is empty
            publications = "NoPublicationsValue"
    # catch all possible error
    except KeyError:
        publications = "NoPublicationsValue"
    except ValueError:
        publications = "NoPublicationsValue"
    except AttributeError:
        publications = "NoPublicationsValue"
    # return the output value as a string;
    # the parse to string is due to the possible presence of some character
    # that don't is correctly write in the save file
    return (str(authors) + ";op;" + str(keywords) + ";op;" + str(publications))
