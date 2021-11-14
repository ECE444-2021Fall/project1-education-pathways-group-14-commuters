from . import main
from .forms import CourseSearchForm
from flask import render_template, request, redirect, session, flash
from .search import search_url
import pandas as pd

"""Homepage is essentially just the course search form. If a post request is received, call the method that finds search results."""
@main.route('/',methods=['GET'])
def home():
    return render_template('index.html')


"""Course search form. If a post request is received, call the method that finds search results."""
@main.route('/find',methods=['GET','POST'])
def search():
    search = CourseSearchForm(request.form)
    if request.method == 'POST':
        return search_results(search)
    return render_template('search.html',form=search)

"""Handle the data from the POST request that will go to the main algorithm.
If we get an empty search, just go back to home.
Otherwise, pull out the elements of the POST request that are used by the algorithm, and get the results.
Then, render the results page with a list of pandas tables containing the results for each year.
Pass the original search to the template as well, so the user can see the context of what they asked for.
"""
@main.route('/results')
def search_results(search):
    data = search_url(search)
        
    df = pd.json_normalize(data['result'])

    if search != None:
        df = df.head(int(search.data['top']))
    
    if len(df):
        df = df[["course_level", "code", "department", "name", "division", "course_description", "campus"]]
        df = df.rename(columns={"course_level":"Level", "code":"Code", "department":"Departement", "name":"Course Name", "division":"Division", "course_description":"Course Description", "campus":"Campus"})
        for i in range(len(df)):
            df["Code"][i] = '<a href="/course/%s" target="_blank"> %s <a>' %(df["Code"][i], df["Code"][i])
        df = [df]
    else: df = []

    return render_template('results.html',tables=[t.to_html(classes='data table table-light table-striped table-hover table-bordered',index=False,na_rep='',render_links=True, escape=False) for t in df],form=search)

"""
This method shows the information about a single course.
First, some basic error handling for if a course is passed that does not exist.
Then, separate the course information into the elements which have specific display functionality and the rest, which we show in a big table.
Pass all that to render template.
"""
@main.route('/course/<code>')
def course(code):

    data = search_url(code=code)

    df = pd.json_normalize(data['result'])

    #Since the calls are made for course that do exist in the database this should not happen
    #However, if user brute force by typing his own link he will be redirect to home directory to not make page crash
    if len(df) == 0:
        return redirect('/')
        
    course = df

    #use course network graph to identify pre and post requisites
    pre = course['prerequisites']
    #post = G.out_edges(code)

    excl = course['exclusion'][0]
    coreq = course['corequisite'][0]
    aiprereq = course['ai_pre_reqs'][0]
    majors = course['majors_outcomes'][0]
    minors = course['minors_outcomes'][0]
    faseavailable = course['fase_available'][0]
    mayberestricted = course['maybe_restricted'][0]
    terms = course['term'][0]
    activities = course['activity'][0]

    course = df[["division", "course_description", "department", "course_level",  "campus", "code", "name"]]
    course = course.rename(columns={"course_level":"Course Level", "code":"Code", "department":"Department", "name":"Course Name", "division":"Division", "course_description":"Course Description", "campus":"Campus"})
    course = course.iloc[0]

    return render_template(
        'course.html',
        course=course,
        pre=pre, 
        #post=post,
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

@main.route('/login', methods=['GET', 'POST'])
def login():

    #When submit button is pressed
    if request.method == 'POST':

        #Verify that username and password match the required values
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            #Flash login error
            flash('Invalid Credentials. Please try again.',"danger")

        else:
            #Login sucessful
            #Set session variable to use for access 
            session['username'] = request.form['username']
            #Flash success message
            flash('You were successfully logged in.',"success")

    return render_template('login.html')


"""
Method to Logout User
"""
@main.route('/logout')
def logout():
    #If user logs out, delete session username variable
    session.pop('username', None)

    return render_template('index.html')


"""
Method to View User Timetable
"""
@main.route('/plan')
def planner():

    #If user tries to access planner without logging in
    #Redirect to Login Page
    if 'username' not in session or session['username'] is None:
        flash('Login to view profile.',"warning")

        return redirect('/login')

    #Get session user name
    user = session['username']
    
    #Open Planner page using user 
    #return(render_template('planner.html', user=user))

    #testing --------------
    test_data=[["2017F","2017S","2018F","2018S"],["ECE444","ECE454","",""]]
    test_df = pd.DataFrame(test_data, columns=["2017F","2017W","2018F","2018W"])
    print(test_df)
    test_df=[test_df]
    print(test_df)
    return(render_template('planner.html',tables=[t.to_html(classes='data table table-light table-hover table-bordered',index=False,na_rep='',render_links=True, escape=False) for t in test_df], user=user))