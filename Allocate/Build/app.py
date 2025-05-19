import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import datetime, timedelta
from flask import Flask, jsonify, render_template, url_for, request, redirect, send_from_directory
from sqlalchemy import create_engine, select, or_, and_, desc
from sqlalchemy.orm import sessionmaker
from Build.DBSetup import session, init_db
from Build.DBCreation import Users, Reservations, Facility, Buildings, Reports, Guests, Preparations, PreparationsRequests
from Build.DBCreation import Media, MediaRequests, Transport, TransportRequests, Hospitality, HospitalityRequests, Equipment
from Build.DBCreation import ClubCommittee, Instructors, Clubs, Registration, StudentAffairs, Department, Technicians
from datetime import date, time
from Build.AIModel import AIModel
import hashlib
from flask_mail import Mail, Message
from email.message import EmailMessage
import smtplib




app = Flask(__name__)
# app.secret_key = "your_secret_key"


app.config['MAIL_SERVER'] = 'smtp.mail.yahoo.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True 
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USERNAME'] = 'jood237@yahoo.com'
app.config['MAIL_PASSWORD'] = 'rjorzyaabdjwmgmh'  # Use an app password, NOT your Gmail password
app.config['MAIL_DEFAULT_SENDER'] = 'jood237@yahoo.com'

mail = Mail(app)

engine = create_engine("sqlite:///Databases.db", echo=True)
Session = sessionmaker(bind=engine)
session = Session()

hashObject = hashlib.sha256()

# init_db()

# User1 = Users(20210042, "Jood Wafa", "Student", "joo20210042@std.psut.edu.jo", "bsbsbs")
# User2 = Users(20210278, "Salma AlNawaiseh", "Student", "sal20210278@std.psut.edu.jo", "banana milk")
# User3 = Users(20210559, "Rama Bishawi", "Student", "ram20210559@std.psut.edu.jo", "strawberry shortcake")
# User4 = Users(20210173, "Abdulkarim Damisi", "Student", "abd20210173@std.psut.edu.jo", "great minds")
# User5 = Users(20210001, "Diya Momani", "Student", "diy20210001@std.psut.edu.jo", "duckduck")
# User6 = Users(20210389, "Aya Tell", "Student", "aya20210389@std.psut.edu.jo", "ilovecubes")
# User7 = Users(20210899, "Lama Amer", "Student", "lam20210899@std.psut.edu.jo", "ilovejude")

# Res1 = Reservations(1, "AI Agents", "Workshop", date(2025, 5, 28), time(1, 0), time(2, 30), 1, None, None, None, 1, 1, None)
# Res2 = Reservations(1, "ACM Trainings", "Training Course", date(2025, 5, 28), time(14, 0), time(17, 30), 3, None, None, None, 1, 1, None)

# Report1 = Reports(1, "E-Share not working", 1, None, None, 1, True)

# Equipment1 = Equipment("Monitor", "PC3065-LENOVO1-ThinkcenterM92Pi7", "10040712305200010001", True, "Computer", 1)

# Facility1 = Facility("Luai Shammout", "Auditorium", 75, 2, 1)
# Facility2 = Facility("IT103", "Room", 50, 1, None)
# Facility3 = Facility("IT102", "Room", 40, 1, None)

# Building1 = Buildings("IT")
# Building2 = Buildings("ENG")
# Building3 = Buildings("Bussiness B")
# Building4 = Buildings("Bussiness D")

# Flowers = Preparations("Flowers")
# Backdrop = Preparations("Backdrop")
# Banner = Preparations("Banner/Rollup")
# Materials = Preparations("Printed Materials")
# Laptop = Preparations("Laptop")
# Giftbag = Preparations("Gift Bags")
# Presentation = Preparations("Presentation")
# Screen = Preparations("Screen/Projection")
# Translation = Preparations("Translation")
# Sound = Preparations("Sound Equipment")
# Board = Preparations("Guidance Boards")
# Badges = Preparations("Badges")
# Electrical = Preparations("Electrical Equipment")
# Tour = Preparations("University Tour")
# Stationary = Preparations("Stationary")
# Visual = Preparations("Visual Equipment")
# Other = Preparations("Other")

