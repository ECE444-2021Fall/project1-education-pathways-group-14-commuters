from . import main
from .forms import CourseSearchForm
from ..model import G, courses
from flask import render_template, request, redirect
from .search import filter_courses
import pandas as pd

"""Homepage is essentially just the course search form. If a post request is received, call the method that finds search results."""
@main.route('/',methods=['GET','POST'])
def home():
    search = CourseSearchForm(request.form)
    if request.method == 'POST':
        return search_results(search)
    return render_template('index.html',form=search)

"""Handle the data from the POST request that will go to the main algorithm.
If we get an empty search, just go back to home.
Otherwise, pull out the elements of the POST request that are used by the algorithm, and get the results.
Then, render the results page with a list of pandas tables containing the results for each year.
Pass the original search to the template as well, so the user can see the context of what they asked for.
"""
@main.route('/results')
def search_results(search):
    if search.data['search'] == '' or not search.data['search']:
        return redirect('/')
    results = filter_courses(
        search.data['search'],
        search.data['select'],
        search.data['divisions'],
        search.data['departments'],
        search.data['campuses'],
        search.data['top']
        )

    return render_template('results.html',tables=[t.to_html(classes='data',index=False,na_rep='',render_links=True, escape=False) for t in results],form=search)

"""
This method shows the information about a single course.
First, some basic error handling for if a course is passed that does not exist.
Then, separate the course information into the elements which have specific display functionality and the rest, which we show in a big table.
Pass all that to render template.
"""
@main.route('/course/<code>')
def course(code):

    #If the course code is not present in the dataset, progressively remove the last character until we get a match.
    #For example, if there is no CSC413 then we find the first match that is CSC41.
    #If there are no matches for any character, just go home.

    course_code = []
    
    for index in courses.find({}, {'Code': True}):
        course_code.append(index["Code"])

    course_code = pd.DataFrame(course_code)
    course_code.columns=['Code']


    if code not in course_code['Code'].values:
        while True:
            code = code[:-1]

            if len(code) == 0:
                return redirect('/')

            t = course_code[course_code['Code'].str.contains(code)]

            if len(t) > 0:
                code = t['Code'].values[0]
                return redirect('/course/' + code)

    course = courses.find({'Code': code}, {'_id': False})[0]
    # print(courses.find({'Code': code}, {'_id': False})[0])
    #use course network graph to identify pre and post requisites
    pre = G.in_edges(code)
    post = G.out_edges(code)
    excl = course['Exclusion']
    coreq = course['Corequisite']
    aiprereq = course['AIPreReqs']
    majors = course['MajorsOutcomes']
    minors = course['MinorsOutcomes']
    faseavailable = course['FASEAvailable']
    mayberestricted = course['MaybeRestricted']
    terms = course['Term']
    activities = course['Activity']
    course = {k:v for k,v in course.items() if k not in ['Course','Course Level Number','FASEAvailable','MaybeRestricted','URL','Pre-requisites','Exclusion','Corequisite','Recommended Preparation','AIPreReqs','MajorsOutcomes','MinorsOutcomes','Term','Activity'] and v==v}
    return render_template(
        'course.html',
        course=course,
        pre=pre, 
        post=post,
        excl=excl,
        coreq=coreq,
        aip=aiprereq,
        majors=majors,
        minors=minors,
        faseavailable=faseavailable,
        mayberestricted=mayberestricted,
        terms=terms,
        activities=activities,
        zip=zip
        )
