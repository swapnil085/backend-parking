from flask import Flask, g, render_template, request , flash, redirect, url_for, session
from passlib.hash import pbkdf2_sha256 as encrpyt
import datetime
from functools import wraps
import random

app = Flask(__name__)
app.config.from_object("config")
app.secret_key = "secret"
from models import db
db.init_app(app)

from models import *

@app.route('/')
@app.route('/home')
def home():
	return render_template("home.html")

#authentication module
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
		if gender == "male":
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
			return redirect(url_for("dashboard",user_id=usr.id))

	
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



# customer dashboard


@app.route("/dashboard/<int:user_id>")
@is_logged_in
def dashboard(user_id):
	return render_template("dashboard.html",user_id = user_id)





# slot booking

@app.route("/book-slot/<int:user_id>",methods=["GET","POST"])
@is_logged_in
def book_a_slot(user_id):
	if request.method == "POST":
		car_no =  request.form["car_no"]
		date = request.form["date"]
		date = datetime.datetime.strptime(date,"%Y-%m-%d")
		print (date)
		start_time = request.form["start"]
		start_time = datetime.datetime.strptime(start_time,"%H:%M")
		
		end_time = request.form["end"]
		end_time = datetime.datetime.strptime(end_time,"%H:%M")
		
		if start_time.day == end_time.day:
			duration = (end_time.hour-start_time.hour)*60 + (end_time.minute-start_time.minute)

		avail_slot_by_status = Slot.query.filter_by(status = "AVAILABLE").first()
		if avail_slot_by_status is not None:
			avail_slot_by_status.status = "RESERVED"
			avail_slot_by_status.date = date
			
			avail_slot_by_status.start = start_time
			
			avail_slot_by_status.end = end_time
			#slot = Slot(avail_slot.slot_no,avail_slot.status,start,end,duration)
			avail_slot_by_status.duration = duration
			res_no = random.randrange(1,10000,3)               
			res_no = date.strftime("%B")[0:3]+str(res_no)		#generate reservation number

			book = Booking(user_id = user_id,slot_id= avail_slot_by_status.id,car_no=car_no,reservation_no=res_no)
			db.session.add(book)
			db.session.commit()
		else:
			available_slot_by_time = Slot.query.filter_by(Slot.end <= start ).first()
			if available_slot_by_time is None:
				flash("No slots available!!")
				return redirect(url_for("dashboard",user_id=user_id))
			else:	
				available_slot_by_time.status = "RESERVED"
				available_slot_by_time.date = date
				available_slot_by_time.start = start_time
				available_slot_by_time.end = end_time
				available_slot_by_time.duration = duration
				book = Booking(user_id = user_id,slot_id= avail_slot_by_time.id,car_no=car_no,reservation_no=res_no)
				db.session.add(book)
				db.session.commit()

		return redirect(url_for("dashboard",user_id = user_id))		
	return render_template("booking.html",user_id = user_id)	




# feedback functionality

@app.route("/feedback/<int:user_id>",methods=["GET","POST"])
@is_logged_in
def feedback(user_id):
	if request.method == "POST":
		
		rating = request.form["rating"]
		comments = request.form["comment"]
		feed = Feedback(user_id,comments,rating)
		try:
			db.session.add(feed)
			db.session.commit()
			flash("Feedback saved successfully","Success")
		except:
			db.rollback()
			flash("Please try again","error")
		return redirect(url_for("dashboard",user_id = user_id))
	return render_template("feedback.html")			




# view history
@app.route("/history/<int:user_id>",methods=["GET","POST"])
@is_logged_in
def history(user_id):
	bookings = Booking.query.filter_by(user_id = user_id).all()
	book_history=[]
	for b in bookings:
		history_dict = {
			"date" : b.slots.date.strftime("%Y-%m-%d"),
			"start_time" : b.slots.start.strftime("%H:%M"),
			"end_time" : b.slots.end.strftime("%H:%M"),
			"charges" : 0
		}
		book_history.append(history_dict)
	return render_template("history.html",book_history = book_history)



#run app

if __name__ == "__main__" :

	app.run()