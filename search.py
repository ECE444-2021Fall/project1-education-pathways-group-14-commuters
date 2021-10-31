import acronyms_reverse

def search_url(tags, year, division, department, campus):

    url = "/api/course/search?"
    many_filter = False

    if(tags != "Any"):
        url += "keyword=" + tags
        many_filter = True

    if(division != "Any"):
        if(many_filter): url += "&"
        url += "Division=" + acronyms_reverse.division[division]
        many_filter = True

    if(department != "Any"):
        if(many_filter): url += "&"
        url += "Department=" + acronyms_reverse.department[department]
        many_filter = True

    if(year != "Any"):
        if(many_filter): url += "&"
        url += "Course+Level=" + str(year)
        many_filter = True

    if(campus != "Any"):
        if(many_filter): url += "&"
        url += "Campus=" + acronyms_reverse.campus[campus]
        many_filter = True
    
    return url