import os
import unittest
import app

from datetime import date
from barter_app.extensions import app, db, bcrypt
from barter_app.models import ListingCategory, ShopContainer, ListedItem, User

def login(client, username, password):
	return client.post('/login', data=dict(
		username=username,
		password=password
	), follow_redirects=True)

def logout(client):
	return client.get('/logout', follow_redirects=True)

def create_user():
	password_hash = bcrypt.generate_password_hash('password').decode('utf-8')
	user = User(username='Test', password=password_hash)
	db.session.add(user)
	db.session.commit()

def create_shop():
	shop_name = 'Wallyshop'
	city = 'Tri Cities'
	shop = ShopContainer(shop_name=shop_name, city=city)
	db.session.add(shop)
	db.session.commit()

def new_item():
	item_name = "Ice Cream"
	price = 1.25
	category = 'Other'
	photo_url = 'https://www.washingtonpost.com/resizer/qYpYDV1BjKI3ZimLblCjjFXhc2k=/arc-anglerfish-washpost-prod-washpost/public/KUFWIPXROII6ZLAWR67XDFGNPA.jpg'
	shop = 'Wallyshop'



class TestMain(unittest.TestCase):
	def setUp(self):
		app.config['TESTING'] = True
		app.config['WTF_CSRF_ENABLED'] = False
		app.config['DEBUG'] = False
		app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
		self.app = app.test_client()
		db.drop_all()
		db.create_all()

	def test_homepage_logged_out(self):
		create_shop()
		create_user()

		response = self.app.get('/', follow_redirects=True)
		self.assertEqual(response.status_code, 200)

		response_text = response.get_data(as_text=True)
		self.assertIn('Login', response_text)
		self.assertIn('Sign Up', response_text)
		self.assertIn('Wallyshop', response_text)

		self.assertNotIn('Create Storefront', response_text)
		self.assertNotIn('New Listing', response_text)
		self.assertNotIn('Cart', response_text)

	def test_homepage_logged_in(self):
		create_shop()
		create_user()
		login(self.app, 'Test', 'password')

		response = self.app.get('/', follow_redirects=True)
		self.assertEqual(response.status_code, 200)

		response_text = response.get_data(as_text=True)
		
		self.assertIn('Wallyshop', response_text)
		self.assertIn('Test', response_text)
		self.assertIn('Create Storefront', response_text)
		self.assertIn('New Listing', response_text)
		self.assertIn('Cart', response_text)
		self.assertIn('Logout', response_text)

		self.assertNotIn('Sign Up', response_text)
		self.assertNotIn('Login', response_text)

	def test_shop_detail_logged_in(self):
		create_shop()
		create_user()
		login(self.app, 'Test', 'password')

		response = self.app.get('/shop/1', follow_redirects=True)
		self.assertEqual(response.status_code, 200)
		
		response_text = response.get_data(as_text=True)
		self.assertIn('Shop - Wallyshop', response_text)


