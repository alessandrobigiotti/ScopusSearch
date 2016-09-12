#######################################
# PYTHON SCOPUS DATA RETRIEVE PROGRAM
# Created by        Alessandro Bigiotti
# Using the Scopus API we can download the data with an http request

# This program allow to create a text file
# that containe informations about some publications
# obtained with a specific query from Scopus Database
import os
import sys
# package JSON to read and manage the response
import json
# package REQUEST to make the http request
import requests

# The file my_scopus.py containe the api_key
# into a variable MY_API_KEY = 'xxxxxxxxxxxxxx'
from my_scopus import MY_API_KEY

# The file link_query_search containe some possible query syntax and the headers
from link_query_search import *
# get_info_scopus containe a function to make more specific query
from get_info_scopus import *

###############################################################################
# create the file to write the results
path = os.path.dirname(os.path.abspath(__file__))
savefile = path + "/Scopus_Data.txt"

# open the file to write results
info_file = open(savefile, "w")
# write the title of each "column"
info_file.write("AUTHORS; KEYWORDS; PUBLICATION; TITLE; AFFILIATION; SCOPUS_ID; EID \n")

###############################################################################
# request query from input (See Documentation Elseiver Developer Portal)
# must be in the form: query=KEY(complexity) or query=AUTH(Milani) AND ...
print ("Scrivi la query per la ricerca di Scopus \n")
print ("Es: query=KEY(complexity) \n")
# read the input into the query variable
query = input()

################################################################################
# MAKE HTTP REQUEST
# retrieve the first page of the search
page_request = requests.get(scopus_api_search + query, headers=headers)

###############################################################################
# READ THE RESPONSE
# read the page response as JSON
page = json.loads(page_request.content.decode("utf-8"))

# with JSON reader, we can match the xml tag as object['xml-tag']
# hence we first select the page['search-results'],
# ['opensearch:totalResults'] tag containe the number of papers found

# count the items found
number_item = int(page['search-results']['opensearch:totalResults'])

###############################################################################
# ITER THE PAGES

# some counter
i=0; count = 25; download = 0

# read from keyboard the paper index to download, it must be cast to INT
start = int(raw_input("Inserisci l'indice dell'articolo da scaricare; valori: (0, " + str(number_item) + ") \n"))

# iter the page in the search results
for i in range(0, number_item, count):

    # in each page we can view 25 papers, its are indicated by count
    # hence we have to iter all the pages, in this way we don't excede the maximum
    # number of article response
    page_request = requests.get(scopus_api_search + "&start=" + str(start) + "&count="+ str(count) + "&" + query + "&apikey=" + MY_API_KEY)

    # read the page as JSON
    page = json.loads(page_request.content.decode("utf-8"))
    "print page" #to see the json file structures

    # ['entry'] tag containe some basic information about the paper
    # as an example: creator, link to scopus_id_paper_page, link_to_author_affiliation, eid, title, ....
    try:
        # check if the page is empty
        if page['search-results']['entry'] is not None:
            # save the list of paper in the current page
            article_list = page['search-results']['entry']
        else:
            print ("Not Article")
    except KeyError:
        print ("not page found")

    # to retrieve all the interested information, first we have to read the
    # scopusid, eid or doi,... to operate a more specific search
    # iter the paper in the page
    for article in article_list:
        # update the paper download number
        download = download + 1
        try:
            # get title
            if article['dc:title'] is not None:
                title = article['dc:title'].encode('utf-8')
            else:
                title = "NoTitlePresent"
        # catch some possible error
        except KeyError:
            title = "NoTitlePresent"
        except AttributeError:
            title = "NoTitlePresent"
        except ValueError:
            title = "NoTitlePresent"

        try:
            # get scopus_id
            if article['dc:identifier'] is not None:
                # get ScopusID for more specific query
                scopusID = article['dc:identifier'].encode("utf-8")
            else:
                scopusID = "NoScopusIDPresent"
        # catch some possible error
        except KeyError:
            scopusID = "NoScopusIDPresent"
        except AttributeError:
            scopusID = "NoScopusIDPresent"
        except ValueError:
            scopusID = "NoScopusIDPresent"

        try:
            # get the EID
            if article['eid'] is not None:
                # get EID for affiliation retrieval
                EID = article['eid'].encode("utf-8")
            else:
                EID = "NoEIDPresent"
        # catch some possible error
        except KeyError:
            EID = "NoEIDPresent"
        except AttributeError:
            EID = "NoEIDPresent"
        except ValueError:
            EID = "NoEIDPresent"

        try:
            # get the affifliations
            for aff in article['affiliation']:
                # check if the aff['affilname'] have the .encode(utf-8) method
                try:
                    # check if the affilname is empty
                    if aff['affilname'] is not None:
                        affiliation = ', '.join([ aff['affilname'].encode("utf-8") for aff in article['affiliation'] ])
                    # if have not encode maethod, it is already a string
                    else:
                        # there is the tag, but is empty
                        affiliation = "NoAffiliationPresent"
                # capture the error due to unicode method
                except AttributeError:
                    # then cast the value to string and continue
                    affiliation = ', '.join([ str(aff['affilname']) for aff in article['affiliation'] ])
        # check some possible error
        except KeyError:
                affiliation = "NoAffiliationPresent"
        except ValueError:
                affiliation = "NoAffiliationPresent"
        except AttributeError:
                affiliation = "NoAffiliationPresent"
        # call function to retrieve author, title, and keywords of the paper specify by scopusID
        info_scopus = get_scopus_abstract_info(scopusID)

        # write the results in the output file
        info_file.write(info_scopus + ";" + title + ";" + str(affiliation) + ";" + str(scopusID) + ";" + str(EID) + "\n")

    # update for cicle values
    i = i + count
    start = start + count
    # feedback on the last paper downloaded
    print ("the number of paper already downloaded is: " + str(download))

# close the reader file
info_file.close()
# feedback on the download completed
print ("Download Completed!! ")
print ("Total Number of download:" + str(download))
