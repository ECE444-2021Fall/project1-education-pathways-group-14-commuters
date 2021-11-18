# Planner & Exploration Tool (PET)

## 🖥 About PET
The objective of this project is to create a system that enables efficient course planning for all University
of Toronto students by having the planning and selection tools in one place. This will be achieved by
ensuring the system includes functions that improve user experience. The primary benefit of the design
is that it saves the students’ time to do course planning without having to navigate multiple websites.

## ⚙ Project Management Tools 
Trello: https://trello.com/b/aeajEIoi/main

## 📚 Tech Stack
- Python
- Flask
- JavaScript

## 🏃‍♂️ Getting Started
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

## 🎖 Acknowledgements
This project is built upon https://github.com/nelaturuk/education_pathways, a tool published by the Centre for Analytics and Artificial Intelligence Engineering (CARTE) at the University of Toronto. 

## :file_folder: Folder Structure
```
project1-education-pathway-group-14-commuters
│   .flaskenv
|   .gitignore
│   CONTRIBUTION.md
│   Dockerfile
|   Procfile
│   README.md
│   environment.yml
│   requirements.txt
│   run.py   
│
└───app
│   │   __init__.py
│   │   model.py
│   │
│   └───database
│       │   __init__.py
│       │   acronyms.py
│       │   acronyms_reverse.py
│       │   course_choices.py
│       │   courses.py
│       │   users.py
│       └───
│   └───main
│       │   __init__.py
│       │   forms.py
│       │   search.py
│       │   views.py
│       └───
│   └───static
│       │   base_template.html
│       │   course.html
│       │   edit.html
│       │   index.html
│       │   login.html
│       │   ...
│       └───
│   └───templates
│       │   __init__.py
│       │   forms.py
│       │   search.py
│       │   views.py
│       └───
└───config
│   │   __init__.py
│   │   app_config.py
│   │   db_config.py
│   └───
└───constants
│   │   __init__.py
│   │   local_run.py
│   └───
└───test
│   │   __init__.py
│   │   test_client
│   │   test_basic
│   │   ...
│   └───
└───
```