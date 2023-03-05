from sqlalchemy_utils import URLType
from flask_login import UserMixin
from barter_app.utils import FormEnum
from barter_app.extensions import db

class ListingCategory(FormEnum):
	AUTO = 'Auto'
	BEAUTY = 'Beauty'
	ENTERTAINMENT = 'Entertainment'
	FASHION = 'Fashion'
	HEALTH = 'Health'
	HOUSEHOLD = 'Household'
	OUTDOORS = 'Outdoors'
	TECH = 'Tech'
	OTHER = 'Other'

class ShopContainer(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	shop_name = db.Column(db.String(80), nullable=False)
	city = db.Column(db.String(200), nullable=False)
	items = db.relationship('ListedItem', back_populates='shop')
	created_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	created_by = db.relationship('User')

	def __str__(self):
			return f'{self.shop_name}'

class ListedItem(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	item_name = db.Column(db.String(80), nullable=False)
	price = db.Column(db.Float(precision=2), nullable=False)
	category = db.Column(db.Enum(ListingCategory), default=ListingCategory.OTHER)
	photo_url = db.Column(URLType)
	shop_id = db.Column(
			db.Integer, db.ForeignKey('shop_container.id'), nullable=False)
	shop = db.relationship('ShopContainer', back_populates='items')
	created_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	created_by = db.relationship('User')
	cart_items = db.relationship('User', secondary='user_cart', back_populates='cart_list')
	
class User(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(80), nullable=False, unique=True)
	password = db.Column(db.String(80), nullable=False)
	cart_list = db.relationship('ListedItem', secondary='user_cart', back_populates='cart_items')

cart_table = db.Table('user_cart',
	db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
	db.Column('item_id', db.Integer, db.ForeignKey('listed_item.id'), primary_key=True)
)