# Photo = Media("Photo/Video")
# Press = Media("Press")
# Social = Media("Social Media")

# Parking = Transport("Empty Parking Spaces")
# Security = Transport("Inform Security")
# CarBus = Transport("Car/Bus")

# Breakfast = Hospitality("Breakfast")
# Lunch = Hospitality("Lunch")
# Dinner = Hospitality("Dinner")
# Regular = Hospitality("Regular")
# VIP = Hospitality("VIP")
# Coffee = Hospitality("Coffee")
# Juice = Hospitality("Juice")
# Pastries = Hospitality("Pastries")
# Biscuits = Hospitality("Biscuits")

# Dep1 = Department("Computer Science")
# Dep2 = Department("Software Engineering")
# Dep3 = Department("Cyber Security")
# Dep4 = Department("Data Science and AI")
# Dep5 = Department("Computer Graphics")
# Dep6 = Department("Basic Sciences")

# session.add(Dep1)
# session.add(Dep2)
# session.add(Dep3)
# session.add(Dep4)
# session.add(Dep5)
# session.add(Dep6)

# session.add(User1)
# session.add(User2)
# session.add(User3)
# session.add(User4)
# session.add(User5)
# session.add(User6)
# session.add(User7)
# session.add(Res1)
# session.add(Res2)
# session.add(Report1)
# session.add(Equipment1)
# session.add(Facility1)
# session.add(Facility2)
# session.add(Facility3)
# session.add(Building1)
# session.add(Building2)
# session.add(Building3)
# session.add(Building4)
# session.add(Flowers)
# session.add(Backdrop)
# session.add(Banner)
# session.add(Materials)
# session.add(Laptop)
# session.add(Giftbag)
# session.add(Presentation)
# session.add(Screen)
# session.add(Translation)
# session.add(Sound)
# session.add(Board)
# session.add(Badges)
# session.add(Electrical)
# session.add(Tour)
# session.add(Visual)
# session.add(Other)
# session.add(Photo)
# session.add(Press)
# session.add(Social)
# session.add(Breakfast)
# session.add(Lunch)
# session.add(Dinner)
# session.add(Regular)
# session.add(VIP)
# session.add(Coffee)
# session.add(Juice)
# session.add(Pastries)
# session.add(Biscuits)

# session.commit()

@app.route("/logIn", methods=["GET", "POST"])
def logIn():
    if request.method == "POST":
        emails = [email[0] for email in session.query(Users.email).all()]
        print("Emails = ", emails)
        if request.form["email"] in emails:
            print(request.form["email"])
        else:
            print("Not found")
            return render_template("login.html", message = "Invalid username")
        
        password = session.query(Users.password).filter_by(email=request.form["email"]).first()[0]
        print(password)
        if request.form["password"] == password:
            name = session.query(Users.userName).filter_by(email=request.form["email"]).first()[0]
            id = session.query(Users.userId).filter_by(email=request.form["email"]).first()[0]
            role = session.query(Users.role).filter_by(email=request.form["email"]).first()[0]
            if role == "Student" or "Instructor": 
                return redirect("/Homepage/" + str(id))
                # return render_template("home_student.html", message = name, id = id)
            if role == "Student Affairs":
                return redirect("/ViewPendingRequests")
            if role == "Technician":
                return redirect("/ViewPendingReports")
            if role == "Registration":
                return redirect("/GenerateSchedule")
        else:
            print("Inocrrect password")
            return render_template("login.html", message = "Incorrect password")
        
    return render_template("login.html")


