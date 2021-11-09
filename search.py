import acronyms_reverse
from flask import redirect

from urllib.request import urlopen
import json

"""
Convert the search fields from the wtforms into an url which redirects the user to the search result page
The input search is CourseSearchForm return variable 
The return is redirect to the search result page
"""
def search_url(search):

    #Extract the specific values from the form
    tags = search.data['search']
    year = search.data['select']
    division = search.data['divisions']
    department = search.data['departments']
    campus = search.data['campuses']

    #search.data['top'] 

    #The API call is done by this url
    url = "http://127.0.0.1:5000/api/course/search?"
    many_filter = False

    #Between each different tags it is required to have an "&"
    #The values are not case sensitive but the categories (e.g. "Division=") are case sensitive
    #If no specific filters have been applied no need to include the categories in the url (same result but url look more compact this way)
    if(len(tags) > 0):
        terms = [t for t in tags.split(',')]
        print(terms)
        for i in range(len(terms)): 
            if(many_filter): url += "&"
            url += "keyword=" + terms[i]
            many_filter = True

    if(division != "Any"):
        if(many_filter): url += "&"
        url += "Division=" + acronyms_reverse.division[division]
        many_filter = True

    if(department != "Any"):
        if(many_filter): url += "&"
        url += "Department=" + acronyms_reverse.department[department]
        many_filter = True

    if(len(year) > 0):
        for i in range(len(year)): 
            if(many_filter): url += "&"
            url += "Course+Level=" + str(year[i])
            many_filter = True

    if(campus != "Any"):
        if(many_filter): url += "&"
        url += "Campus=" + acronyms_reverse.campus[campus]
        many_filter = True
    
  
    '''From the json and urllib libraries'''
    # store the response of URL
    response = urlopen(url)
    
    # storing the JSON response from url in data
    data_json = json.loads(response.read())

    return data_json