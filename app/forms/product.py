from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField, SubmitField
from wtforms.validators import DataRequired

class ProductForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    price = FloatField("Price", validators=[DataRequired()])
    description  = StringField("Description")
    category = StringField("Category", validators=[DataRequired()])
    quantity = IntegerField("Quantity", validators=[DataRequired()])
    unique_tag = StringField("Unique Tag", validators=[DataRequired()])
    submit = SubmitField("Submit")