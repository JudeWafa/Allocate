import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from datetime import date, time
from flask import Flask, jsonify, render_template, url_for, request, redirect
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from Build.DBSetup import session, init_db
from Build.DBCreation import Users, Reservations, Facility, Buildings, Reports, Guests, Preparations, PreparationsRequests
from Build.DBCreation import Media, MediaRequests, Transport, TransportRequests, Hospitality, HospitalityRequests, Equipment
from Build.DBCreation import ClubCommittee, Instructors, Clubs, Registration, StudentAffairs, Department, Technicians
import hashlib
import bcrypt

engine = create_engine("sqlite:///Databases.db", echo=True)
Session = sessionmaker(bind=engine)
session = Session()

def hash_password(pw):
    # hash_object = hashlib.sha256()
    # password_bytes = pw.encode('utf-8')
    # hash_object.update(password_bytes)
    # return hash_object.hexdigest()
    password_bytes = pw.encode('utf-8')
    hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    return hashed

# init_db()


User1 = Users(20210042, "Jood Wafa", "Student", "joo20210042@std.psut.edu.jo", hash_password("bsbsbs"))
User2 = Users(20210278, "Salma AlNawaiseh", "Student", "sal20210278@std.psut.edu.jo", hash_password("banana milk"))
# User3 = Users(20210559, "Rama Bishawi", "Student", "ram20210559@std.psut.edu.jo", "strawberry shortcake")
# User4 = Users(20210173, "Abdulkarim Damisi", "Student", "abd20210173@std.psut.edu.jo", "great minds")
# User5 = Users(20210001, "Diya Momani", "Student", "diy20210001@std.psut.edu.jo", "duckduck")
# User6 = Users(20210389, "Aya Tell", "Student", "aya20210389@std.psut.edu.jo", "ilovecubes")
# User7 = Users(20210899, "Lama Amer", "Student", "lam20210899@std.psut.edu.jo", "ilovejude")

Res1 = Reservations(1, "AI Agents", "Workshop", date(2025, 5, 28), time(1, 0), time(2, 30), 1, None, None, None, 1, 1, None)
Res2 = Reservations(1, "ACM Trainings", "Training Course", date(2025, 5, 28), time(14, 0), time(17, 30), 3, None, None, None, 1, 1, None)

Report1 = Reports(1, "E-Share not working", 1, None, None, 1, True)

Equipment1 = Equipment("Monitor", "", "10040712305200010001", True, "Computer", 1)
Equipment2 = Equipment("E-Share", "", "10040712305200011001", True, "E-Share", 1)
Equipment3 = Equipment("Air Conditioner", "", "100407123052000112001", True, "Cooling", 1)
session.add(Equipment2)
session.add(Equipment3)

Facility1 = Facility("Luai Shammout", "Auditorium", 75, 2, 1)
Facility2 = Facility("IT103", "Room", 50, 1, None)
Facility3 = Facility("IT102", "Room", 40, 1, None)

Building1 = Buildings("IT")
Building2 = Buildings("ENG")
Building3 = Buildings("Bussiness B")
Building4 = Buildings("Bussiness D")

Flowers = Preparations("Flowers")
Backdrop = Preparations("Backdrop")
Banner = Preparations("Banner/Rollup")
Materials = Preparations("Printed Materials")
Laptop = Preparations("Laptop")
Giftbag = Preparations("Gift Bags")
Presentation = Preparations("Presentation")
Screen = Preparations("Screen/Projection")
Translation = Preparations("Translation")
Sound = Preparations("Sound Equipment")
Board = Preparations("Guidance Boards")
Badges = Preparations("Badges")
Electrical = Preparations("Electrical Equipment")
Tour = Preparations("University Tour")
Stationary = Preparations("Stationary")
Visual = Preparations("Visual Equipment")
Other = Preparations("Other")

Photo = Media("Photo/Video")
Press = Media("Press")
Social = Media("Social Media")

Parking = Transport("Empty Parking Spaces")
Security = Transport("Inform Security")
CarBus = Transport("Car/Bus")

Breakfast = Hospitality("Breakfast")
Lunch = Hospitality("Lunch")
Dinner = Hospitality("Dinner")
Regular = Hospitality("Regular")
VIP = Hospitality("VIP")
Coffee = Hospitality("Coffee")
Juice = Hospitality("Juice")
Pastries = Hospitality("Pastries")
Biscuits = Hospitality("Biscuits")

Dep1 = Department("Computer Science")
Dep2 = Department("Software Engineering")
Dep3 = Department("Cyber Security")
Dep4 = Department("Data Science and AI")
Dep5 = Department("Computer Graphics")
Dep6 = Department("Basic Sciences")

session.add(Dep1)
session.add(Dep2)
session.add(Dep3)
session.add(Dep4)
session.add(Dep5)
session.add(Dep6)

session.add(User1)
session.add(User2)
# session.add(User3)
# session.add(User4)
# session.add(User5)
# session.add(User6)
# session.add(User7)
session.add(Res1)
session.add(Res2)
session.add(Report1)
session.add(Equipment1)
session.add(Facility1)
session.add(Facility2)
session.add(Facility3)
session.add(Building1)
session.add(Building2)
session.add(Building3)
session.add(Building4)
session.add(Flowers)
session.add(Backdrop)
session.add(Banner)
session.add(Materials)
session.add(Laptop)
session.add(Giftbag)
session.add(Presentation)
session.add(Screen)
session.add(Translation)
session.add(Sound)
session.add(Board)
session.add(Badges)
session.add(Electrical)
session.add(Tour)
session.add(Visual)
session.add(Other)
session.add(Photo)
session.add(Press)
session.add(Social)
session.add(Breakfast)
session.add(Lunch)
session.add(Dinner)
session.add(Regular)
session.add(VIP)
session.add(Coffee)
session.add(Juice)
session.add(Pastries)
session.add(Biscuits)

UserAdmin = Users(1021, "Ahmad", "Admin", "ahmad@psut.edu.jo", hash_password("admin123"))
UserTechnician = Users(2011, "Mohammed", "Technician", "mohammed@psut.edu.jo", hash_password("tech123"))
UserStudentAffairs = Users(3091, "Sara", "Affairs", "sara@psut.edu.jo", hash_password("affairs123"))
print(hash_password("affairs123"))
UserRegistration = Users(4091, "Ibrahim", "Registration", "ibrahim@psut.edu.jo", hash_password("reg123"))

session.add(UserAdmin)
session.add(UserTechnician)
session.add(UserStudentAffairs)
session.add(UserRegistration)


session.commit()
