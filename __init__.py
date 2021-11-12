import os
import pickle
import numpy as np
import pandas as pd
import networkx as nx
from collections import defaultdict
from scipy.sparse import load_npz
from sklearn.metrics.pairwise import cosine_similarity
from flask import Flask, render_template, request, redirect, session, flash
from wtforms import Form, StringField, SelectField, SelectMultipleField
from wtforms.widgets import ListWidget, CheckboxInput
from wtforms.widgets.core import Select, TableWidget
from search import *

'''wtforms method to have a MultiCheckboxField returning an array of selected values (may be empty)'''
class MultiCheckboxField(SelectMultipleField):
    widget = TableWidget(with_table_tag=False)
    option_widget = CheckboxInput()

from flask_pymongo import PyMongo

"""Build the search form, including dropdown menus at the top of the page, from the main datafile."""
class CourseSearchForm(Form):
    df = pd.read_pickle('resources/df_processed.pickle').set_index('Code')
    divisions = [('Any','Any')] + sorted([
        (t,t) for t in set(df.Division.values)
    ])

    departments = [('Any','Any')] + sorted([
        (t,t) for t in set(df.Department.values)
    ])

    campus = [('Any','Any')] + sorted([
        (t,t) for t in set(df.Campus.values)
    ])

    year_choices = [
        (t,t) for t in set(df['Course Level'].values)
    ]
            
    top = [
        ('10','10'),
        ('25','25'),
        ('50','50')
    ]
    select = MultiCheckboxField('Course Year(s)', choices=year_choices)
    top = SelectField('Show Top',choices=top)
    divisions = SelectField('Division', choices=divisions)
    departments = SelectField('Department', choices=departments)
    campuses = SelectField('Campus', choices=campus)
    search = StringField('Search Term(s)', render_kw={"placeholder": "Search Terms"})


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config['SECRET_KEY'] = 'secret'

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    """Homepage is essentially just the course search form. If a post request is received, call the method that finds search results."""
    @app.route('/',methods=['GET'])
    def home():
        return render_template('index.html')


    """Course search form. If a post request is received, call the method that finds search results."""
    @app.route('/find',methods=['GET','POST'])
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
    @app.route('/results')
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
    @app.route('/course/<code>')
    def course(code):

        data = search_url(code=code)

        df = pd.json_normalize(data['result'])

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

        #course = {k:v for k,v in course.items() if k not in ['name','code','fase_available','maybe_restricted','prerequisites','exclusion','corequisite','recommended_preparation', 'majors_outcomes', 'term'] and v==v}
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


    """
    Method to Manage User Login
    """
    @app.route('/login', methods=['GET', 'POST'])
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
    @app.route('/logout')
    def logout():
        #If user logs out, delete session username variable
        session.pop('username', None)

        return render_template('index.html')


    """
    Method to View User Timetable
    """
    @app.route('/plan')
    def planner():

        #If user tries to access planner without logging in
        #Redirect to Login Page
        if 'username' not in session or session['username'] is None:
            flash('Login to view profile.',"warning")

            return redirect('/login')

        #Get session user name
        user = session['username']
        
        #Open Planner page using user 
        return(render_template('planner.html', user=user))


    return app

with open('resources/course_vectorizer.pickle','rb') as f:
    vectorizer = pickle.load(f)
with open('resources/course_vectors.npz','rb') as f:
    course_vectors = pickle.load(f)
with open('resources/graph.pickle','rb') as f:
    G = nx.read_gpickle(f)
df = pd.read_pickle('resources/df_processed.pickle').set_index('Code')
app = create_app()

with app.app_context():  
    from database.courses import courses_bp
    app.register_blueprint(courses_bp)

if __name__=="__main__":
    app.run(host='0.0.0.0')
