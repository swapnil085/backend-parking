from flask import Flask, g, render_template, request , flash, redirect, url_for, session
from passlib.hash import pbkdf2_sha256 as encrpyt
import datetime
from functools import wraps
import random
#import json
# payment library
import stripe


app = Flask(__name__)
app.config.from_object("config")
app.secret_key = "secret"
from models import db
db.init_app(app)


#payment keys
pub_key = "pk_test_E4NxK1kQ5tH2AyX5cg4KpBJp00cWoAiGmY"
secret_key = "sk_test_e5ol7EOAOMDPiodmDNvJPS1w00sdSPrTnc"
stripe.api_key = secret_key

#import models
from models import *

#import elasticsearch
from elastic_search import *




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
			return redirect(url_for("dashboard",user_id=usr.id,name="user"))


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
	return redirect(url_for("home"))






# customer dashboard


@app.route("/dashboard/<name>/<int:user_id>")
@is_logged_in
def dashboard(user_id,name):
	return render_template("dashboard.html",user_id = user_id,name = name)





# slot booking

@app.route("/book-slot/<name>/<int:user_id>",methods=["GET","POST"])
@is_logged_in
def book_a_slot(user_id,name):
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
		slots = Slot.query.all()
		print(slots)
		if len(slots)==0:
			for i in range(10):
				slot= Slot(slot_no=i,status="AVAILABLE",date=datetime.datetime.now(),start=datetime.datetime.now(),end=datetime.datetime.now(),duration=0)
				try:
					db.session.add(slot)
					db.session.commit()
				except:
					db.session.rollback()
		avail_slot_by_status = Slot.query.filter(Slot.status=="AVAILABLE").first()
		if avail_slot_by_status is not None:
			avail_slot_by_status.status = "RESERVED"
			avail_slot_by_status.date = date

			avail_slot_by_status.start = start_time

			avail_slot_by_status.end = end_time
			avail_slot_by_status.duration = duration
			res_no = random.randrange(1,10000,3)
			res_no = date.strftime("%B")[0:3]+str(res_no)		#generate reservation number

			book = Booking(user_id = user_id,slot_id= avail_slot_by_status.id,car_no=car_no,reservation_no=res_no)
			book_dict = Booking.obj2dict(book)
			try:
				res = create_index("booking",book_dict)
				print(res)
			except:
				print("Elasticsearch server down!!")
			db.session.add(book)
			db.session.commit()
		else:
			available_slot_by_time = Slot.query.filter(Slot.end <= start_time ).first()
			if available_slot_by_time is None:
				flash("No slots available!!")
				return redirect(url_for("dashboard",user_id=user_id,name=name))
			else:
				available_slot_by_time.status = "RESERVED"
				available_slot_by_time.date = date
				available_slot_by_time.start = start_time
				available_slot_by_time.end = end_time
				available_slot_by_time.duration = duration
				book = Booking(user_id = user_id,slot_id= avail_slot_by_time.id,car_no=car_no,reservation_no=res_no)
				book_dict = Booking.obj2dict(book)
				res = create_index("booking",book_dict)
				print(res)
				db.session.add(book)
				db.session.commit()

		return redirect(url_for("dashboard",user_id = user_id,name = name))
	return render_template("booking.html",user_id = user_id,name = name)




# feedback functionality

@app.route("/feedback/<name>/<int:user_id>",methods=["GET","POST"])
@is_logged_in
def feedback(user_id,name):
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
		return redirect(url_for("dashboard",user_id = user_id,name=name))
	return render_template("feedback.html",name=name,user_id=user_id)




# view history
@app.route("/history/<name>/<int:user_id>",methods=["GET","POST"])
@is_logged_in
def history(user_id,name):
	bookings = Booking.query.filter_by(user_id = user_id).all()
	book_history=[]
	for b in bookings:
		history_dict = {
			"date" : b.slots.date.strftime("%Y-%m-%d"),
			"start_time" : b.slots.start.strftime("%H:%M"),
			"end_time" : b.slots.end.strftime("%H:%M"),
			"charges" : 100
		}
		book_history.append(history_dict)
	return render_template("history.html",book_history = book_history,name=name,user_id=user_id)


@app.route("/cancel-booking/<name>/<user_id>",methods=["GET","POST"])
@is_logged_in
def cancel_booking(name,user_id):
	if request.method == "POST":
		res_no = request.form["res_no"]
		booking = Booking.query.filter_by(reservation_no = res_no).first()
		if booking is not None:
			booking.slots.status = "AVAILABLE"
			db.session.delete(booking)
			flash("Booking canceled successfully!!")
		else:
			flash("Invalid reservation number!!")
		db.session.commit()
		return redirect(url_for("dashboard",user_id = user_id,name=name))
	return render_template("cancel_booking.html",name=name,user_id=user_id)


