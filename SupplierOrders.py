from wtforms import Form, StringField, RadioField, SelectField, IntegerField, DecimalField, FloatField, FileField, validators, ValidationError
from wtforms.fields.html5 import DateField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
import re
from datetime import date
from Supplier import Supplier

class CreateCheckoutForm(Form):
    firstName = StringField('First Name', [validators.DataRequired()])
    lastName = StringField('Last Name', [validators.DataRequired()])
    phone = StringField('p', [validators.Regexp('^[6|8|9]\d{7}$', message='Invalid phone number'), validators.DataRequired()])
    email = StringField('Email', [validators.Email(message='Invalid email address'), validators.DataRequired()])

    address = StringField('Address', [validators.DataRequired()])
    postalCode = StringField('Postal Code', [validators.Regexp('^[0-9]{6}$', message='Invalid postal code'), validators.DataRequired()])

    shippingMethod = RadioField('Choose an option: ', choices=[('regular', 'Regular ( 1-2 weeks )'), ('express', 'Express ( 1-5 days )')], default='regular')

    expiryDate = StringField('Card Expiration Date', [validators.Regexp('^(0[1-9]|10|11|12)\/[0-9]{2}$', message='Invalid date'), validators.DataRequired()])
    cardVerificationNumber = StringField('Card Verification Number', [validators.Regexp('^[0-9]\d\d$', message='Invalid verification number'), validators.DataRequired()])


class CreateSupplierForm(Form):
    companyName = StringField('Company Name:', [validators.Length(min=1, max=150), validators.DataRequired()])
    companyPhone = StringField('p', [validators.Regexp('^[6|8|9]\d{7}$', message='Invalid phone number'), validators.DataRequired()])
    companyEmail = StringField('Company Email:', [validators.Email(message='Invalid email address'), validators.DataRequired()])
    address = StringField('Office Address:', [validators.DataRequired()])  # find out how to validate address
    postalCode = StringField('Postal Code', [validators.Regexp('^[0-9]{6}$', message='Invalid postal code'), validators.DataRequired()])


class UpdateSupplierForm(Form):
    companyName = StringField('Company Name:', render_kw={'readonly': True})
    companyPhone = StringField('p', [validators.Regexp('^[6|8|9]\d{7}$', message='Invalid phone number'), validators.DataRequired()])
    companyEmail = StringField('Company Email:', [validators.Email(message='Invalid email address'), validators.DataRequired()])
    address = StringField('Office Address:', [validators.DataRequired()])  # find out how to validate address
    postalCode = StringField('Postal Code', [validators.Regexp('^[0-9]{6}$', message='Invalid postal code'), validators.DataRequired()])


def validate_date(form, field):
    if field.data <= date.today():
        raise ValidationError("Invalid Delivery Date")


class CreateOrderForm(Form):
    companyName = StringField('Company Name:', render_kw={'readonly': True})

    product = SelectField('', [validators.DataRequired()], default='')
    productQuantity = StringField('Quantity:', [validators.Regexp('^[0-9]*$', message='Invalid quantity'), validators.DataRequired()])
    productPrice = StringField('Price per candy:', [validators.Regexp('^[0-9]+(\.[0-9]{1,2})?$', message='Invalid price'), validators.DataRequired()])
    deliveryDate = DateField('Product Delivery Date:', [validate_date], format='%Y-%m-%d')
    deliveryStatus = RadioField('Delivery Status:', choices=[('p', 'Pending'), ('d', 'Delivered')], default='p')


class UpdateOrderForm(Form):
    companyName = StringField('Company Name:', render_kw={'readonly': True})
    product = StringField('Product:', render_kw={'readonly': True})
    productQuantity = StringField('Quantity:', [validators.Regexp('^[0-9]*$', message='Invalid quantity'), validators.DataRequired()])
    productPrice = StringField('Price per candy:', [validators.Regexp('^[0-9]+(\.[0-9]{1,2})?$', message='Invalid price'), validators.DataRequired()])
    deliveryDate = DateField('Product Delivery Date:', [validate_date], format='%Y-%m-%d')
    deliveryStatus = RadioField('Delivery Status:', choices=[('p', 'Pending'), ('d', 'Delivered')], default='p')


class SearchCheckoutInformation(Form):
    search = StringField('Enter receipt number:')


class NewEmail(Form):
    email = StringField('New Email', [validators.Email(message='Invalid email address'), validators.DataRequired()])


