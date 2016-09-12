#######################################
# Created by        Alessandro Bigiotti

# import API_KEY from my_scopus file
from my_scopus import MY_API_KEY

#####################################################################################################################################
# POSSIBLE LINK FOR QUERY SEARCH
# for all possible link see the documentation: elseiver developer portal

# search from Scopus API
scopus_api_search = "http://api.elsevier.com/content/search/scopus?"

# search from ScienceDirect API
science_direct_search = "http://api.elsevier.com/content/search/scidir?"

####################################
# POSSIBLE LINK TO Scopus API

# retrieve abstract information
abstract_retrieval = "http://api.elsevier.com/content/abstract/scopus_id/"
# example: http://api.elsevier.com/content/abstract/scopus_id/xxxxxxxxxxx?field=field1,field2&apikey=xxxxxxxx

# retrieve author information
author_retrieval = "http://api.elsevier.com/content/author/author_id/"
# example: http://api.elsevier.com/content/author/author_id/xxxxxxxxxxx?field=field1,field2&apikey=xxxxxxxx

# retrieve affiliation information
affiliation_retrieval = "http://api.elsevier.com/content/affiliation/eid/"
# example: http://api.elsevier.com/content/affiliation/eid/xxxxxxxxxxx?field=field1,field2&apikey=xxxxxxxx

#####################################################################################
#POSSIBLE LINK TO Science Direct API

#link to retrieve article information by pii
article_retrieve_by_pii = "http://api.elsevier.com/content/article/pii/"

# link to retrieve article recommended information by pii
article_recommendation_by_pii = "http://api.elsevier.com/content/article/recommendation/pii/"

################################################################################
# HEADERS OF THE QUERY

headers = dict()
headers['X-ELS-APIKey'] = MY_API_KEY  # your API_KEY
headers['X-ELS-ResourceVersion'] = 'XOCS'  # response type
headers['Accept'] = 'application/json'    # application type
