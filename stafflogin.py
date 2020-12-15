from wtforms import Form, StringField, SelectField, PasswordField, validators

class StaffLogin(Form):
    username = StringField('', [validators.Length(min=1,max=150), validators.DataRequired()])
    password = PasswordField('', [validators.Length(min=1,max=150), validators.DataRequired()])


class CreateStaff(Form):
    firstname = StringField('', [validators.Length(min=1,max=150), validators.DataRequired()])
    lastname = StringField('', [validators.Length(min=1,max=150), validators.DataRequired()])
    gender = SelectField('', [validators.DataRequired()], choices=[('', 'Select'), ('F', 'Female'), ('M', 'Male'), ('O', 'Others')],default='')
    email = StringField('', [validators.Length(min=1,max=150), validators.DataRequired(), validators.Email()])
    password = PasswordField('', [validators.Length(min=1,max=150), validators.DataRequired()])
    username = StringField('', [validators.Length(min=1,max=150), validators.DataRequired()])

class UpdateStaff(Form):
    firstname = StringField('', [validators.Length(min=1,max=150), validators.DataRequired()], render_kw={'readonly':True})
    lastname = StringField('', [validators.Length(min=1,max=150), validators.DataRequired()], render_kw={'readonly':True})
    gender = SelectField('', [validators.DataRequired()], choices=[('', 'Select'), ('F', 'Female'), ('M', 'Male'), ('O', 'Others')],default='')
    email = StringField('', [validators.Length(min=1,max=150), validators.DataRequired(), validators.Email()])
    password = PasswordField('')
    username = StringField('', [validators.Length(min=1,max=150), validators.DataRequired()], render_kw={'readonly':True})

