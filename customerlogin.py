from wtforms import Form, StringField, SelectField, PasswordField, IntegerField, validators

class CustomerLogin(Form):
    username = StringField('', [validators.Length(min=1,max=150), validators.DataRequired()])
    password = PasswordField('', [validators.Length(min=1,max=150), validators.DataRequired()])

class CreateCustomer(Form):
    firstname = StringField('', [validators.Length(min=1,max=150), validators.DataRequired()])
    lastname = StringField('', [validators.Length(min=1,max=150), validators.DataRequired()])
    gender = SelectField('', [validators.DataRequired()], choices=[('', 'Select'), ('F', 'Female'), ('M', 'Male'), ('O', 'Others')],default='')
    email = StringField('', [validators.Length(min=1,max=150), validators.DataRequired(), validators.Email()])
    password = PasswordField('', [validators.Length(min=1,max=150), validators.DataRequired()])
    username = StringField('', [validators.Length(min=1,max=150), validators.DataRequired()])
    contactNo = IntegerField('', [validators.NumberRange(min=0,max=99999999), validators.DataRequired()])
    membPoints = IntegerField('', [validators.NumberRange(min=0,max=1000), validators.DataRequired()])


class UpdateCustomer(Form):
    firstname = StringField('', [validators.Length(min=1,max=150), validators.DataRequired()], render_kw={'readonly':True})
    lastname = StringField('', [validators.Length(min=1,max=150), validators.DataRequired()], render_kw={'readonly':True})
    gender = SelectField('', [validators.DataRequired()], choices=[('', 'Select'), ('F', 'Female'), ('M', 'Male'), ('O', 'Others')],default='')
    email = StringField('', [validators.Length(min=1,max=150), validators.DataRequired(), validators.Email()])
    password = PasswordField('')
    username = StringField('', [validators.Length(min=1,max=150), validators.DataRequired()], render_kw={'readonly':True})
    contactNo = IntegerField('', [validators.NumberRange(min=0,max=99999999), validators.DataRequired()])
    membStatus = StringField('', [validators.Length(min=1,max=150), validators.DataRequired()], render_kw={'readonly':True})
    membPoints = IntegerField('', [validators.NumberRange(min=0,max=1000), validators.DataRequired()], render_kw={'readonly':True})

class CustomerChange(Form):
    firstname = StringField('', [validators.Length(min=1,max=150), validators.DataRequired()], render_kw={'readonly':True})
    lastname = StringField('', [validators.Length(min=1,max=150), validators.DataRequired()], render_kw={'readonly':True})
    gender = SelectField('', [validators.DataRequired()], choices=[('', 'Select'), ('F', 'Female'), ('M', 'Male'), ('O', 'Others')],default='')
    email = StringField('', [validators.Length(min=1,max=150), validators.DataRequired(), validators.Email()])
    password = PasswordField('')
    username = StringField('', [validators.Length(min=1,max=150), validators.DataRequired()], render_kw={'readonly':True})
    contactNo = IntegerField('', [validators.NumberRange(min=0,max=99999999), validators.DataRequired()])
    #membStatus = SelectField('', [validators.DataRequired()], choices=[('', 'Select'), ('B', 'Bronze'), ('S', 'SILVER'), ('G', 'GOLD')],default='')
    membStatus = StringField('', [validators.Length(min=1,max=150), validators.DataRequired()], render_kw={'readonly':True})
    membPoints = IntegerField('', [validators.NumberRange(min=0,max=1000), validators.DataRequired()], render_kw={'readonly':True})

class ManagePoints(Form):
    type = SelectField('', [validators.DataRequired()], choices=[('', 'Select'), ('A', 'ADD'), ('D', 'DEDUCT')],default='')
    value = IntegerField('', [validators.NumberRange(min=0,max=1000), validators.DataRequired()])
