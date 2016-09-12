#######################################
# Created by        Alessandro Bigiotti

# import the query link
from link_query_search import *
# import the API_KEY file
from my_scopus import *
# import the requests package to make the query
import requests
# import the json to read the query response
import json

# function to retrieve the information about a paper, selected by the scopus_id
# input: a specific Scopus id, can be in the form: SCOPUS_ID:XXXXXXXX, or simply XXXXXXXXXX
# output: a set that contain: Authors, KeyWords, Publication
def get_scopus_abstract_info(SCOPUS_ID):
    # print the scopus_id of the paper
    print ("Searching for " + str(SCOPUS_ID) + "...")

    # construct the query to retrieve the information
    url = (abstract_retrieval # see link_query_search
          + SCOPUS_ID         # specific Paper ID
          + "?view=FULL")     # information to view (there are some restrictions)

    # make the http request on Scopus Abstract Retrivial link
    page_request = requests.get(url,                       # The query previously constructed
                    headers={'Accept':'application/json',  # The type of application (possible: /json, /xml, /atom+xml)
                             'X-ELS-APIKey': MY_API_KEY})  # The API_KEY for authentication
                                                           # (See Documentation Elseiver Developer Portal: MY_API_KEY)

    # read the results as json
    informations = json.loads(page_request.content.decode('utf-8'))
    # to see the various TAG :
    "print informations"

    # select Authors informations
    try:      # maybe there is some empty field
        # check if the tag is empty
        if informations['abstracts-retrieval-response']['authors'] is not None:
            # select the value indicated by the tag: 'ce:indexed-name'
            authors = ', '.join([au['ce:indexed-name'].encode("utf-8") for au in informations['abstracts-retrieval-response']['authors']['author']])
        else:
            # if is None assign this value
            authors = "NoAuthorsPresent"
    # catch some possible Error
    except KeyError:
        authors = "NoAuthorsPresent"
    except ValueError:
        authors = "NoAuthorsPresent"
    except AttributeError:
        authors = "NoAuthorsPresent"


    # select Keywords informations
    try:     # maybe there is some empty field
        # check if the tag is empty
        if informations['abstracts-retrieval-response']['authkeywords'] is not None:
            # select the value indicated by the tag: '$'
            keywords = ', '.join([keyword['$'].encode("utf-8") for keyword in informations['abstracts-retrieval-response']['authkeywords']['author-keyword']])
        else:
            # if is None assign this value
            keywords = "NoKeyWordsPresent"
    # catch some possible value
    except KeyError:
        keywords = "NoKeyWordsPresent"
    except ValueError:
        keywords = "NoKeyWordsPresent"
    except AttributeError:
        keywords = "NoKeyWordsPresent"

    # select Journal information
    try:     # maybe there is some empty field
        if informations['abstracts-retrieval-response']['coredata']['prism:publicationName'] is not None:
            # select the value indicated by the tag: 'prosm:publicationName'
            publications = informations['abstracts-retrieval-response']['coredata']['prism:publicationName'].encode("utf-8")
        else:
            # if is None assign this value
            publications = "NoPublicationsValue"
    # catch some possible error
    except KeyError:
        publications = "NoPublicationsValue"
    except ValueError:
        publications = "NoPublicationsValue"
    except AttributeError:
        publications = "NoPublicationsValue"

    # return the values as a string;
    return (str(authors) + ";" + str(keywords) + ";" + str(publications))
