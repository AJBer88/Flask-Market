from market import app
from flask import render_template, redirect, url_for, flash, request
from market.models import Item, User
from market.forms import RegistrationForm, LoginForm, PurchaseItemForm, SellItemForm
from market import db
from flask_login import login_user, login_required, logout_user
from . import Bcrypt
from werkzeug.security import generate_password_hash, check_password_hash

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/market', methods=['GET', 'POST'])
@login_required
def market_page():
    purchase_form = PurchaseItemForm()
    if request.method == "POST":
        purchased_item = request.form.get('purchased_item')
        p_item_object = Item.query.filter_by(name=purchased_item).first()
        if p_item_object:
            if current_user.can_purchase(p_item_object):
                p_item_object.buy(current_user)
                flash(f"Congratulations! You purchased {p_item_object.name} for {p_item_object.price}$", category='success')
            else:
                flash(f"Unfortunately, you don't have enough money to purchase {p_item_object.name}!", category='danger')

        return redirect(url_for('market_page'))

    if request.method == "GET":
        items = Item.query.filter_by(owner=None)
        return render_template('market.html', items=items, purchase_form=purchase_form)

@app.route('/register', methods=['GET','POST'])
def register_page():
	form = RegistrationForm()
	if form.validate_on_submit():
		hashed_password = generate_password_hash(form.password1.data)
		user = User(username=form.username.data, email=form.email.data,
				password_hash=hashed_password)
		db.session.add(user)
		db.session.commit()
		login_user(user)
		flash(f"Success! You are now registered as: {user.username}", category='success')
		return redirect(url_for('home.html'))
	if form.errors != {}:
		for err_msg in form.errors.values():
			flash(f'There was an error with creating a user: {err_msg}', category='danger')
	
	return render_template('register.html', form=form)

@app.route('/login', methods=['GET','POST'])
def login_page():
	form = LoginForm()
	if form.validate_on_submit():
		try:
			user = User.query.filter_by(email=form.email.data).first()
			if check_password_hash(user.password_hash, form.password.data):
				login_user(user, form.remember_me.data)
				flash(f'Success! You have been logged in as: {user.username}', category="success")
				return redirect(url_for('home_page'))
			else:
				flash("Invalid username or password!", "danger")
		except Exception as e:
			flash(e, "danger")

	return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout_page():
	logout_user()
	flash('You have been logged out', category="info")
	return redirect(url_for('home_page'))
		



	

