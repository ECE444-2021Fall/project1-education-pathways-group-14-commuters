
from wtforms import Form, StringField, SelectField, SelectMultipleField
from wtforms.widgets import CheckboxInput
from wtforms.widgets.core import TableWidget
from ..model import courses
from ..database import acronyms

'''wtforms method to have a MultiCheckboxField returning an array of selected values (may be empty)'''
class MultiCheckboxField(SelectMultipleField):
    widget = TableWidget(with_table_tag=False)
    option_widget = CheckboxInput()

"""Build the search form, including dropdown menus at the top of the page, from the main datafile."""
class CourseSearchForm(Form):
    divisions = [('Any','Any')] + ([
        (t,t) for t in acronyms.division.values()
    ])

    departments = [('Any','Any')] + ([
       (t,t) for t in acronyms.department.values()
    ])


    campus = [('Any','Any')] + ([
        (t,t) for t in acronyms.campus.values()
    ])

    year_choices = [
        (t,t) for t in [0,1,2,3,4,5,6,7]
    ]
            
    top = [
        ('10','10'),
        ('25','25'),
        ('50','50')
    ]
    select = MultiCheckboxField('Course Year:', choices=year_choices)
    top = SelectField('Show Top',choices=top)
    divisions = SelectField('Division:', choices=divisions)
    departments = SelectField('Department:', choices=departments)
    campuses = SelectField('Campus:', choices=campus)
    search = StringField('Search Terms:')
