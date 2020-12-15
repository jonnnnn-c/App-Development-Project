from wtforms import Form, StringField, RadioField, SelectField, TextAreaField, IntegerField, FloatField, validators, FileField
from Supplier import Supplier

class CreateCandy(Form):
    name = StringField('', [validators.Length(min=1,max=150), validators.DataRequired()])
    retailprice = FloatField('', [validators.NumberRange(min=0,max=1000), validators.DataRequired()])
    costprice = FloatField('', [validators.NumberRange(min=0,max=1000), validators.DataRequired()])
    category = SelectField('', [validators.DataRequired()], choices=[('', 'Select'), ('C', 'Chocolate'), ('G', 'Gummy'), ('F', 'Fizzy'), ('O', 'Others')] ,default='O')
    image = FileField('',[validators.DataRequired()])
    #supplier = SelectField('', [validators.DataRequired()],choices=Supplier.SelectField, default='')
    supplier = SelectField('', [validators.DataRequired()], default='')

class UpdateCandy(Form):
    name = StringField('', render_kw={'readonly':True})
    stock = IntegerField('', [validators.NumberRange(min=0,max=1000)])
    retailprice = FloatField('', [validators.NumberRange(min=0,max=1000), validators.DataRequired()])
    costprice = FloatField('', [validators.NumberRange(min=0,max=1000), validators.DataRequired()])
    category = SelectField('', [validators.DataRequired()], choices=[('', 'Select'), ('C', 'Chocolate'), ('G', 'Gummy'), ('F', 'Fizzy'), ('O', 'Others')],default='O')
    image = FileField('')
    #supplier = SelectField('', [validators.DataRequired()],choices=Supplier.SelectField, default='')
    supplier = SelectField('', [validators.DataRequired()], default='')

