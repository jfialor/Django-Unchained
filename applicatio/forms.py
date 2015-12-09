from flask.ext.wtf import Form
from wtforms import TextField, validators, HiddenField

class EnterDBInfo(Form):
    dbNotes = TextField(label='Items to add to DB', description="db_enter", validators=[validators.required(), validators.Length(min=0, max=128, message=u'Enter 128 characters or less')])    

class RetrieveDBInfo(Form):
    numRetrieve = TextField(label='Number of DB Items to Get', description="db_get", validators=[validators.required(), validators.Length(min=0, max=500, message=u'Enter 500 characters or less')]) 

class RetrieveRevenue(Form):
    numRetrieve22 = TextField(label='Number of DB Items to Get', description="db_get", validators=[validators.required(), validators.Length(min=0, max=500, message=u'Enter 500 characters or less')])

class RetrieveMovie(Form):
    numRetrieve23 = TextField(label='Number of DB Items to Get', description="db_get", validators=[validators.required(), validators.Length(min=0, max=500, message=u'Enter 500 characters or less')])



class MovieForm(Form):
	field = HiddenField("Main")
	budget = TextField(label="Budget")