from flask import Flask, g, render_template, request , flash, redirect, url_for, session
from passlib.hash import pbkdf2_sha256 as encrpyt
import datetime
from functools import wraps


app = Flask(__name__)
app.config.from_object("config")

from models import db
db.init_app(app)

from models import *

@app.route('/')
@app.route('/home')
def home():
	return render_template("home.html")

#user registration

@app.route('/sign-up',methods=['GET','POST'])
def sign_up():
	if request.method == 'POST':
		name = request.form['name']
		email = request.form['email']
		contact_number = request.form['contact_number']
		password = request.form['password']
		gender = request.form['gender']
		created_at = datetime.datetime.now()
		password_hash = encrpyt.hash(password)
		if gender == "Male":
			gender = "M"
		else:
			gender = "F"	
		usr = User(name = name,email= email,contact_number= contact_number,password= password_hash,
					gender= gender,created_at= created_at)
		try:
			db.session.add(usr)
			db.session.commit()
			flash("User added successfully!!","Success")
		except:
			db.rollback()
			flash("Please try again","error")
		
		return redirect(url_for("home"))

	return render_template("sign_up.html")			


@app.route('/login',methods=['GET','POST'])
def login():
	if request.method == "POST":
		email = request.form['email']
		password = request.form['password']
		usr = User.query.filter_by(email=email).first()
		if encrpyt.verify(password,usr.password):
			flash("Login Successful!")
			session["logged_in"] = True
			return redirect(url_for("dashboard"))

	
	return render_template("login.html")	

def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            #flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('login'))
    return wrap

@app.route('/logout',methods=["GET"])
def logout():
	session.clear()
	return redirect(url_for("login"))

@app.route("/dashboard")
@is_logged_in
def dashboard():
	return render_template("dashboard.html")

@app.route("/book-slot",methods=["GET","POST"])
@is_logged_in
def book_a_slot():
	return render_template("booking.html")	




if __name__ == "__main__" :

	app.run()