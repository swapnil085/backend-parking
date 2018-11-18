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

class Slot(db.Model):
	__tablename__ = "slots"
	id = db.Column(db.Integer,primary_key=True)
	slot_no = db.Column(db.Integer, nullable=False)
	status = db.Column(db.Enum("AVAILABLE","RESERVED","OCCUPIED"),default="AVAILABLE")
	start = db.Column(db.DateTime,nullable = False, default=datetime.datetime.now())
	end = db.Column(db.DateTime,nullable=False)
	duration = db.Column(db.Integer,nullable=False)

	def __init__(self,slot_no,status,start,end,duration):
		self.slot_no = slot_no
		self.status = status
		self.start = start
		self.end = end
		self.duration = duration

class Booking(db.Model):
	__tablename__ = "bookings"
	id = db.Column(db.Integer,primary_key=True)
	user_id = db.Column(db.Integer,db.ForeignKey("users.id"))
	slot_id = db.Column(db.Integer,db.ForeignKey("slots.id"))		
