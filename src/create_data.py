from app import db
from models import Admin,Slot,Walk_in
from flask import session
import datetime

def create_admin():
	admin = Admin(username='admin',password='$pbkdf2-sha256$29000$nHMuRQihNMb4f28N4XxPiQ$jCz/3CoLPaGMDtR9yADmi4E3KWy6jwEOulDkE6B7lJA')
	try:
		db.session.add(admin)
		db.session.commit()
	except:
		db.session.rollback()

# def insert_slots():
# 	for i in range(10):
# 		slot= Slot(slot_no=i,status="AVAILABLE",date=datetime.datetime.now(),start=datetime.datetime.now(),end=datetime.datetime.now(),duration=0)
# 		try:
# 			db.session.add(slot)
# 			db.session.commit()
# 		except:
# 			db.session.rollback()

create_admin()
#insert_slots()