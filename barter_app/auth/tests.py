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



class TestAuth(unittest.TestCase):
	def setUp(self):
		app.config['TESTING'] = True
		app.config['WTF_CSRF_ENABLED'] = False
		app.config['DEBUG'] = False
		app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
		self.app = app.test_client()
		db.drop_all()
		db.create_all()

	def test_signup(self):
		post_data = {
			'username': 'Test',
			'password': 'password',
		}
		self.app.post('/signup', data=post_data)

		new_user = User.query.filter_by(username='Test').first()
		self.assertEqual('Test', new_user.username)

	# def test_signup_existing_user(self):
	# 	create_user()
	# 	post_data = {
	# 		'username': 'Test',
	# 		'password': 'password',
	# 	}
		
	# 	response = self.app.post('/signup', data=post_data)
	# 	response_text = response.get_data(as_text=True)
	# 	self.assertIn('Username is taken.', response_text)