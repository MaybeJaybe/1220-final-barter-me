from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SelectField, SubmitField, FloatField, PasswordField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Length, URL, ValidationError

from barter_app.models import ListingCategory, ShopContainer, ListedItem, User
from barter_app.extensions import bcrypt, app, db

class ShopForm(FlaskForm):
	shop_name = StringField('Shop name',
		validators=[
			DataRequired(),
			Length(min=3, max=80, message="Shop name must be between 3 and 80 characters.")
		])
	city = StringField('City',
		validators=[
			DataRequired(),
			Length(min=3, max=80, message="City name must be between 3 and 80 characters.")
		])
	submit = SubmitField('Submit')

class ItemListingForm(FlaskForm):
	item_name = StringField('Name',
		validators=[
			DataRequired(),
			Length(min=3, max=80, message="Item name must be between 3 and 80 characters.")
		])
	price = FloatField('Price',
		validators=[DataRequired()])
	category = SelectField('Category', choices=ListingCategory.choices())
	photo_url = StringField('Photo')
	shop = QuerySelectField('Shop',
		query_factory=lambda: ShopContainer.query, allow_blank=False)
	submit = SubmitField('Submit')