from flask import Blueprint, request, render_template, redirect, url_for, flash
from datetime import date, datetime
from barter_app.models import ShopContainer, ListedItem, User
from barter_app.main.forms import ShopForm, ItemListingForm

import flask_login
from flask_login import login_user, logout_user, login_required, current_user

from barter_app.extensions import app, db, bcrypt

main = Blueprint("main", __name__)

@main.route('/')
def homepage():
	all_shops = ShopContainer.query.all()
	print(all_shops)
	return render_template('home.html', all_shops=all_shops)

@main.route('/create_shop', methods=['GET', 'POST'])
@login_required
def create_shop():
	form = ShopForm()
	if form.validate_on_submit():
		create_shop = ShopContainer(
			shop_name=form.shop_name.data,
			city=form.city.data,
			created_by=current_user
		)
		db.session.add(create_shop)
		db.session.commit()

		flash('New shop created')
		return redirect(url_for('main.shop_detail', shop_id=create_shop.id))
	return render_template('create_shop.html', form=form)

@main.route('/new_item', methods=['GET', 'POST'])
@login_required
def new_item():
	form = ItemListingForm()
	if form.validate_on_submit():
		new_item = ListedItem(
			item_name=form.item_name.data,
			price=form.price.data,
			category=form.category.data,
			photo_url=form.photo_url.data,
			shop=form.shop.data,
			created_by=flask_login.current_user
		)
		db.session.add(new_item)
		db.session.commit()

		flash('New item added')
		return redirect(url_for('main.item_detail', item_id=new_item.id))
	return render_template('new_item.html', form=form)

@main.route('/shop/<shop_id>', methods=['GET', 'POST'])
@login_required
def shop_detail(shop_id):
	shop = ShopContainer.query.get(shop_id)
	form = ShopForm(obj=shop)
	print(shop.items)
	if form.validate_on_submit():
		shop.shop_name = form.shop_name.data
		shop.city = form.city.data
		db.session.commit()

		flash('Shop updated')
		return redirect(url_for('main.shop_detail', shop_id=shop.id))
	shop = ShopContainer.query.get(shop_id)
	return render_template('shop_detail.html', shop=shop, form=form)

@main.route('/item/<item_id>', methods=['GET', 'POST'])
@login_required
def item_detail(item_id):
	item = ListedItem.query.get(item_id)
	form = ItemListingForm(obj=item)
	if form.validate_on_submit():
		item.item_name = form.item_name.data
		item.price = form.price.data
		item.category = form.category.data
		item.photo_url = form.photo_url.data
		item.shop = form.shop.data
		db.session.add(item)
		db.session.commit()

		flash('Item updated')
		return redirect(url_for('main.item_detail', item_id=item.id))
	item = ListedItem.query.get(item_id)
	return render_template('item_detail.html', item=item, form=form)

@main.route('/delete_item/<item_id>/<shop_id>', methods=['POST'])
@login_required
def delete_item(item_id, shop_id):
	item = ListedItem.query.get(item_id)
	db.session.delete(item)
	db.session.commit()
	flash('Item deleted from store')
	return redirect(url_for('main.shop_detail', shop_id=item.shop_id))

@main.route('/add_to_cart/<item_id>', methods=['POST'])
@login_required
def add_to_cart(item_id):
	item = ListedItem.query.get(item_id)
	current_user.cart_list.append(item)
	db.session.add(current_user)
	db.session.commit()
	flash('Item added to list')
	return redirect(url_for('main.cart', item_id=item_id))

@main.route('/cart')
@login_required
def cart():
	cart = current_user.cart_list
	return render_template('cart.html', cart=cart)

@main.route('/remove_from_cart/<item_id>', methods=['POST'])
@login_required
def remove_from_cart(item_id):
	item = ListedItem.query.get(item_id)
	db.session.delete(item)
	db.session.commit()
	return redirect(url_for('main.cart', item_id=item_id))
