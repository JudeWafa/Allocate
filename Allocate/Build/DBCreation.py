from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, Boolean, Date, Time
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.types import JSON
from sqlalchemy.schema import PrimaryKeyConstraint
from Build.DBSetup import Base

###########################
# Base = declarative_base()

################### Users ##################### Done :)
class Users(Base):
    __tablename__ = "Users"

    userId = Column("userId", Integer, primary_key=True)
    uniId = Column("uniId", Integer, nullable=False)
    userName = Column("userName", String, unique=True)
    role = Column("role", String)
    email = Column("email", String)
    password = Column("password", String) ######## Hash the value when inserting



    def __init__(self, uniId, userName, role, email, password):
        self.uniId = uniId
        self.userName = userName
        self.role = role
        self.email = email
        self.password = password


    def __repr__(self):
        return f"User name: {self.userName}"


class Instructors(Base):
    __tablename__ = "Instructors"

    instructorId = Column("instructorId", Integer, primary_key=True)
    departmentId = Column(Integer, ForeignKey("Department.departmentId"))
    userId = Column(Integer, ForeignKey("Users.userId"))


    def __init__(self, departmentId, userId):
        self.departmentId = departmentId
        self.userId = userId


    def __repr__(self):
        return f"Instructor Id: {self.instructorId}"
    

class Clubs(Base):
    __tablename__ = "Clubs"

    clubId = Column("clubId", Integer, primary_key=True)
    clubName = Column("clubName", String)
    supervisorId = Column(Integer, ForeignKey("Instructors.instructorId"))


    def __init__(self, clubName, supervisorId):
        self.clubName = clubName
        self.supervisorId = supervisorId

    def __repr__(self):
        return f"Club: {self.clubName}"


class ClubCommittee(Base):
    __tablename__ = "ClubCommittee"

    studentId = Column("studentId", Integer, primary_key=True)
    clubId = Column(Integer, ForeignKey("Clubs.clubId"))
    userId = Column(Integer, ForeignKey("Users.userId"))


    def __init__(self, clubId, userId):
        self.clubId = clubId
        self.userId = userId

    def __repr__(self):
        return f"Club: {self.clubName}"
  

class Registration(Base):
    __tablename__ = "Registration"

    registrationId = Column("registrationId", Integer, primary_key=True)
    departmentId = Column(Integer, ForeignKey("Department.departmentId"))
    userId = Column(Integer, ForeignKey("Users.userId"))


    def __init__(self, departmentId, userId):
        self.departmentId = departmentId
        self.userId = userId


    def __repr__(self):
        return f"Registration Id: {self.registrationId}"
    

class Technicians(Base):
    __tablename__ = "Technicians"

    technicianId = Column("technicianId", Integer, primary_key=True)
    departmentId = Column(Integer, ForeignKey("Department.departmentId"))
    userId = Column(Integer, ForeignKey("Users.userId"))


    def __init__(self, departmentId, userId):
        self.departmentId = departmentId
        self.userId = userId


    def __repr__(self):
        return f"Technician Id: {self.technicianId}" 


class StudentAffairs(Base):
    __tablename__ = "StudentAffairs"

    affairsId = Column("affairsId", Integer, primary_key=True)
    position = Column("position", String)
    userId = Column(Integer, ForeignKey("Users.userId"))


    def __init__(self, position, userId):
        self.position = position
        self.userId = userId


    def __repr__(self):
        return f"Student Affairs Id: {self.affairsId}"   

################### Facility Management #####################
class Schedule(Base):
    __tablename__ = 'Schedules'
    
    scheduleId = Column(Integer, primary_key=True)
    scheduleName = Column(String)

class Reservations(Base):
    __tablename__ = "Reservations"

    reservationId = Column("reservationId", Integer, primary_key=True)
    reservedBy = Column(Integer, ForeignKey("Users.userId"))
    title = Column("title", String, nullable=False)
    eventType = Column("eventType", String)
    date = Column("date", Date, nullable=False)
    start = Column("start", Time, nullable=False)
    end = Column("end", Time, nullable=False)
    facilityId = Column(Integer, ForeignKey("Facility.facilityName"))
    fundSource = Column("fundSource", String)
    fundAmount = Column("fundAmount", Integer)
    agenda = Column("agenda", String)
    status = Column("status", Integer)
    affairsId = Column(Integer, ForeignKey("StudentAffairs.affairsId"))
    reportId = Column(Integer, ForeignKey("Reports.reportId"))


    def __init__(self, reservedBy, title, eventType, date, start, end, 
                 facilityId, fundSource, fundAmount, agenda, status, affairsId, reportId):
        self.reservedBy = reservedBy
        self.title = title
        self.eventType = eventType
        self.date = date
        self.start = start
        self.end = end
        self.facilityId = facilityId
        self.fundSource = fundSource
        self.fundAmount = fundAmount
        self.agenda = agenda
        self.status = status
        self.affairsId = affairsId
        self.reportId = reportId



    def __repr__(self):
        res = ""
        res+=f"Reservation ID: {self.reservationId}\n"
        res+=f"Reserver: {self.reservedBy}\n"
        res+=f"Date: {self.date}\n"
        res+=f"Time: {self.start}\n"
        res+=f"Status: {self.status}\n"
        res+=f"Facility ID: {self.facilityId}\n"
        res+="\n"
        return res
    
