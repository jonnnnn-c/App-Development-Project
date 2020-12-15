from wtforms import Form, StringField, RadioField, SelectField, IntegerField, TextAreaField, PasswordField, FloatField, FileField, validators, ValidationError
from wtforms.fields.html5 import DateField
from datetime import date

class CreateCheckoutForm(Form):
    firstName = StringField('First Name', [validators.Regexp('^[A-Za-z]+$', message='Should not contain numbers'), validators.DataRequired()])
    lastName = StringField('Last Name', [validators.Regexp('^[A-Za-z]+$', message='Should not contain numbers'), validators.DataRequired()])
    phone = StringField('', [validators.Regexp('^[6|8|9]\d{7}$', message='Invalid phone number'), validators.DataRequired()])
    email = StringField('Email', [validators.Email(message='Invalid email address'), validators.DataRequired()])
    address = StringField('Address', [validators.DataRequired()])
    postalCode = StringField('Postal Code', [validators.Regexp('^[0-9]{6}$', message='Invalid postal code'), validators.DataRequired()])
    shippingMethod = RadioField('Choose an option: ', choices=[('regular', 'Regular <br/><small>( 1-2 weeks, Free )</small>'), ('express', 'Express <br/><small>( 1-5 days, +$3.50 )</small>')], default='regular')
    expiryDate = StringField('Card Expiration Date', [validators.Regexp('^(0[1-9]|10|11|12)\/[0-9]{2}$', message='Invalid date'), validators.DataRequired()])
    cardVerificationNumber = PasswordField('Card Verification Number', [validators.Regexp('^[0-9]\d\d$', message='Invalid verification number'), validators.DataRequired()])

class UpdateDeliveryForm(Form):
    firstName = StringField('', [validators.DataRequired()], render_kw={'readonly': True})
    lastName = StringField('', [validators.DataRequired()], render_kw={'readonly': True})
    phone = StringField('', [validators.Regexp('^[6|8|9]\d{7}$', message='Invalid phone number'), validators.DataRequired()])
    email = StringField('', [validators.Email(message='Invalid email address'), validators.DataRequired()])
    address = StringField('', [validators.DataRequired()])
    postalCode = StringField('', [validators.Regexp('^[0-9]{6}$', message='Invalid postal code'), validators.DataRequired()])
    shippingMethod = StringField('', render_kw={'readonly': True})
    deliveryStatus = RadioField('', choices=[('p', 'Pending'), ('d', 'Delivered')], default='p')

class CreateSupplierForm(Form):
    companyName = StringField('', [validators.Length(min=1, max=150), validators.DataRequired()])
    companyPhone = StringField('', [validators.Regexp('^[6|8|9]\d{7}$', message='Invalid phone number'), validators.DataRequired()])
    companyEmail = StringField('', [validators.Email(message='Invalid email address'), validators.DataRequired()])
    address = StringField('', [validators.DataRequired()])  # find out how to validate address
    postalCode = StringField('', [validators.Regexp('^[0-9]{6}$', message='Invalid postal code'), validators.DataRequired()])

class UpdateSupplierForm(Form):
    companyName = StringField('', render_kw={'readonly': True})
    companyPhone = StringField('', [validators.Regexp('^[6|8|9]\d{7}$', message='Invalid phone number'), validators.DataRequired()])
    companyEmail = StringField('', [validators.Email(message='Invalid email address'), validators.DataRequired()])
    address = StringField('', [validators.DataRequired()])  # find out how to validate address
    postalCode = StringField('', [validators.Regexp('^[0-9]{6}$', message='Invalid postal code'), validators.DataRequired()])

def validate_date(form, field):
    if field.data <= date.today():
        raise ValidationError("Invalid Delivery Date")


class CreateOrderForm(Form):
    companyName = StringField('', render_kw={'readonly': True})

    product = SelectField('', [validators.DataRequired()], default='')
    productQuantity = StringField('', [validators.Regexp('^[0-9]*$', message='Invalid quantity'), validators.DataRequired()])
    deliveryDate = DateField('', [validate_date], format='%Y-%m-%d')
    deliveryStatus = RadioField('', choices=[('p', 'Pending'), ('d', 'Delivered')], default='p')


class UpdateOrderForm(Form):
    companyName = StringField('', render_kw={'readonly': True})
    product = StringField('', render_kw={'readonly': True})
    productQuantity = StringField('', [validators.Regexp('^[0-9]*$', message='Invalid quantity'), validators.DataRequired()])
    productPrice = StringField('', [validators.Regexp('^[0-9]+(\.[0-9]{1,2})?$', message='Invalid price'), validators.DataRequired()], render_kw={'readonly': True})
    deliveryDate = DateField('', [validate_date], format='%Y-%m-%d')
    deliveryStatus = RadioField('', choices=[('p', 'Pending'), ('d', 'Delivered')], default='p')