@app.route("/ForgotPassword", methods = ["GET", "POST"])
def ForgotPassword():
    if request.method == "POST":
        msg = EmailMessage()
        msg['Subject'] = 'Password reset'
        msg['From'] = app.config['MAIL_USERNAME']
        msg['To'] = request.form["email"]
        userId = session.query(Users.userId).filter_by(email = request.form["email"]).first()[0]
        msg.set_content('Did you forget your password?\nReset password here: ' + request.host + str(url_for("resetPassword", id = userId)))

        with smtplib.SMTP_SSL(app.config['MAIL_SERVER'], 465) as smtp:
            smtp.login(app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD']) 
            smtp.send_message(msg)
    
    return render_template("forgot_password.html")

@app.route("/ResetPassword/<int:id>", methods = ["POST", "GET"])
def resetPassword(id):
    user = session.query(Users).filter_by(userId = id).first()
    
    if request.method == "POST":
        new_password = request.form["password"]
        user.password = new_password
        session.commit()
    
    return render_template("reset_password.html", email=user.email)







########################### Academics #############################
@app.route("/ViewReservations/<int:id>", methods = ["GET", "POST"])
def viewReservations(id):
    reservations = session.query(Reservations).filter_by(reservedBy=id).order_by(desc(Reservations.reservationId)).all()

    result = []
    for r in reservations:
        if r.status == 1:
            facility = session.query(Facility).filter_by(facilityId=r.facilityId).first()
            result.append({
                "reservationId" : r.reservationId,
                "title": r.title,
                "date": r.date.isoformat(),
                "start": r.start.strftime("%H:%M"),
                "facilityName": session.query(Facility.facilityName).filter_by(facilityId = r.facilityId).first()[0],
                "location": session.query(Buildings.buildingName).filter_by(buildingId = facility.buildingId).first()[0],
                "reportId" : r.reportId,
                "reservedBy" : r.reservedBy
            })
            print("Report id = ", r.reportId)


    # print("Reservations = ", reservations)
    return render_template("reservations_student.html", reservations = result, id = id)


@app.route("/Homepage/<int:id>", methods = ["GET", "POST"])
def studentHomePage(id):
    name = session.query(Users.userName).filter_by(userId=id).first()[0]
    lastRequest = session.query(Reservations).filter_by(reservedBy=id).order_by(desc(Reservations.reservationId)).first()
    status = "Pending"
    if lastRequest.status == 1:
        status = "Approved"
    elif lastRequest.status == 2:
        status = "Rejected"
    req = {
        "facility": session.query(Facility.facilityName).filter_by(facilityId=lastRequest.facilityId).first()[0],
        "time": lastRequest.start.strftime("%H:%M"),
        "status": status
    }
    return render_template("home_student.html", name = name, id = id, req=req)


@app.route("/CreateNewPassword/<int:id>", methods = ["GET", "POST"])
def createNewPassword(id):
    user = session.query(Users).filter_by(userId=id)
    if user.password == request.form["oldPassword"]:
        if request.form["newPassword1"] == request.form["newPassword2"]:
            user.password = request.form["newPassword1"]
            session.commit()
        else:
            ###### Add the correct templage path and put a suitable message ######
            return render_template("template.html", message = "New passwords don't match")
        
    else:
        ###### Add the correct templage path and put a suitable message ######
        return render_template("template.html", message = "Incorrect old password")

    ###### Add the correct templage path (some page for succesfull password change) ######
    return render_template("template.html")

        

@app.route("/ReportIssue/<int:resId>", methods = ["GET", "POST"])
def reportIssue(resId):
    reservation = session.query(Reservations).filter_by(reservationId = resId).first()

    if request.method == "GET":
        equipments = [e[0] for e in session.query(Equipment.name).filter_by(facilityId = reservation.facilityId).all()]
        facility = session.query(Facility.facilityName).filter_by(facilityId = reservation.facilityId).first()[0]
        print("reservation.facilityId = ", reservation.facilityId)
        print(equipments)
        if len(equipments) == 0:
            print("yup")
            equipments = None

        return render_template("report_student.html", id = reservation.reservedBy, equipment = equipments, facility=facility)


    if request.method == 'POST':
        description = request.form["description"]
        facility_id = reservation.facilityId
        equipment_name = request.form["equipment"]
        print("smth = ", equipment_name)
        
        if equipment_name != "No equipment found.":
            equipment_id = session.query(Equipment.equipmentId).filter_by(name = equipment_name).first()[0]
            report = Reports(equipment_id, description, facility_id, None, None, reservation.reservedBy, 0)
            # print(reservation.reportId)
            print("reportId = ", report.reportId)
            session.add(report)
            session.commit()
            print("reportId = ", report.reportId)
            reservation.reportId = report.reportId
            session.commit()
    print("res = ", reservation.reservedBy)
    return render_template("report_student.html", id = reservation.reservedBy)


@app.route("/ViewReport/<int:reportId>/<int:id>")
def viewReport(reportId, id):
    report = session.query(Reports).filter_by(reportId = reportId).first()
    facilityName = session.query(Facility.facilityName).filter_by(facilityId = report.facilityId).first()[0]
    equipmentName = session.query(Equipment.name).filter_by(equipmentId = report.equipmentId).first()[0]

    return render_template("view_report_student.html", facility = facilityName, equipment = equipmentName, description = report.reportInfo, id = id)


@app.route("/ReserveSchedule/<int:id>", methods=["GET", "POST"])
def reserveSchedule(id):
    # print("meow")
    if request.method == "POST":
        print("hola")
        start = request.form["start"]
        end = request.form["end"]
        facility = request.form["facility"]
        return redirect(url_for("reserveForm", id=id, start=start, end=end, facility=facility))
    return render_template("reserve_student.html", id=id)


@app.route("/ReserveForm/<int:id>", methods = ["POST", "GET"])
def reserveForm(id):

    if request.method == "GET":
        start = request.args.get("start")
        end = request.args.get("end")
        facility = request.args.get("facility")

        return render_template("reservation_form.html", id=id, start=start, end=end, facility=facility)

    if request.method == "POST":
        title = request.form["eventTitle"]
        eventType = request.form["eventType"]
        date = datetime.strptime(request.form["date"], "%Y-%m-%d").date()
        start = datetime.strptime(request.form["start_time"], "%H:%M").time()
        end = datetime.strptime(request.form["end_time"], "%H:%M").time()
        facilityName = request.form["facility"]
        facilityId = session.query(Facility.facilityId).filter_by(facilityName=facilityName).first()[0]
        fundSource = request.form["fundingSource"]
        fundAmount = request.form["fundingAmount"]
        agenda = request.form["agenda"]


        reservation = Reservations(id, title, eventType, date, start, end, facilityId, 
                                   fundSource, fundAmount, agenda, 0, None, None)
    
        
        session.add(reservation)
        session.commit()
        resId = reservation.reservationId
        print(resId)

        ######## Guests ########
        guestCount = request.form["guestCount"]
        for i in range(int(guestCount)):
            CV = request.form["guestCV" + str(i)]
            if not request.form["guestCV" + str(i)]:
                CV = None
            guest = Guests(request.form["guestName" + str(i)], CV, resId)
            session.add(guest)
        
        session.commit()

        checked_boxes = request.form.getlist('preparations')
        print(f"Checked: {', '.join(checked_boxes)}")

        ####### Preparations #######
        if "flowers" in checked_boxes:
            print("bsbsbs")
            prep = PreparationsRequests(1, resId, None)
            session.add(prep)
        
        if "backdrop" in checked_boxes:
            prep = PreparationsRequests(2, resId, None)
            session.add(prep)
        
        if "banner" in checked_boxes:
            prep = PreparationsRequests(3, resId, None)
            session.add(prep)

        if "printedMaterials" in checked_boxes:
            prep = PreparationsRequests(4, resId, None)
            session.add(prep)
            
        if "laptop" in checked_boxes:
            prep = PreparationsRequests(5, resId, None)
            session.add(prep)

        if "giftBag" in checked_boxes:
            prep = PreparationsRequests(6, resId, str(request.form["giftNum"]))
            session.add(prep)

        if "presentation" in checked_boxes:
            prep = PreparationsRequests(7, resId, None)
            session.add(prep)
            
        if "display" in checked_boxes:
            prep = PreparationsRequests(8, resId, None)
            session.add(prep)

        if "translation" in checked_boxes:
            prep = PreparationsRequests(9, resId, None)
            session.add(prep)
            
        if "soundEquipment" in checked_boxes:
            prep = PreparationsRequests(10, resId, None)
            session.add(prep)
        
        if "guidanceBoards" in checked_boxes:
            prep = PreparationsRequests(11, resId, None)
            session.add(prep)

        if "badges" in checked_boxes:
            prep = PreparationsRequests(12, resId, str(request.form["badgeNum"]))
            session.add(prep)
            
        if "electricalEquipment" in checked_boxes:
            prep = PreparationsRequests(13, resId, None)
            session.add(prep)
        
        if "tour" in checked_boxes:
            prep = PreparationsRequests(14, resId, None)
            session.add(prep)
            
        if "stationary" in checked_boxes:
            prep = PreparationsRequests(15, resId, None)
            session.add(prep)
        
        if "visualEquipment" in checked_boxes:
            prep = PreparationsRequests(16, resId, None)
            session.add(prep)
        
        if "other" in checked_boxes:
            prep = PreparationsRequests(17, resId, request.form["otherInput"])
            session.add(prep)
        

        checked_boxes = request.form.getlist("media")

        if "photoVideo" in checked_boxes:
            media = MediaRequests(1, resId)
            session.add(media)
        
        if "press" in checked_boxes:
            media = MediaRequests(2, resId)
            session.add(media)
        
        if "socialMedia" in checked_boxes:
            media = MediaRequests(3, resId)
            session.add(media)  
        

        checked_boxes = request.form.getlist("transportation")
        if "emptyParking" in checked_boxes:
            transport = TransportRequests(1, resId)
            session.add(transport) 
        
        if "informSecurity" in checked_boxes:
            transport = TransportRequests(2, resId)
            session.add(transport) 
        
        if "car" in checked_boxes:
            transport = TransportRequests(3, resId)
            session.add(transport) 

        checked_boxes = request.form.getlist("hospitality")

        if "breakfast" in checked_boxes:
            host = HospitalityRequests(1, resId)
            session.add(host)

        if "lunch" in checked_boxes:
            host = HospitalityRequests(2, resId)
            session.add(host)

        if "dinner" in checked_boxes:
            host = HospitalityRequests(3, resId)
            session.add(host)
        
        if "regular" in checked_boxes:
            host = HospitalityRequests(4, resId)
            session.add(host)
        
        if "vip" in checked_boxes:
            host = HospitalityRequests(5, resId)
            session.add(host)
        
        if "coffee" in checked_boxes:
            host = HospitalityRequests(6, resId)
            session.add(host)
        
        if "juice" in checked_boxes:
            host = HospitalityRequests(7, resId)
            session.add(host)
        
        if "pastries" in checked_boxes:
            host = HospitalityRequests(8, resId)
            session.add(host)
        
        if "biscuits" in checked_boxes:
            host = HospitalityRequests(9, resId)
            session.add(host)

        session.commit()

    return render_template("reservation_form.html", id=id)

@app.route("/checkAvailability", methods=["POST", "GET"])
def checkAvailability():
    data = request.get_json()
    date = data.get('date') 
    start = data.get('start')     
    end = data.get('end') 
    building = data.get("building")   
    type = data.get("type") 
    capacity = data.get("capacity") 

    requested_date = datetime.strptime(date, "%Y-%m-%d").date()
    
    conflicting = session.query(Reservations.facilityId).filter(
        Reservations.date == requested_date,
        or_(
            and_(start > Reservations.start, start < Reservations.end), 
            and_(end < Reservations.start, end > Reservations.end)
        )
    ).subquery()


    available = session.query(Facility).filter(
        ~Facility.facilityId.in_(conflicting),
        Facility.buildingId == building,
        Facility.facilityType == type,
        Facility.capacity >= capacity).all()
    
    print("wtf")
    print(available)

    return jsonify([{'id': f.facilityId, 'name': f.facilityName} for f in available])


@app.route("/ViewRequests/<int:id>")
def viewRequests(id):
    requests = session.query(Reservations).filter_by(reservedBy=id).order_by(desc(Reservations.reservationId)).all()

    result = []
    for r in requests:
        facility = session.query(Facility).filter_by(facilityId=r.facilityId).first()
        result.append({
            "reservationId" : r.reservationId,
            "title": r.title,
            "date": r.date.isoformat(),
            "start": r.start.strftime("%H:%M"),
            "facilityName": session.query(Facility.facilityName).filter_by(facilityId = r.facilityId).first()[0],
            "location": session.query(Buildings.buildingName).filter_by(buildingId = facility.buildingId).first()[0],
            "reportId" : r.reportId,
            "reservedBy" : r.reservedBy,
            "status": r.status
        })
        print(session.query(Buildings.buildingName).filter_by(buildingId = facility.buildingId).first()[0])

    return render_template("requests_student.html", id=id, requests=result)







########################### Registration #############################
@app.route("/GenerateSchedule", methods=["GET", "POST"])
def generateSchedule():
    if request.method == "POST":
        start_date = request.form["startDate"]
        end_date = request.form["endDate"]

        AIModel.generateExamSchedule(start_date, end_date)

    return render_template("schedule_registration.html")


@app.route("/downloadFile")
def downloadFile():
    return send_from_directory('outputFiles', 'ExamsSchedule.csv', as_attachment=True)





########################### Student Affairs #############################
@app.route("/ViewAllRequests")
def viewAllRequests():
    requests = session.query(Reservations).order_by(desc(Reservations.reservationId)).all()

    result = []
    for r in requests:
        facility = session.query(Facility).filter_by(facilityId=r.facilityId).first()
        result.append({
            "reservationId" : r.reservationId,
            "title": r.title,
            "date": r.date.isoformat(),
            "start": r.start.strftime("%H:%M"),
            "facilityName": session.query(Facility.facilityName).filter_by(facilityId = r.facilityId).first()[0],
            "location": session.query(Buildings.buildingName).filter_by(buildingId = facility.buildingId).first()[0],
            "reportId" : r.reportId,
            "reservedBy" : session.query(Users.userName).filter_by(userId = r.reservedBy).first()[0],
            "status": r.status
        })
        
    return render_template("all_affairs.html", requests=result)


@app.route("/ViewPendingRequests")
def viewPendingRequests():
    requests = session.query(Reservations).order_by(desc(Reservations.reservationId)).all()

    result = []
    for r in requests:
        if r.status == 0:
            facility = session.query(Facility).filter_by(facilityId=r.facilityId).first()
            result.append({
                "reservationId" : r.reservationId,
                "title": r.title,
                "date": r.date.isoformat(),
                "start": r.start.strftime("%H:%M"),
                "facilityName": session.query(Facility.facilityName).filter_by(facilityId = r.facilityId).first()[0],
                "location": session.query(Buildings.buildingName).filter_by(buildingId = facility.buildingId).first()[0],
                "reportId" : r.reportId,
                "reservedBy" : session.query(Users.userName).filter_by(userId = r.reservedBy).first()[0],
                "status": r.status
            })
        
    return render_template("all_affairs.html", requests=result)


@app.route('/ViewRequestForm/<int:resId>', methods = ["POST", "GET"])
def viewRequestForm(resId):
    reservation = session.query(Reservations).filter_by(reservationId=resId).first()
    facility = session.query(Facility).filter_by(facilityId=reservation.facilityId).first()
    guests = session.query(Guests).filter_by(reservationId=resId).all()
    preparations = session.query(PreparationsRequests).filter_by(reservationId=resId).all()
    reqs = []
    gifts = None
    badges = None
    other = None 
    for p in preparations:
        prepName = session.query(Preparations.prepType).filter_by(prepId = p.prepId).first()[0]
        if prepName == "Gift Bags":
            gifts = p.other
        if prepName == "Badges":
            badges = p.other
        if prepName == "Other":
            other = p.other
        reqs.append(prepName)
    media = session.query(MediaRequests).filter_by(reservationId=resId).all() 
    for m in media:
        mediaName = session.query(Media.mediaType).filter_by(mediaId = m.mediaId).first()[0]
        reqs.append(mediaName)
    transport = session.query(TransportRequests).filter_by(reservationId=resId).all() 
    for t in transport:
        tName = session.query(Transport.transportType).filter_by(transportId = t.transportId).first()[0]
        reqs.append(tName)
    hospitality = session.query(HospitalityRequests).filter_by(reservationId=resId).all()
    for h in hospitality:
        hName = session.query(Hospitality.hospitalityType).filter_by(hospitalityId = h.hospitalityId).first()[0]
        reqs.append(hName)

    return render_template("reservation_form_affairs.html", res = reservation, facility = facility, guests=guests, reqs=reqs, gifts=gifts, badges=badges, other=other)


@app.route("/approveRequest/<int:reqId>")
def approveRequest(reqId):
    request = session.query(Reservations).filter_by(reservationId=reqId).first()
    request.status = 1
    session.commit()
    return redirect(url_for("requestApproval", reqId=reqId))

@app.route("/RequestApproval/<int:reqId>", methods = ["GET", "POST"])
def requestApproval(reqId):
    if request.method == "POST":
        req = session.query(Reservations).filter_by(reservationId=reqId).first()
        affairsName = request.form["assigned-affair"]
        userId = session.query(Users.userId).filter_by(userName=affairsName).first()[0]
        affairsId = session.query(StudentAffairs.affairsId).filter_by(userId=userId).first()[0]
        req.affairsId = affairsId
        session.commit()
        return redirect(url_for("viewAllRequests"))

    studentAffairs = [s[0] for s in session.query(Users.userName).filter_by(role="Affairs").all()]
    return render_template("approval_followup_affairs.html", affairs=studentAffairs)


########################### Technicians #############################
@app.route("/ViewAllReports")
def viewAllReports():
    reports = session.query(Reports).order_by(desc(Reports.reportId)).all()

    result = []
    for r in reports:
        result.append({
            "reportId": r.reportId,
            "name": session.query(Users.userName).filter_by(userId=r.issuedBy).first()[0],
            "facility": session.query(Facility.facilityName).filter_by(facilityId = r.facilityId).first()[0],
            "description": r.reportInfo,
            "status": r.status
        })
        
    return render_template("all_technician.html", reports=result)


@app.route("/ViewPendingReports")
def viewPendingReports():
    reports = session.query(Reports).order_by(desc(Reports.reportId)).all()

    result = []
    for r in reports:
        if r.status == 0:
            result.append({
                "reportId": r.reportId,
                "name": session.query(Users.userName).filter_by(userId=r.issuedBy).first()[0],
                "facility": session.query(Facility.facilityName).filter_by(facilityId = r.facilityId).first()[0],
                "description": r.reportInfo,
                "status": r.status
            })
        
    return render_template("pending_technician.html", reports=result)





########################### Admin #############################
@app.route("/AddUser", methods = ["POST", "GET"])
def addUser():
    if request.method == "GET":
        clubs = [c[0] for c in session.query(Clubs.clubName).all()]
        departments = [d[0] for d in session.query(Department.departmentName).all()]
        for c in clubs:
            print(c)
        return render_template("add_user_admin.html", clubs=clubs, departments=departments)
    

    if request.method == "POST":
        uniId = request.form["uniId"]
        name = request.form["name"]
        role = request.form["userType"]
        if role == "0":
            role = "Student"
        if role == "1":
            role = "Instructor"
        if role == "2":
            role = "Registration"
        if role == "3":
            role = "Affairs"
        if role == "4":
            role = "Technician"

        email = request.form["email"]
        user = Users(uniId, name, role, email, None)
        session.add(user)
        session.commit()

        if role == "Student":
            clubName = request.form["clubs"]
            clubId = session.query(Clubs.clubId).filter_by(clubName=clubName).first()[0]
            addClubCommittee(clubId, user.userId)

        if role == "Instructor":
            department = request.form["department"]
            departmentId = session.query(Department.departmentId).filter_by(departmentName = department).first()[0]
            addInstructor(departmentId, user.userId)


        if role == "Registration":
            department = request.form["department"]
            departmentId = session.query(Department.departmentId).filter_by(departmentName = department).first()[0]
            addRegistration(departmentId, user.userId)
            
        if role == "Affairs":
            position = request.form["position"]
            addAffairs(position, user.userId)

        if role == "Technician":
            department = request.form["department"]
            departmentId = session.query(Department.departmentId).filter_by(departmentName = department).first()[0]
            addTechnician(departmentId, user.userId)
        
        redirect(url_for("addUser"))
        
        

    return render_template("add_user_admin.html")

def addClubCommittee(cId, uId):
    print("YESSSS")
    club = ClubCommittee(cId, uId)
    session.add(club)
    session.commit()

def addInstructor(dId, uId):
    instructor = Instructors(dId, uId)
    session.add(instructor)
    session.commit()

def addRegistration(dId, uId):
    registration = Registration(dId, uId)
    session.add(registration)
    session.commit()

def addAffairs(pos, uId):
    affairs = StudentAffairs(pos, uId)
    print("no")
    session.add(affairs)
    session.commit()

def addTechnician(dId, uId):
    technician = Technicians(dId, uId)
    session.add(technician)
    session.commit()

@app.route("/AddClub", methods=["POST", "GET"])
def AddClub():
    if request.method == "POST":
        name = request.form["clubName"]
        supervisor = request.form["supervisor"]

        club = Clubs(name, supervisor)
        session.add(club)
        session.commit()

    return render_template("add_club_admin.html")

@app.route("/AboutUsAdmin")
def AboutUsAdmin():
    return render_template("about_us_admin.html")

@app.route("/AboutUsAcademic")
def AboutUsAcademic():
    return render_template("about_us_academics.html")

@app.route("/AboutUsAffairs")
def AboutUsAffairs():
    return render_template("about_us_affairs.html")

@app.route("/AboutUsRegistration")
def AboutUsRegistration():
    return render_template("about_us_registration.html")

@app.route("/AboutUsTechnician")
def AboutUsTechnician():
    return render_template("about_us_technician.html")

@app.route("/ContactUsAdmin")
def ContactUsAdmin():
    return render_template("contact_us_admin.html")

@app.route("/ContactUsAcademic")
def ContactUsAcademic():
    return render_template("contact_us_academics.html")

@app.route("/ContactUsAffairs")
def ContactUsAffairs():
    return render_template("contact_us_affairs.html")

@app.route("/ContactUsRegistration")
def ContactUsRegistration():
    return render_template("contact_us_registration.html")

@app.route("/ContactUsTechnician")
def ContactUsTechnician():
    return render_template("contact_us_technician.html")

@app.route("/ViewReportTechnician/<int:reportId>", methods=["POST", "GET"])
def viewReportTechnician(reportId):
    report = session.query(Reports).filter_by(reportId = reportId).first()
    if request.method == "GET":
        facilityName = session.query(Facility.facilityName).filter_by(facilityId = report.facilityId).first()[0]
        equipmentName = session.query(Equipment.name).filter_by(equipmentId = report.equipmentId).first()[0]
    
        return render_template("report_technician.html", facility = facilityName, equipment = equipmentName, description = report.reportInfo, id = id)
    
    if request.method == "POST":
        comment = request.form["comment"]
        report.technicianComment = comment
        session.commit()
        return redirect("/ViewPendingReports")
    
    return render_template("report_technician.html")


@app.route("/test")
def test():
    return render_template("report_technician.html")



if __name__ == "__main__":
    app.run()
