from ..model import users


def newUser(username, name, email, studentNumber, campus, division, department, year, status, startYear, gradYear, password):
    '''
    newUser creates a new user account.
    
    Params:
    - `username`: user's account username. Must be unique or the function will return False. Stores as `_id` in mongodb.
    - `name`: user's full name.
    - `email`: user's email address.
    - `studentNumber`: user's UofT student number.
    - `campus`: user's campus. (e.g. UTSG, UTM, UTSC)
    - `division`: user's division. (e.g. APSC)
    - `department`: user's department (e.g. ECE)
    - `year`: user's current year of study. Expecting a string.
    - `status`: user's status, full-time or part-time. (e.g. FT, PT)
    - `startYear`: user's starting year. Expecting an integer.
    - `gradYear`: user's expected graduation year. Expecting an integer.
    - `password`: user's password.
    
    Returns:
    - `True`: a user has been successfully added.
    - `False`: failed to add the user, an exception has occurred (e.g. non-unique username or database connection error).
    '''
    try:
        # check if "year", "startYear", and "gradYear" are passed as integers.
        if type(year) is not int:
            raise TypeError("year is expected to be an integer.")
        if type(startYear) is not int:
            raise TypeError("startYear is expected to be an integer.")
        if type(gradYear) is not int:
            raise TypeError("gradYear is expected to be an integer.")
            
        # create new user record with an empty plan
        new = {
            "_id": username,
            "name": name,
            "email": email,
            "studentNumber": studentNumber,
            "campus": campus,
            "division": division,
            "department": department,
            "year": year,
            "status": status,
            "startYear": startYear,
            "gradYear": gradYear,
            "plan": {},
            "password": password
        }

        # add year and semester to "plan" based on "startYear" and "gradYear".
        # e.g. if startYear=2021 and gradYear=2025, the following will be created:
        #   {"2021F": [], "2022W": [], "2022S": [], "2022F": [], "2023W": [], "2023S": [], "2023F": [], "2024W": [], "2024S": [], "2024F": [], "2025W": [], "2025S": []}
        for i in range(startYear, gradYear):
            new["plan"].update({str(i)+'F': [], str(i+1)+'W': [], str(i+1)+'S': []})

        # insert into mongodb
        users.insert_one(new)

    except Exception as e:
        print("newUser:", repr(e)) # non-unique username or database connection error
        return False

    return True


def getUser(username):
    '''
    getUser obtains all the information of a specific user, including user account info and plan.

    Params:
    - `username`: user's account username.

    Returns:
    - a dictionary of user's info.
    - `None` if there is no such user or an exception has occured.
    
    E.g. 
    ```
    {
        '_id': 'billgetas', 
        'name': 'Bill Getas', 
        'email': 'bill.getas@mail.utoronto.ca', 
        'studentNumber': '1234567890', 
        'campus': 'UTSG', 
        'division': 'APSC', 
        'department': 'ECE', 
        'year': 4, 
        'status': 'FT', 
        'startYear': 2020, 
        'gradYear': 2024, 
        'plan': {
            '2020F': ['APS100H1', 'APS110H1', 'APS111H1', 'CIV100H1', 'MAT186H1', 'MAT188H1'], 
            '2021W': ['APS105H1', 'APS112H1', 'APS191H1', 'ECE110H1', 'MAT187H1', 'MIE100H1'], 
            '2021S': [],
            '2021F': ['ECE201H1', 'ECE212H1', 'ECE241H1', 'ECE244H1', 'MAT290H1', 'MAT291H1'], 
            '2022W': ['ECE216H1', 'ECE221H1', 'ECE231H1', 'MUS243H1', 'ECE297'], 
            '2022S': [],
            '2022F': ['ECE302', 'ECE311', 'ECE345', 'ECE361', 'LIN101'], 
            '2023W': ['CSC384', 'ECE421', 'CSC343', 'ECE344', 'LIN102H1'], 
            '2023S': ['APS360'], '2023F': ['ECE444H1', 'ECE446H1', 'ECE344H1', 'MUS200H1'], 
            '2024W': ['ECE318H1', 'ECE528H1', 'CSC343H1', 'ECE472'], '2024S': []
        }, 
        'password': '1234'
    }
    ```
    '''
    # query by username
    query = {"_id": username}
    try:
        result = users.find_one(query) # search in mongodb, returns None if no such username
    except Exception as e:
        print("getUser:", repr(e))
        return None
    return result