class SearchCheckoutInformation(Form):
    search = StringField('Enter receipt number:')


class NewEmail(Form):
    email = StringField('New Email', [validators.Email(message='Invalid email address'), validators.DataRequired()])


class CreateFeedbackForm(Form):
    firstName = StringField('First Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    lastName = StringField('Last Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    email = StringField('Email', [validators.Email(message='Invalid email address'), validators.DataRequired()])
    phone = StringField('Contact', [validators.Regexp('^[6|8|9]\d{7}$', message='Invalid phone number'), validators.DataRequired()])  # - counted as number
    region = SelectField('Region', choices=[('AS', 'Asia'), ('AM', 'America'), ('AF', 'Africa'), ('EU', 'Europe')], default='AS')
    surveyOne= RadioField('How would you rate your overall satisfaction with the webpage?', [validators.DataRequired()], choices=[('Very Satisfied','Very Satisfied'), ('Satisfied','Satisfied'), ('Neutral','Neutral'), ('Unsatisfied','Unsatisfied'), ('Very Unsatisfied','Very Unsatisfied')])
    surveyTwo = RadioField('Would you visit our website again?', [validators.DataRequired()], choices=[('Yes','Yes'), ('Maybe','Maybe'), ('No','No')])
    improvements = TextAreaField('How Can We Improve?', [validators.Optional()])


class StaffLogin(Form):
    username = StringField('', [validators.Length(min=1,max=150), validators.DataRequired()])
    password = PasswordField('', [validators.Length(min=1,max=150), validators.DataRequired()])


class CreateStaff(Form):
    firstname = StringField('', [validators.Length(min=1,max=150), validators.DataRequired()])
    lastname = StringField('', [validators.Length(min=1,max=150), validators.DataRequired()])
    gender = SelectField('', [validators.DataRequired()], choices=[('', 'Select'), ('F', 'Female'), ('M', 'Male'), ('O', 'Others')],default='')
    email = StringField('', [validators.Length(min=1,max=150), validators.DataRequired(), validators.Email()])
    password = PasswordField('', [validators.Length(min=1,max=150), validators.DataRequired()])


class UpdateStaff(Form):
    firstname = StringField('', [validators.Length(min=1,max=150), validators.DataRequired()], render_kw={'readonly':True})
    lastname = StringField('', [validators.Length(min=1,max=150), validators.DataRequired()], render_kw={'readonly':True})
    gender = SelectField('', [validators.DataRequired()], choices=[('', 'Select'), ('F', 'Female'), ('M', 'Male'), ('O', 'Others')],default='')
    email = StringField('', [validators.Length(min=1,max=150), validators.DataRequired(), validators.Email()])
    password = PasswordField('')

class CreateCandy(Form):
    name = StringField('', [validators.Length(min=1,max=150), validators.DataRequired()])
    retailprice = StringField('', [validators.Regexp('^(\d+\.\d{2})$', message='Invalid price'), validators.DataRequired()])
    costprice = StringField('', [validators.Regexp('^(\d+\.\d{2})$', message='Invalid price'), validators.DataRequired()])
    category = SelectField('', [validators.DataRequired()], choices=[('', 'Select'), ('C', 'Chocolate'), ('G', 'Gummy'), ('F', 'Fizzy'), ('S', 'Specials')] , default='')
    image = FileField('',[validators.DataRequired()])
    supplier = SelectField('', [validators.DataRequired()], default='')
    keyinformation = TextAreaField('', [validators.DataRequired()], default='')
    ingredients = TextAreaField('', [validators.DataRequired()], default='')
    country = StringField('', [validators.DataRequired()], default='')


class UpdateCandy(Form):
    name = StringField('', render_kw={'readonly':True})
    stock = IntegerField('', [validators.NumberRange(min=0,max=1000)])
    retailprice = StringField('', [validators.Regexp('^(\d+\.\d{2})$', message='Invalid price'), validators.DataRequired()])
    costprice = StringField('', [validators.Regexp('^(\d+\.\d{2})$', message='Invalid price'), validators.DataRequired()])
    category = SelectField('', [validators.DataRequired()], choices=[('', 'Select'), ('C', 'Chocolate'), ('G', 'Gummy'), ('F', 'Fizzy'), ('S', 'Specials')], default='')
    image = FileField('')
    supplier = StringField('', render_kw={'readonly':True})
    keyinformation = TextAreaField('', [validators.DataRequired()])
    ingredients = TextAreaField('', [validators.DataRequired()])
    country = StringField('', [validators.DataRequired()])


class CustomerLogin(Form):
    username = StringField('', [validators.Length(min=1,max=150), validators.DataRequired()])
    password = PasswordField('', [validators.Length(min=1,max=150), validators.DataRequired()])

class CreateCustomer(Form):
    firstname = StringField('', [validators.Length(min=1,max=150), validators.DataRequired()])
    lastname = StringField('', [validators.Length(min=1,max=150), validators.DataRequired()])
    gender = SelectField('', [validators.DataRequired()], choices=[('', 'Select'), ('F', 'Female'), ('M', 'Male'), ('O', 'Others')],default='')
    email = StringField('', [validators.Length(min=1,max=150), validators.DataRequired(), validators.Email()])
    password = PasswordField('', [validators.Length(min=1,max=150), validators.DataRequired()])
    contactNo = StringField('', [validators.Regexp('^[6|8|9]\d{7}$', message='Invalid phone number'), validators.DataRequired()])

class s_CreateCustomer(Form):
    firstname = StringField('', [validators.Length(min=1,max=150), validators.DataRequired()])
    lastname = StringField('', [validators.Length(min=1,max=150), validators.DataRequired()])
    gender = SelectField('', [validators.DataRequired()], choices=[('', 'Select'), ('F', 'Female'), ('M', 'Male'), ('O', 'Others')],default='')
    email = StringField('', [validators.Length(min=1,max=150), validators.DataRequired(), validators.Email()])
    password = PasswordField('', [validators.Length(min=1,max=150), validators.DataRequired()])
    contactNo = StringField('', [validators.Regexp('^[6|8|9]\d{7}$', message='Invalid phone number'), validators.DataRequired()])
    membPoints = IntegerField('')

class UpdateCustomer(Form):
    firstname = StringField('', [validators.Length(min=1,max=150), validators.DataRequired()], render_kw={'readonly':True})
    lastname = StringField('', [validators.Length(min=1,max=150), validators.DataRequired()], render_kw={'readonly':True})
    gender = SelectField('', [validators.DataRequired()], choices=[('', 'Select'), ('F', 'Female'), ('M', 'Male'), ('O', 'Others')],default='')
    email = StringField('', [validators.Length(min=1,max=150), validators.DataRequired(), validators.Email()])
    password = PasswordField('')
    contactNo = StringField('', [validators.Regexp('^[6|8|9]\d{7}$', message='Invalid phone number'), validators.DataRequired()])
    membStatus = StringField('', [validators.Length(min=1,max=150), validators.DataRequired()], render_kw={'readonly':True})
    membPoints = IntegerField('', [validators.NumberRange(min=-1,max=1000)], render_kw={'readonly':True})

class CustomerChange(Form):
    firstname = StringField('', [validators.Length(min=1,max=150), validators.DataRequired()], render_kw={'readonly':True})
    lastname = StringField('', [validators.Length(min=1,max=150), validators.DataRequired()], render_kw={'readonly':True})
    gender = SelectField('', [validators.DataRequired()], choices=[('', 'Select'), ('F', 'Female'), ('M', 'Male'), ('O', 'Others')],default='')
    email = StringField('', [validators.Length(min=1,max=150), validators.DataRequired(), validators.Email()])
    password = PasswordField('')
    contactNo = StringField('', [validators.Regexp('^[6|8|9]\d{7}$', message='Invalid phone number'), validators.DataRequired()])
    membStatus = StringField('', [validators.Length(min=1,max=150), validators.DataRequired()], render_kw={'readonly':True})
    membPoints = IntegerField('', [validators.NumberRange(min=-1,max=1000)], render_kw={'readonly':True})

class ManagePoints(Form):
    type = SelectField('', [validators.DataRequired()], choices=[('', 'Select'), ('A', 'ADD'), ('D', 'DEDUCT')],default='')
    value = IntegerField('', [validators.NumberRange(min=0,max=1000), validators.DataRequired()])

class LoginForm(Form):
    id = IntegerField('', [ validators.DataRequired()])
    password = PasswordField('', [validators.Length(min=1,max=150), validators.DataRequired()])

class CartQuantity(Form):
    quantity = IntegerField('', [validators.NumberRange(min=0,max=1000), validators.DataRequired()])