################### Reservation Form #####################
class Guests(Base):
    __tablename__ = "Guests"

    guestId = Column("guestId", Integer, primary_key=True)
    guestName = Column("guestName", String, nullable=False)
    guestCV = Column("guestsCV", String)
    reservationId = Column(Integer, ForeignKey("Reservations.reservationId"))

    def __init__(self, guestName, guestCV, reservationId):
        self.guestName = guestName
        self.guestCV = guestCV
        self.reservationId = reservationId

    def __repr__(self):
        return f"Guest Name: {self.guestName}\n"
    


class Preparations(Base):
    __tablename__ = "Preparations"

    prepId = Column("prepId", Integer, primary_key=True)
    prepType = Column("prepType", String)

    def __init__(self, prepType):
        self.prepType = prepType

    def __repr__(self):
        return f"Preparation Id: {self.prepId}\n Preparation type: {self.prepType}\n"


class PreparationsRequests(Base):
    __tablename__ = "PreparationsRequests"

    prepId = Column(Integer, ForeignKey("Preparations.prepId"), primary_key=True)
    reservationId = Column(Integer, ForeignKey("Reservations.reservationId"), primary_key=True)
    other = Column("other", String, nullable=True)

    def __init__(self, prepId, reservationId, other):
        self.prepId = prepId
        self.reservationId = reservationId
        self.other = other

    __table_args__ = (PrimaryKeyConstraint("prepId", "reservationId"), )

    def __repr__(self):
        return f"Preparation Id: {self.prepId}\n Reservation Id: {self.reservationId}\n"


class Hospitality(Base):
    __tablename__ = "Hospitality"

    hospitalityId = Column("hospitalityId", Integer, primary_key=True)
    hospitalityType = Column("hospitalityType", String)

    def __init__(self, hospitalityType):
        self.hospitalityType = hospitalityType

    def __repr__(self):
        return f"Hospitality Id: {self.hospitalityId}/n Hospitality type: {self.hospitalityType}/n"


class HospitalityRequests(Base):
    __tablename__ = "HospitalityRequests"

    hospitalityId = Column(Integer, ForeignKey("Hospitality.hospitalityId"), primary_key=True)
    reservationId = Column(Integer, ForeignKey("Reservations.reservationId"), primary_key=True)

    def __init__(self, hospitalityId, reservationId):
        self.hospitalityId = hospitalityId
        self.reservationId = reservationId

    __table_args__ = (PrimaryKeyConstraint("hospitalityId", "reservationId"),)

    def __repr__(self):
        return f"Hospitality Id: {self.prepId}/n Reservation Id: {self.reservationId}/n"


class Events(Base):
    __tablename__ = "Events"

    eventId = Column("eventId", Integer, primary_key=True)
    eventType = Column("eventType", String)

    def __init__(self, eventType):
        self.eventType = eventType

    def __repr__(self):
        return f"Event Id: {self.eventId}/n Event type: {self.eventType}/n"


class EventsRequests(Base):
    __tablename__ = "EventsRequests"

    eventId = Column(Integer, ForeignKey("Events.eventId"), primary_key=True)
    reservationId = Column(Integer, ForeignKey("Reservations.reservationId"), primary_key=True)
    other = Column("other", String)

    def __init__(self, eventId, reservationId, other):
        self.eventId = eventId
        self.reservationId = reservationId
        self.other = other

    __table_args__ = (PrimaryKeyConstraint("eventId", "reservationId"), )

    def __repr__(self):
        return f"Event Id: {self.eventId}/n Reservation Id: {self.reservationId}/n"


class Media(Base):
    __tablename__ = "Media"

    mediaId = Column("mediaId", Integer, primary_key=True)
    mediaType = Column("mediaType", String)

    def __init__(self, mediaType):
        self.mediaType = mediaType

    def __repr__(self):
        return f"Media Id: {self.mediaId}/n Media type: {self.mediaType}/n"

class MediaRequests(Base):
    __tablename__ = "MediaRequests"

    mediaId = Column(Integer, ForeignKey("Media.mediaId"), primary_key=True)
    reservationId = Column(Integer, ForeignKey("Reservations.reservationId"), primary_key=True)

    def __init__(self, mediaId, reservationId):
        self.mediaId = mediaId
        self.reservationId = reservationId

    __table_args__ = (PrimaryKeyConstraint("mediaId", "reservationId"), )

    def __repr__(self):
        return f"Media Id: {self.mediaId}/n Reservation Id: {self.reservationId}/n"
    
