from ..database import acronyms_reverse
from urllib.request import urlopen
import json

"""
Convert the search fields from the wtforms or a course code into an API call and returns a JSON with the courses it found
The input search is CourseSearchForm return variable or a course code 
If both inputs are used in a call only the function will prioritize the search form results rather than the course code
If no inputs are given it will return a list of all the course in the database
The return value is JSON file containing the results of the API call
"""
def search_url(search=None, code=None):

    #The API call is done by this url
    url = "https://planning-and-exploration.herokuapp.com/api/course/search?"
    many_filter = False

    #Between each different tags it is required to have an "&"
    #The values are not case sensitive but the categories (e.g. "Division=") are case sensitive
    #If no specific filters have been applied no need to include the categories in the url (same result but url look more compact this way)
    if search != None:
        
        #Extract the specific values from the form
        tags = search.data['search']
        year = search.data['select']
        division = search.data['divisions']
        department = search.data['departments']
        campus = search.data['campuses']

        if(len(tags) > 0):
            terms = [t for t in tags.split(',')]

            #The user may input several keyword
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
            #Similar to the tags the user may select multiple years
            for i in range(len(year)): 
                if(many_filter): url += "&"
                url += "Course+Level=" + str(year[i])
                many_filter = True

        if(campus != "Any"):
            if(many_filter): url += "&"
            url += "Campus=" + acronyms_reverse.campus[campus]
            many_filter = True
    elif code != None:
        url += "Code=" + str(code)
        
    '''From the json and urllib libraries'''
    # store the response of URL
    response = urlopen(url)
    
    # storing the JSON response from url in data
    data_json = json.loads(response.read())

    return data_json