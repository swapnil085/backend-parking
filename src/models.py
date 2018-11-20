from flask_sqlalchemy import SQLAlchemy
from passlib.hash import pbkdf2_sha256 as encrpyt
import datetime

db = SQLAlchemy()

class User(db.Model):
	__tablename__ = "users"

	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(255), nullable = False)
	email = db.Column(db.String(255), nullable = False)
	contact_number = db.Column(db.String(255), nullable = False)
	gender = db.Column(db.Enum('M','F'), default = 'M')
	password = db.Column(db.String(255), nullable = False)
	created_at = db.Column(db.DateTime, nullable = False, default = datetime.datetime.now)
	bookings = db.relationship("Booking",back_populates="users")

	def __init__(self,name,email,contact_number,gender,password,created_at):
		self.name = name
		self.email = email
		self.contact_number = contact_number
		self.gender = gender
		self.password = password
		self.created_at = created_at

	def generate_hash(self,password):
		pass_hash =  encrpyt.hash(password)
		return pass_hash

	def verify_hash(self,password):
		if encrpyt.verify(password,self.password):
			return True
		else:
			return False	

class Admin(db.Model):
	__tablename__ = "admins"
	id = db.Column(db.Integer,nullable = False,primary_key=True)
	username = db.Column(db.String(255),nullable = False)
	password = db.Column(db.String(255),nullable = False)

	def __init__(self,username,password):
		self.username = username
		self.password = password




class Slot(db.Model):
	__tablename__ = "slots"
	id = db.Column(db.Integer,primary_key=True)
	slot_no = db.Column(db.Integer, nullable=False)
	status = db.Column(db.Enum("AVAILABLE","RESERVED","OCCUPIED"),default="AVAILABLE")
	date = db.Column(db.DateTime,nullable = False, default = datetime.datetime.now())
	start = db.Column(db.DateTime,nullable = False, default=datetime.datetime.now())
	end = db.Column(db.DateTime, nullable=False, default = datetime.datetime.now())
	duration = db.Column(db.Integer,nullable=False,default = 0)
	bookings = db.relationship("Booking",back_populates="slots")

	def __init__(self,slot_no,status,date,start,end,duration):
		self.slot_no = slot_no
		self.status = status
		self.date = date
		self.start = start
		self.end = end
		self.duration = duration

class Booking(db.Model):
	__tablename__ = "bookings"
	id = db.Column(db.Integer,primary_key=True)
	user_id = db.Column(db.Integer,db.ForeignKey("users.id"))
	slot_id = db.Column(db.Integer,db.ForeignKey("slots.id"))
	car_no = db.Column(db.String(255),nullable = False)
	reservation_no = db.Column(db.String(255),nullable = False)
	slots= db.relationship("Slot",back_populates="bookings")
	users = db.relationship("User",back_populates="bookings")

	def __init__(self,user_id,slot_id,car_no,reservation_no):
		self.user_id = user_id
		self.slot_id = slot_id
		self.car_no = car_no
		self.reservation_no = reservation_no





class Feedback(db.Model):
	__tablename__ = "feedbacks"
	id = db.Column(db.Integer,primary_key=True)
	user_id = db.Column(db.Integer,db.ForeignKey('users.id'))
	comments = db.Column(db.String(255),nullable = True)
	rating = db.Column(db.Enum('1','2','3','4','5'),default='5')
	users = db.relationship("User",backref="users",lazy="joined")


	def __init__(self,user_id,comments,rating):
		self.comments= comments
		self.rating = rating
		self.user_id = user_id
