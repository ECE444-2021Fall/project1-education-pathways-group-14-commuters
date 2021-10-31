from flask import jsonify, request
from flask import Blueprint
from .db import courses

courses_bp = Blueprint('courses_dp', __name__)

@courses_bp.route('/api/course/search', methods=['GET'])
def get_courses_with_params():
    # We will implement our search and filters in such way: AND(OR(), OR()...)
    # E.g. to search for a Computer Science or Engineering course that has the keyword "software" in the course name or code:
    #       AND(OR(keyword=software), OR(department=csc, department=ece))
    # 
    # Right now you have to call the exact column name in the database because I haven't implemented acroynms like ece yet
    # TODO: implement acroynms
    # http://127.0.0.1:5000/api/course/search?keyword=software&Department=Computer+Science&Department=Edward%20S.%20Rogers%20Sr.%20Dept.%20of%20Electrical%20%26%20Computer%20Engin.
    # Query parameters:
    #   keyword: software
    #   Department: Computer+Science, Edward%20S.%20Rogers%20Sr.%20Dept.%20of%20Electrical%20%26%20Computer%20Engin.
    # Note 1: keyword searches for both Name and Code
    # Note 2: use url encoder (https://www.urlencoder.org/) to encode values with space or symbols

    dictionary = map_query_params(request.args) # map the query parameters by keys
    searchFilter = create_search_filter(dictionary) # create filter
    
    output = []
    for s in courses.find(searchFilter):
        try:
            output.append({
                'code' : s['Code'],
                'name' : s['Name'], 
                'division': s['Division'], 
                'course_description': s['Course Description'],
                'department': s['Department'],
                'prerequisites': s['Pre-requisites'],
                'course_level': s['Course Level'],
                'utsc_breadth': s['UTSC Breadth'],
                'apsc_electives': s['APSC Electives'],
                'campus': s['Campus'],
                'term': s['Term'],
                'last_updated': s['Last updated'],
                'exclusion': s['Exclusion'],
                'utm_distribution': s['UTM Distribution'],
                'corequisite': s['Corequisite'],
                'recommended_preparation': s['Recommended Preparation'],
                'arts_and_science_breadth': s['Arts and Science Breadth'],
                'arts_and_science_distribution': s['Arts and Science Distribution'],
                'fase_available': s['FASEAvailable'],
                'maybe_restricted': s['MaybeRestricted'],
                'majors_outcomes': s['MajorsOutcomes']
            })
        except KeyError: # when key does not exist in s
            return jsonify({'result' : []}), 500
    return jsonify({'result' : output}), 200

# map the query parameters by keys
def map_query_params(args):
    return dict(args.lists())

# create search filter to be passed to mongodb
def create_search_filter(dictionary):
    if not dictionary: # empty dictionary
        return {}

    searchFilter = {"$and": []} # initialize filter
    i = 0 # indexing objects inside $and 

    for key in dictionary: # iterate through each key
        for value in dictionary[key]: # iterate each value in the keys
            if key == 'keyword': # special handling for 'keyword'
                content = {"$regex": value, "$options": "i"} # content has to contain value, but doesn't have to match exactly the same
                try: # see if $or for the current key exists in the filter
                    searchFilter["$and"][i]["$or"].append({'Name': content}) # append a filter that checks whether the keyword appears in 'Name'
                    searchFilter["$and"][i]["$or"].append({'Code': content}) # append a filter that checks whether the keyword appears in 'Code'
                except IndexError: # if $or for the current key doesn't exist, append a new one
                    searchFilter["$and"].append({"$or": [{'Name': content}, {'Code': content}]})
            
            else:
                try: # see if $or for the current key exists in the filter
                    searchFilter["$and"][i]["$or"].append({key: value}) 
                except IndexError: # if $or for the current key doesn't exist, append a new one
                    searchFilter["$and"].append({"$or": [{key: value}]})
            
            #TODO: handle course level which has values of int

        i=i+1
    return searchFilter