class Transport(Base):
    __tablename__ = "Transport"

    transportId = Column("transportId", Integer, primary_key=True)
    transportType = Column("transportType", String)

    def __init__(self, transportType):
        self.transportType = transportType

    def __repr__(self):
        return f"Transport Id: {self.transportId}/n Transport type: {self.transportType}/n"

class TransportRequests(Base):
    __tablename__ = "TransportRequests"

    transportId = Column(Integer, ForeignKey("Transport.transportId"), primary_key=True)
    reservationId = Column(Integer, ForeignKey("Reservations.reservationId"), primary_key=True)

    def __init__(self, transportId, reservationId):
        self.transportId = transportId
        self.reservationId = reservationId

    __table_args__ = (PrimaryKeyConstraint("transportId", "reservationId"), )

    def __repr__(self):
        return f"Transport Id: {self.transportId}/n Reservation Id: {self.reservationId}/n"


################### Facilities #####################
class Facility(Base):
    __tablename__ = "Facility"

    facilityId = Column("facilityId", Integer, primary_key=True)
    facilityName = Column("facilityName", String)
    facilityType = Column("facilityType", String)
    capacity = Column("capacity", Integer, nullable=False)
    buildingId = Column(Integer, ForeignKey("Buildings.buildingId"))
    reservationId = Column(Integer, ForeignKey("Reservations.reservationId"))

    def __init__(self, facilityName, facilityType, capacity, buildingId, reservationId):
        self.facilityName = facilityName
        self.facilityType = facilityType
        self.capacity = capacity
        self.buildingId = buildingId
        self.reservationId = reservationId

    def __repr__(self):
        return f"Facility Id: {self.facilityId}/n Facility Name: {self.facilityName}"


class Rooms(Base):
    __tablename__ = "Rooms"

    roomId = Column("roomId", Integer, primary_key=True)
    facilityId = Column(Integer, ForeignKey("Facility.facilityId"))
    roomName = Column("roomName", String)

    def __init__(self, facilityId, roomName):
        self.facilityId = facilityId
        self.roomName = roomName

    def __repr__(self):
        return f"Room: {self.roomName}"
    

class RoomEquipment(Base): ##### Modify on Schema
    __tablename__ = "RoomEquipment"

    equipmentId = Column("equipmentId", Integer, primary_key=True)
    description = Column("description", String)
    barcode = Column("barcode", String, unique=True, nullable=False)
    active = Column("active", Boolean)
    assetClass = Column("assetClass", String)
    roomId = Column(Integer, ForeignKey(Rooms.roomId))

    def __init__(self, description, barcode, active, assetClass, roomId):
        self.description = description
        self.barcode = barcode
        self.active = active
        self.assetClass = assetClass
        self.roomId = roomId
    
    def __repr__(self):
        return f"Room equipment barcode: {self.barcode}/n Room equipment status: {self.active}/n"


class OutdoorSpaces(Base):
    __tablename__ = "OutdoorSpaces"

    outdoorId = Column("outdoorId", Integer, primary_key=True)
    facilityId = Column(Integer, ForeignKey("Facility.facilityId"))
    outdoorName = Column("outdoorName", String)

    def __init__(self, facilityId, outdoorName):
        self.facilityId = facilityId
        self.outdoorName = outdoorName

    def __repr__(self):
        return f"Outdoor Space: {self.outdoorName}"
    

class Labs(Base):
    __tablename__ = "Labs"

    labId = Column("labId", Integer, primary_key=True)
    facilityId = Column(Integer, ForeignKey("Facility.facilityId"))
    labName = Column("labName", String)

    def __init__(self, facilityId, labName):
        self.facilityId = facilityId
        self.labName = labName

    def __repr__(self):
        return f"Lab: {self.labName}"
    
class LabEquipment(Base): ##### Modify schema ######
    __tablename__ = "LabEquipment"

    equipmentId = Column("equipmentId", Integer, primary_key=True)
    description = Column("description", String)
    barcode = Column("barcode", String, unique=True, nullable=False) 
    active = Column("active", Boolean)
    assetClass = Column("assetClass", String)
    labId = Column(Integer, ForeignKey("Labs.labId"))

    def __init__(self, description, barcode, active, assetClass, labId):
        self.description = description
        self.barcode = barcode
        self.active = active
        self.assetClass = assetClass
        self.labId = labId
    
    def __repr__(self):
        return f"Lab equipment barcode: {self.barcode}/n Lab equipment status: {self.active}/n"



