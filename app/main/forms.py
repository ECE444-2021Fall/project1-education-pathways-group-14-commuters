
from wtforms import Form, StringField, SelectField, SelectMultipleField
from wtforms.widgets import CheckboxInput
from wtforms.widgets.core import TableWidget
from ..database import acronyms
from ..database.course_choices import course_choices

"""wtforms method to have a MultiCheckboxField returning an array of selected values (may be empty)"""
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

"""Build the edit plan form"""
class EditPlanForm(Form):

    #course_choices from course_choices.py in database folder

    year_choices = [
        (t,t) for t in [2020,2021,2022,2023,2024,2025,2026,2027]
    ]

    sem_choices = {'F':'Fall','W':'Winter','S':'Summer'}

    status_choices = [
        (t,t) for t in ['Taken','Taking','Will Take']
    ]

    code = SelectField("Enter a Course Code/Name", choices=[("", "")] + [(uuid, name) for uuid, name in course_choices.items()])

    year = SelectField('Course Year:', choices=year_choices)

    sem = SelectField('Semester:', choices=sem_choices)

    status = SelectField('Status', choices=status_choices)

