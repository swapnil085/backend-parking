
import datetime
from src.models import *

def test_user():
	user = User(name='foo', email='foo@bar.com', contact_number=100, gender='F', password='foo', created_at=datetime.datetime.now)
	assert user.__str__() == 'foo'

def test_admin():
	admin = Admin(username="foo",password="qwerty")
	assert admin.__str__() == "foo"

def test_slot():
	slot = Slot(slot_no=4,status="AVAILABLE",date = datetime.datetime.now(),start = datetime.datetime.now(),end = datetime.datetime.now(),duration=0)
	assert slot.__str__() == 4		

def test_booking():
	booking = Booking(user_id = 1,slot_id=4,car_no="MP04CM9872",reservation_no="Nov2002")
	assert booking.__str__() == "MP04CM9872"

def test_feedback():
	feedback = Feedback(user_id = 1,comments="improvement needed",rating=4)
	assert feedback.__str__() ==  "improvement needed"

def test_Guard():
	guard = Guard(username="guard10",password="qwerty")
	assert guard.__str__() == "guard10"

def Walk_in():
	walk = Walk_in(email = "abc@gmail.com",reservation_no="Nov3456" , car_no = "MP04CM9872",slot_id = 4)
	assert walk.__str__() == 4