class Auditoriums(Base):
    __tablename__ = "Auditoriums"

    auditoriumId = Column("auditoriumId", Integer, primary_key=True)
    facilityId = Column(Integer, ForeignKey("Facility.facilityId"))
    auditoriumName = Column("auditoriumName", String)


    def __init__(self, facilityId, auditoriumName):
        self.facilityId = facilityId
        self.auditoriumName = auditoriumName

    def __repr__(self):
        return f"Auditorium: {self.auditoriumName}"
    

class AuditoriumEquipment(Base):
    __tablename__ = "AuditoriumEquipment"

    equipmentId = Column("equipmentId", Integer, primary_key=True)
    description = Column("description", String)
    barcode = Column("barcode", String, unique=True, nullable=False)
    active = Column("active", Boolean)
    assetClass = Column("assetClass", String)
    auditoriumId = Column(Integer, ForeignKey("Auditoriums.auditoriumId"))

    def __init__(self, description, barcode, active, assetClass, auditoriumId):
        self.description = description
        self.barcode = barcode
        self.active = active
        self.assetClass = assetClass
        self.auditoriumId = auditoriumId
    
    def __repr__(self):
        return f"Auditorium equipment barcode: {self.barcode}/n Auditorium equipment status: {self.active}/n"

class Equipment(Base):
    __tablename__ = "Equipment"

    equipmentId = Column("equipmentId", Integer, primary_key=True)
    name = Column("name", String, nullable=False)
    description = Column("description", String)
    barcode = Column("barcode", String, unique=True, nullable=False)
    active = Column("active", Boolean)
    assetClass = Column("assetClass", String)
    facilityId = Column(Integer, ForeignKey("Facility.facilityId"))

    def __init__(self, name, description, barcode, active, assetClass, facilityId):
        self.name = name
        self.description = description
        self.barcode = barcode
        self.active = active
        self.assetClass = assetClass
        self.facilityId = facilityId
    
    def __repr__(self):
        return f"Equipment barcode: {self.barcode}/n Equipment status: {self.active}/n"


class Department(Base):
    __tablename__ = "Department"

    departmentId = Column("departmentId", Integer, primary_key=True)
    departmentName = Column("departmentName", String)

    def __init__(self, departmentName):
        self.departmentName = departmentName

    def __repr__(self):
        return f"Department name: {self.departmentName}"
    

class Buildings(Base):
    __tablename__ = "Buildings"

    buildingId = Column("buildingId", Integer, primary_key=True)
    buildingName = Column("buildingName", String)

    def __init__(self, buildingName):
        self.buildingName = buildingName

    def __repr__(self):
        return f"Bulding name: {self.buildingName}"

    
################### Courses #####################
class Courses(Base):
    __tablename__ = "Courses"

    courseId = Column("courseId", Integer, primary_key=True)
    courseName = Column("courseName", String)
    departmentId = Column(Integer, ForeignKey("Department.departmentId"))
    numberOfStudents = Column("numberOfStudents", Integer)

    def __init__(self, courseName, departmentId, numberOfStudents):
        self.courseName = courseName
        self.departmentId = departmentId
        self.numberOfStudents = numberOfStudents
    
    def __repr__(self):
        return f"Course name: {self.courseName}"
    
class CourseTaught(Base):
    __tablename__ = "CoursesTaught"

    instructorId = Column(Integer, ForeignKey("Instructors.instructorId"))
    courseId = Column(Integer, ForeignKey("Courses.courseId"))

    __table_args__ = (PrimaryKeyConstraint("instructorId", "courseId"), )

    def __init__(self, instructorId, courseId):
        self.instructorId = instructorId
        self.courseId = courseId
    

################### Technical Support #####################
class Reports(Base):
    __tablename__ = "Reports"

    reportId = Column("reportId", Integer, primary_key=True)
    equipmentId = Column(Integer, ForeignKey(Equipment.equipmentId))
    reportInfo = Column("reportInfo", String, nullable=False)
    facilityId = Column(Integer, ForeignKey("Facility.facilityId"))
    technicianId = Column(Integer, ForeignKey("Technicians.technicianId"))
    technicianComment = Column("technicianComment", String)
    issuedBy = Column(Integer, ForeignKey("Users.userId"))
    status = Column("status", Boolean)

    def __init__(self, equipmentId, reportInfo, facilityId, technicianId, technicianComment, issuedBy, status):
        self.equipmentId = equipmentId
        self.reportInfo = reportInfo
        self.facilityId = facilityId
        self.technicianId = technicianId
        self.technicianComment = technicianComment
        self.issuedBy = issuedBy
        self.status = status

    def __repr__(self):
        return f"Report id: {self.reportId} /n Report info: {self.reportInfo}"



# engine = create_engine("sqlite:///Databases.db", echo=True)
# Base.metadata.create_all(bind=engine)

# Session = sessionmaker(bind=engine)
# session = Session()

# session.commit()


