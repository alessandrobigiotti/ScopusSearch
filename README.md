# Introduction

This program allows to retrieve some information about scientific papers using Scopus API. Using Scopus API we can avoid the default limitations on the number of papers or on the papers information (title, authors, affiliations, ...).

# Requiriments

To use this program we will need:
* The _Python3_ compiler version;
* The Scopus API KEY: Create a Key [here](http://dev.elsevier.com/)

# ScopusSearch

1. ScopusSearch.py: the executable 
2. link_query_search.py: a library with some possible link to Scopus API, and the headers of the http requests
3. get_info_scopus.py: an auxiliary function used by ScopuSearch.py to perform more specific query
4. my_scopus.py: your API_KEY for the authentication with Scopus API

# Run the Program

Need Python3 to work correctly.
First you need to create an API_KEY, go to Elseiver Developer Portal, and after put it in the my_scopus.py file.
Open terminal and run ScopusSearch.py