# -------------------------------------------------------------------------------------------------------


# admin login

@app.route("/admin-login",methods=['GET','POST'])
def admin_login():
	if request.method == "POST":
		username = request.form["username"]
		password = request.form["password"]
		admin = Admin.query.filter_by(username = username).first()
		#print(admin.password)
		admin = Admin(username='admin',password='$pbkdf2-sha256$29000$nHMuRQihNMb4f28N4XxPiQ$jCz/3CoLPaGMDtR9yADmi4E3KWy6jwEOulDkE6B7lJA')
		db.session.add(admin)
		db.session.commit()
		if admin is None:
			flash("Invalid Credentials!")
			return redirect(url_for("admin_login"))
		elif encrpyt.verify(password,admin.password):
			flash("Login Successful!")
			session["logged_in"] = True
			return redirect(url_for("dashboard",user_id = admin.id,name = "admin"))
	return render_template("admin_login.html")


#view bookings

@app.route("/bookings/<name>/<int:user_id>",methods=['GET','POST'])
@is_logged_in
def all_bookings(name,user_id):
	if request.method == "POST":
		date = request.form["date"]
		date = datetime.datetime.strptime(date,"%Y-%m-%d")
		all_bookings = Booking.query.join(Slot , Booking.slot_id == Slot.id).filter(Slot.date == date).all()
		print (len(all_bookings))
		#all_slots = Slot.query.filter_by(date = date)
		show_book = []
		if all_bookings is not None:
			for s in all_bookings:
				#customer_id = s.user_id
				#customer = User.query.filter_by(id = customer_id).first()
				d={
					"name":s.users.name,
					"car_no":s.car_no,
					"email":s.users.email,
					"date":s.slots.date.strftime("%Y-%m-%d"),
					"start":s.slots.start.strftime("%H:%M"),
					"end":s.slots.end.strftime("%H:%M")

				}
				show_book.append(d)
			return render_template("view_bookings.html",show_book = show_book,name=name,user_id = user_id)
		else:
			flash("No bookings on the selected date !!")
			return render_template("view_bookings.html",name=name,user_id=user_id)
	return render_template("view_bookings.html",name = name,user_id=user_id)


#Add / Remove slots
@app.route('/add-slots/<name>/<int:user_id>',methods=["GET","POST"])
@is_logged_in
def add_slots(name,user_id):
	if request.method == "POST":
		last_slot = Slot.query.order_by(Slot.id.desc()).first()
		last_slot_no = last_slot.slot_no
		print(last_slot_no)
		no_of_slots = request.form["no_of_slots"]
		no_of_slots = int(no_of_slots)
		for i in range(no_of_slots):
			last_slot_no = last_slot_no+1
			slot = Slot(slot_no=last_slot_no,status="AVAILABLE",date=datetime.datetime.now(),start=datetime.datetime.now(),end=datetime.datetime.now(),duration=0)
			db.session.add(slot)
		db.session.commit()
		return render_template("slots.html",name=name,user_id=user_id,task = "add")
	return render_template("slots.html",name=name,user_id=user_id,task = "add")

@app.route('/remove-slots/<name>/<int:user_id>',methods=["GET","POST"])
@is_logged_in
def remove_slots(name,user_id):
	if request.method == "POST":
		slot_no = request.form["slot_no"]
		slot_no = int(slot_no)
		slot = Slot.query.filter_by(slot_no = slot_no).first()
		db.session.delete(slot)
		db.session.commit()
		return render_template("slots.html",name=name,user_id=user_id,task="remove")
	return render_template("slots.html",name=name,user_id=user_id,task="remove")

#view feedbacks

@app.route('/feedbacks/<name>/<int:user_id>',methods=["GET"])
@is_logged_in
def view_feedbacks(name,user_id):
	feedbacks = Feedback.query.all()
	return render_template("view_feedbacks.html",feedbacks = feedbacks,name=name,user_id=user_id)



#-----------------------------------------------------------------------------------------------------------

#                Garage access control

@app.route("/guard-login",methods=["GET",'POST'])
def guard_login():
	if request.method == "POST":
		username = request.form["username"]
		password = request.form["password"]
		guard = Guard.query.filter_by(username = username).first()
		if guard is None:
			guard = Guard(username='guard10',password='$pbkdf2-sha256$29000$nHMuRQihNMb4f28N4XxPiQ$jCz/3CoLPaGMDtR9yADmi4E3KWy6jwEOulDkE6B7lJA')
			db.session.add(guard)
			db.session.commit()
		if guard is None:
			flash("Invalid Credentials!")
			return redirect(url_for("guard_login"))
		elif encrpyt.verify(password,guard.password):
			flash("Login Successful!")
			session["logged_in"] = True
			return redirect(url_for("guard_dashboard"))
	return render_template("guard_login.html")

