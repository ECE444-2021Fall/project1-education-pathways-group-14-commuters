
from wtforms import Form, StringField, SelectField
from ..model import courses

"""Build the search form, including dropdown menus at the top of the page, from the main datafile."""
class CourseSearchForm(Form):
    divisions = ([('Any','Any')] + sorted(set([
        (t['Division'],t['Division']) for (t) in (courses.find({}, {'Division': True}))
    ])))

    departments = ([('Any','Any')] + sorted(set([
        (t['Department'], t['Department']) for t in (courses.find({}, {'Department': True}))
    ])))
    # print(departments)

    campus = ([('Any','Any')] + sorted(set([
        (t['Campus'], t['Campus']) for t in (courses.find({}, {'Campus': True}))
    ])))

    year_choices = sorted(set([
        (t["Course Level"], t['Course Level']) for t in (courses.find({}, {'Course Level': True}))
    ]))
            
    top = [
        ('10','10'),
        ('25','25'),
        ('50','50')
    ]
    select = SelectField('Course Year:', choices=year_choices)
    top = SelectField('',choices=top)
    divisions = SelectField('Division:', choices=divisions)
    departments = SelectField('Department:', choices=departments)
    campuses = SelectField('Campus:', choices=campus)
    search = StringField('Search Terms:')