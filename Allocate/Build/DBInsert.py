from datetime import datetime
from flask import Flask, jsonify, render_template, url_for, request, redirect
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from Build.DBSetup import session, init_db
from Build.DBCreation import Users

engine = create_engine("sqlite:///Databases.db", echo=True)
Session = sessionmaker(bind=engine)
session = Session()

init_db()

User1 = Users("Jood Wafa", "Student", "joo20210042@std.psut.edu.jo", "1234")
User2 = Users("Salma AlNawaiseh", "Student", "sal20210278@std.psut.edu.jo", "banana milk")

session.add(User1)
session.add(User2)
session.commit()