@app.route("/guard",methods=["GET","POST"])
@is_logged_in
def guard_dashboard():
	return render_template("guard_dashboard.html")

@app.route("/entry",methods=["GET","POST"])
@is_logged_in
def entry():
	if request.method == "POST":
		type_customer = request.form["type_customer"]
		if type_customer == "registered":
			return(redirect(url_for("entry_registered")))
		else:
			return redirect(url_for("entry_walk_in"))

	return render_template("entry.html",type_customer="x")

@app.route("/entry/registered",methods=["GET",'POST'])
@is_logged_in
def entry_registered():
	if request.method == "POST":
		res_no = request.form["res_no"]
		booking = Booking.query.filter_by(reservation_no = res_no).first()
		if booking is not None:
			booking.slots.status = "OCCUPIED"
			db.session.commit()
			return redirect(url_for("entry"))
		else:
			flash("Invalid reservation number!!")
			return render_template("entry.html")
	return render_template("entry.html",type_customer = "registered")

@app.route("/entry/walk_in",methods=["GET","POST"])
@is_logged_in
def entry_walk_in():
	if request.method == "POST":
		car_no = request.form["car_no"]
		email = request.form["email"]
		exit_time = request.form["exit_time"]
		exit_time = datetime.datetime.strptime(exit_time,"%H:%M")
		avail_slot_by_status = Slot.query.filter_by(status = "AVAILABLE").first()
		if avail_slot_by_status is not None:
			avail_slot_by_status.status = "OCCUPIED"
			avail_slot_by_status.date = datetime.datetime.now()
			avail_slot_by_status.start = datetime.datetime.now()
			avail_slot_by_status.end = exit_time
			duration = (exit_time.hour-avail_slot_by_status.start.hour)*60 + (exit_time.minute-avail_slot_by_status.start.minute)
			res_no = random.randrange(1,10000,3)
			res_no = avail_slot_by_status.date.strftime("%B")[0:3]+str(res_no)
			walk_in = Walk_in(email=email,reservation_no=res_no,car_no=car_no,slot_id=avail_slot_by_status.id)
			db.session.add(walk_in)
			db.session.commit()
			return(redirect(url_for("entry")))
	return render_template("entry.html",type_customer="walk_in")


@app.route("/exit",methods=["GET","POST"])
@is_logged_in
def exit():
	if request.method == "POST":
		reservation_no = request.form["reservation_no"]
		car_no = request.form["car_no"]

		booking = Booking.query.filter((reservation_no == reservation_no) | (car_no == car_no)).first()
		if booking is None:
			print("Hello")
			walk_in = Walk_in.query.filter((reservation_no == reservation_no) | (car_no == car_no)).first()
			walk_in.slots.status = "AVAILABLE"
			walk_in.slots.start = datetime.datetime.now()
			walk_in.slots.end = datetime.datetime.now()
			walk_in.slots.duration = 0
			db.session.delete(walk_in)
		else:
			print("Hello")
			booking.slots.status = "AVAILABLE"
			booking.slots.start = datetime.datetime.now()
			booking.slots.end = datetime.datetime.now()
			booking.slots.duration = 0
			db.session.delete(booking)

		db.session.commit()
		return redirect(url_for("exit"))
	return render_template("exit.html")

#---------------------------------------payment module ----------------------------------------

@app.route("/pay",methods=["GET","POST"])
def payment():
	if request.method == "POST":
		customer = stripe.Customer.create(email=request.form['stripeEmail'], source=request.form['stripeToken'])
		charge = stripe.Charge.create(customer=customer.id, amount=100, currency='inr', description='The Product')

		return redirect(url_for('thanks'))

	return render_template("pay.html",pub_key=pub_key)

@app.route('/thanks')
def thanks():
    return render_template('thanks.html')


#-----------------------------------elasticsearch------------------------------------
@app.route('/create/<index_name>',methods=["GET"])
def create(index_name):
	create_index(index_name)
	return "created successfully!!"

@app.route("/delete/<index_name>",methods=["GET"])
def del_index(index_name):
	delete_index(index_name)
	return "successfully Deleted!!"


#run app

if __name__ == "__main__" :

	app.run(debug=True,host='0.0.0.0')
