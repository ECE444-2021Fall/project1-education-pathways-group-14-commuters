# Planner & Exploration Tool (PET)

## π₯ About PET
The objective of this project is to create a system that enables efficient course planning for all University
of Toronto students by having the planning and selection tools in one place. This will be achieved by
ensuring the system includes functions that improve user experience. The primary benefit of the design
is that it saves the studentsβ time to do course planning without having to navigate multiple websites.

## β Project Management Tools 
Trello: https://trello.com/b/aeajEIoi/main

## π Tech Stack
- Python
- Flask
- JavaScript

## πββοΈ Getting Started
### Prerequisites
- Docker: If you haven't yet, please download and install Docker here: https://docs.docker.com/get-docker/

### Install and run PET 
1. Clone this repository
```
git clone https://github.com/ECE444-2021Fall/project1-education-pathways-group-14-commuters.git
```
2. Build docker image (anticipated version v1.0.0)
```docker
docker build --network=host -t python-docker .
```
3. Run docker image on localhost (anticipated version v1.0.0)
```
docker run -d -p 5000:5000 python-docker 
```

## π Acknowledgements
This project is built upon https://github.com/nelaturuk/education_pathways, a tool published by the Centre for Analytics and Artificial Intelligence Engineering (CARTE) at the University of Toronto. 

## :file_folder: Folder Structure
```
project1-education-pathway-group-14-commuters
β   .flaskenv
|   .gitignore
β   CONTRIBUTION.md
β   Dockerfile
|   Procfile
β   README.md
β   environment.yml
β   requirements.txt
β   run.py   
β
ββββapp
β   β   __init__.py
β   β   model.py
β   β
β   ββββdatabase
β       β   __init__.py
β       β   acronyms.py
β       β   acronyms_reverse.py
β       β   course_choices.py
β       β   courses.py
β       β   users.py
β       ββββ
β   ββββmain
β       β   __init__.py
β       β   forms.py
β       β   search.py
β       β   views.py
β       ββββ
β   ββββstatic
β       β   base_template.html
β       β   course.html
β       β   edit.html
β       β   index.html
β       β   login.html
β       β   ...
β       ββββ
β   ββββtemplates
β       β   __init__.py
β       β   forms.py
β       β   search.py
β       β   views.py
β       ββββ
ββββconfig
β   β   __init__.py
β   β   app_config.py
β   β   db_config.py
β   ββββ
ββββconstants
β   β   __init__.py
β   β   local_run.py
β   ββββ
ββββtest
β   β   __init__.py
β   β   test_client
β   β   test_basic
β   β   ...
β   ββββ
ββββ
```