def isCorrectPassword(username, password):
    '''
    isCorrectPassword checks whether the password of a user is correct.

    Params:
    - `username`: user's account username.
    - `password`: password that the client has entered.

    Returns:
    - `True`: password is correct.
    - `False`: password is incorrect or an exception has occured. 
    '''
    # create username + password query combo
    query = {"_id": username, "password": password}
    try:
        if users.find_one(query) == None: # no such combo
            return False
    except Exception as e:
        print("isCorrectPassword:", repr(e))
        return False
    return True


def getPlan(username):
    '''
    getPlan obtains the plan of a specific user.

    Params:
    - `username`: user's account username.
    
    Returns:
    - a dictionary of user's plan.
    - `None` if there is no such user or an exception has occured.

    E.g.
    ```
    {
        '2020F': ['APS100H1', 'APS110H1', 'APS111H1', 'CIV100H1', 'MAT186H1', 'MAT188H1'], 
        '2021W': ['APS105H1', 'APS112H1', 'APS191H1', 'ECE110H1', 'MAT187H1', 'MIE100H1'], 
        '2021S': [], '2021F': ['ECE201H1', 'ECE212H1', 'ECE241H1', 'ECE244H1', 'MAT290H1', 'MAT291H1'], 
        '2022W': ['ECE216H1', 'ECE221H1', 'ECE231H1', 'MUS243H1', 'ECE297'], 
        '2022S': [], 
        '2022F': ['ECE302', 'ECE311', 'ECE345', 'ECE361', 'LIN101'], 
        '2023W': ['CSC384', 'ECE421', 'CSC343', 'ECE344', 'LIN102H1'], 
        '2023S': ['APS360'], '2023F': ['ECE444H1', 'ECE446H1', 'ECE344H1', 'MUS200H1'], 
        '2024W': ['ECE318H1', 'ECE528H1', 'CSC343H1', 'ECE472'], 
        '2024S': []
    }   
    ```
    '''
    query = {"_id": username}
    project = {"_id": False, "plan": 1} # projecting only the plan field
    
    try:
        result = list(users.find(query, project)) # search in mongodb, converts cursor to list
        if not result: # result is empty
            return None
        returnDict = result[0].get("plan")

    except Exception as e:
        print("getPlan:", repr(e))
        return None

    return returnDict

def updatePlan(username, plan):
    '''
    updatePlan updates the plan of a specific user. Use `getPlan()` to ensure you start off with the correct template.

    Params:
    - `username`: user's account username.
    - `plan`: a dictionary that contains the plan we are updating to. Rejects if it's not a dictionary.
    E.g. `{'2021F': ['APS100H1'], '2022W': [], '2022S': [], '2022F': [], '2023W': [], '2023S': [], '2023F': [], '2024W': [], '2024S': [], '2024F': [], '2025W': [], '2025S': []}`

    Returns:
    - `True`: `plan` is successfully updated.
    - `False: failed to update plan due to no such user or an exception has occured.
    '''
    try:
        if type(plan) is not dict:
            raise TypeError("plan is expected to be a dictionary")

        query = {"_id": username}
        newValues = {
            "$set": {"plan": plan}
        }

        result = users.update_one(query, newValues) # update in mongodb
        if result.matched_count < 1: # cannot find matching record to upate
            return False
    except Exception as e:
        print("updatePlan:", repr(e))
        return False
    return True
