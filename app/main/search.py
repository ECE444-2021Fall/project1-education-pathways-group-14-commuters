import numpy as np
from collections import defaultdict
from sklearn.metrics.pairwise import cosine_similarity
from ..model import df, course_vectors, vectorizer
"""
Main algorithm for searching courses. 
In a nutshell: 
1. Split search into phrases e.g. machine learning, biology ==> ['machine learning','biology']
2. Find phrases that occur in the vectorizer (if none, give up). 
3. Find all courses with a nonzero value for each term, and compare all courses against the set of courses with that non-zero value.
4. For every course that is listed as a pre-requisite, add the relevance of its referrer to a list.
5. Take the average of that list and assign it to the pre-requisite.
6. Get the course data for relevant courses in order of score.

"""
def filter_courses(pos_terms, year, division, department, campus, n_return=10):
    print(pos_terms,year)
    n_return=int(n_return) #How many courses are we sending back
    year = int(year) #What year are we primarily looking for
    pos_vals = np.zeros((len(df),))

    #1. Split search into phrases e.g. machine learning, biology ==> ['machine learning','biology']
    #2. Find phrases that occur in the vectorizer (if none, give up). 
    terms = [t for t in pos_terms.split(',') if t.strip() in vectorizer.get_feature_names()]
    print(terms)
    if len(terms) == 0:
        return []
    
    #3. Find all courses with a nonzero value for each term, and compare all courses against the set of courses with that non-zero value.
    #To explain, for each term we look for similarity with all the terms that co-occur with it, to give us a wider scope.
    for term in terms:
        idx = vectorizer.transform([term.strip()]).nonzero()[1][0]
        relevants = course_vectors[:,idx].nonzero()[0]
        pos_vals += np.mean(cosine_similarity(course_vectors,course_vectors[relevants,:]),axis=1)

    #4. For every course that is listed as a pre-requisite, add the relevance of its referrer to a list.
    requisite_vals = defaultdict(list)
    for (k,v),i in zip(df.iterrows(),list(pos_vals)):
        if i>100:
            break
        for col in ['Pre-requisites','Recommended Preparation']:
            for c in v[col]:
                if c in df.index:
                    requisite_vals[c].append(i)

    #5. Take the average of that list and assign it to the pre-requisite.
    for (k,v) in requisite_vals.items():
        requisite_vals[k] = np.mean(v)

    #6. Get the course data for relevant courses in order of score.
    idxs = [t[1] for t in sorted(list(zip(list(pos_vals),list(df.index))),key=lambda x:x[0],reverse=True)]
    tf = df.loc[idxs]

    #7. Separate results by year, starting with the table for the year actually searched for and then decreasing by year. Apply any filters now.
    main_table = tf[tf['Course Level'] == year]
    for name,filter in [('Division',division), ('Department',department), ('Campus',campus)]:
        if filter != 'Any':
            main_table = main_table[main_table[name] == filter]
    tables = [main_table[0:n_return][['Course','Name','Division','Course Description','Department','Course Level']]]
    year -= 1
    while(year > 0):
        tf = df.loc[[t[0] for t in sorted(requisite_vals.items(),key=lambda x: x[1],reverse=True)]]
        tf = tf[tf['Course Level'] == year]
        for name,filter in [('Division',division), ('Department',department), ('Campus',campus)]:
            if filter != 'Any':
                tf = tf[tf[name] == filter]
        tables.append(tf[0:n_return][['Course','Name','Division','Course Description','Department','Course Level']])
        year -= 1
    return tables