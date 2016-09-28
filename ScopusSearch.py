#######################################
# PYTHON SCOPUS DATA RETRIEVE PROGRAM
# Created by        Alessandro Bigiotti Matr 281812
# Using the Scopus API we can download the data with an http request

# This program allow to create a text file
# that containe some field about some publications
# obtained with a specific query from Scopus Database


import os
# package JSON to read and manage the response
import json
# package REQUEST to make the http request
import requests

# create a file named my_scopus.py in the same folder where is the python PROGRAM
# put the api_key into a variable MY_API_KEY = 'xxxxxxxxxxxxxx'
# than import the variable from the file
# it need to authenticate your organization for the query
from my_scopus import MY_API_KEY

# link_query_search containe all possible query syntax
from link_query_search import *
# get_info_scopus containe a function to make more specific query
# and retrieve the right informations like: Authors list, Keywords list, Journals
from get_info_scopus import *
# get_affiliation_info check if the affiliation may be are in an other page
from get_affiliation_info import *



###############################################################################
# create the file to write the results
# path to save results file
path = os.path.dirname(os.path.abspath(__file__))
savefile = path + "/Scopus_Data.txt"

# open file to write results
info_file = open(savefile, "w")
# write the title of each "column"
info_file.write("AUTHORS; KEYWORDS; PUBLICATION; TITLE; AFFILIATION; SCOPUS_ID; EID \n")





###############################################################################
# request query from input
# must be in the form: query=KEY(complexity) or query=AUTH(Milani) AND ...
print ("Scrivi la query per la ricerca ScopusSearch: \n Es: query=KEY(complexity)")
# read the input into the query
query = input(" \n")


################################################################################
# MAKE HTTP REQUEST

# retrieve the first page of the search
page_request = requests.get(scopus_api_search +               query, headers=headers)
#                   ^                   ^                       ^             ^
#                   |                   |                       |             |
#    from package requests    see link_query_search.py      the quey    authentication api_key, see link_query_search.py

###############################################################################
# READ THE RESPONSE
# read the page response as JSON
page = json.loads(page_request.content.decode("utf-8"))


# with JSON reader, we can match the xml tag as object['xml-tag']
# hence we first select the page['search-results'],
# ['opensearch:totalResults'] tag containe the number of searched papers

# count the result items
number_item = int(page['search-results']['opensearch:totalResults'])
print ("numero di elementi ottenuti:" + str(number_item))




###############################################################################
# request the publication index, to start the download
# insert a number > 0 e < number-item
# START TO READ THE PAGE, FOR EACH PAPER WE HAVE TO RETRIEVE THE RIGHT INFORMATION
# SET THE INITIAL VALUE OF:
#   count -> the number of item that are viewed
#   i -> counter for the FOR cicle
#   download -> counter the number of article downloaded
i=0; count = 25; download = 0
#   start -> the index of the first item
# read from keyboard the paper index to download, it must be cast to INT
start = int(input("Inserisci l'indice dell'articolo da scaricare; valori: (0, " + str(number_item) + ") \n"))

# iter the paper in the page viewed
for i in range(0, number_item, count):

    # in each page we can view 25 papers, its are indicated by count
    # hence we have to iter all the pages, in this way we don't excede the maximum
    # number of article response
    page_request = requests.get(scopus_api_search + "&start=" + str(start) + "&count="+ str(count)
    #                               ^                       ^                           ^
    #                               |                       |                           |
    #                     kind of api search    index for iter pages     number of papers to view in each page
    + "&" + query + "&apikey=" + MY_API_KEY)
    #           ^                   ^
    #           |                   |
    #       the query         your api_key



    # read the page as JSON
    page = json.loads(page_request.content.decode("utf-8"))
    # "print page" #to see the json file structures

    # ['entry'] tag containe some basic information about the paper
    # as an example: creator, link to scopus_id_paper_page, link_to_author_affiliation, eid, title, ....
    try:
        if page['search-results']['entry'] is not None:
            article_list = page['search-results']['entry']
        else:
            print ("Not Article")
    except KeyError:
        print ("not page found")

    # to retrieve all the interested information, first we have to read the
    # scopusid, eid or doi,... to operate a more specific search
    for article in article_list:
        # update the paper download number
        download = download + 1
        try:
            # get title
            if article['dc:title'] is not None:
                title = article['dc:title'].encode('utf-8')
            else:
                title = "NoTitlePresent"
        # catch this kind of possible error
        except KeyError:
            title = "NoTitlePresent"
        except AttributeError:
            title = "NoTitlePresent"
        except ValueError:
            title = "NoTitlePresent"
        try:
            if article['dc:identifier'] is not None:
                # get ScopusID for more specific information
                scopusID = str(article['dc:identifier'])
            else:
                scopusID = "NoScopusIDPresent"
        # catch this kind of possible error
        except KeyError:
            scopusID = "NoScopusIDPresent"
        except AttributeError:
            scopusID = "NoScopusIDPresent"
        except ValueError:
            scopusID = "NoScopusIDPresent"
        try:
            if article['eid'] is not None:
                # get EID for affiliation retrieval
                EID = str(article['eid'])
            else:
                EID = "NoEIDPresent"
        # catch this kind of possible error
        except KeyError:
            EID = "NoEIDPresent"
        except AttributeError:
            EID = "NoEIDPresent"
        except ValueError:
            EID = "NoEIDPresent"
        # for the affiliation field we need to use a try catch
        # because the field could be not present in the page
        try:
            # select affifliation
            for aff in article['affiliation']:

                # check if the affilname is empty
                if aff['affilname'] is not None:
                    affiliation = ', '.join([ str(aff['affilname']) for aff in article['affiliation'] ])
                # if have not encode maethod, it is already a string
                else:
                    # there is the tag, but is empty
                    affiliation = "NoAffiliationPresent"

        except AttributeError:
            affiliation = "NoAffiliationPresent"
        except KeyError:
            # if cathc this error there isn't an affiliation value
            affiliation = "NoAffiliationPresent"
        except ValueError:
            affiliation = "NoAffiliationPresent"

        # call function to retrieve author, title, and keywords of the paper specify by scopusID
        info_scopus = get_scopus_abstract_info(scopusID)

        # write the results in the output file, with right formattation
        info_file.write(str(info_scopus) + ";op;" + str(title) + ";op;" + str(affiliation) + ";op;" + str(scopusID) + ";op;" + str(EID) + "\n")

    # updaiting ciclo for value
    i = i + count
    # item page indexes
    start = start + count
    # feedback on the last paper downloaded
    print ("the number of paper already downloaded is: " + str(download))

# close the reader file
info_file.close()
# feedback on the download termination
print ("Download Completed!! ")
print ("Total Number of download:" + str(download))
