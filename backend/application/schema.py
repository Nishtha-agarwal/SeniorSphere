import uuid
from datetime import datetime
import pytz
from enum import Enum
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy import Enum as SQLAlchemyEnum
import re


db = SQLAlchemy()

# Indian Standard Time
IST = pytz.timezone('Asia/Kolkata')

class RoleEnum(Enum):
    ADMIN = 0
    SENIOR_CITIZEN = 1
    CARETAKER = 2

class User(db.Model):
    __tablename__ = 'users'

    userId = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    contact = db.Column(db.BigInteger, unique=True, nullable=False)
    passHash = db.Column(db.String(128), nullable=False)
    roleId = db.Column(SQLAlchemyEnum(RoleEnum), nullable=False)
    isBlocked = db.Column(db.Boolean, default=False)
    isVerified = db.Column(db.Integer, default=0)  # 0: Not Verified, 1: Verified, 2: Rejected
    memberSince = db.Column(db.DateTime, default=lambda: datetime.now(IST))
    lastLogin = db.Column(db.DateTime, default=lambda: datetime.now(IST))

    senior_citizen = db.relationship('SeniorCitizen', backref='user', uselist=False)
    caretaker = db.relationship('Caretaker', backref='user', uselist=False)

    def set_password(self, password):
        self.passHash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.passHash, password)

    def to_dict(self):
        return {
            "userId": self.userId,
            "email": self.contact,
            "role": self.roleId.name,  # This will return "ADMIN", "SENIOR_CITIZEN", or "CARETAKER"
            "memberSince": self.memberSince.strftime("%Y-%m-%d %H:%M:%S"),
            "lastLogin": self.lastLogin.strftime("%Y-%m-%d %H:%M:%S") if self.lastLogin else None
        }

# -----------------------
# Senior Citizen class
# -----------------------

# ...existing imports...

class SeniorCitizen(db.Model):
    __tablename__ = 'senior_citizens'

    userId = db.Column(db.String, db.ForeignKey('users.userId'), primary_key=True)
    fullName = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    contact = db.Column(db.BigInteger, nullable=False)
    languages = db.Column(db.String, nullable=True)
    pinCode = db.Column(db.String, nullable=True)
    city = db.Column(db.String, nullable=True)
    state = db.Column(db.String, nullable=True)
    medCon = db.Column(db.String, default=None)
    assignedCare = db.Column(db.String, db.ForeignKey('caretakers.userId'))
    emergencyContact = db.Column(db.BigInteger, nullable=False)
    emergencyContactName = db.Column(db.String, nullable=True)
    emergencyEmail = db.Column(db.String, nullable=True)

    sos_alerts = db.relationship('SOSAlert', backref='sender', lazy=True)
    queries = db.relationship('Query', backref='sender', lazy=True)
    tasks = db.relationship('Tasks', backref='senior', lazy=True, foreign_keys='Tasks.assignedTo')

class Caretaker(db.Model):
    __tablename__ = 'caretakers'

    userId = db.Column(db.String, db.ForeignKey('users.userId'), primary_key=True)
    fullName = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer)
    email = db.Column(db.String, unique=True, nullable=False)
    qualification = db.Column(db.String)
    languages = db.Column(db.String)
    about = db.Column(db.String(255))
    resumePath = db.Column(db.String)

    queries = db.relationship('Query', backref='assignedCaretaker', lazy=True, foreign_keys='Query.assignedCaretakerId')
    tasks = db.relationship('Tasks', backref='caretaker', lazy=True, foreign_keys='Tasks.assignedBy')

class Tasks(db.Model):
    __tablename__ = 'tasks'

    taskId = db.Column(db.String, primary_key=True)
    taskName = db.Column(db.String, nullable=False)
    taskDetails = db.Column(db.String)
    time = db.Column(db.DateTime, default=datetime.utcnow)
    duration = db.Column(db.String)  # In minutes
    status = db.Column(db.Boolean, default=0)  # (Pending = 0 Completed=1)
    assignedTo = db.Column(db.String, db.ForeignKey('senior_citizens.userId'))
    assignedBy = db.Column(db.String, db.ForeignKey('caretakers.userId'))  # Caretaker who created the task

class Query(db.Model):
    __tablename__ = 'queries'

    queryId = db.Column(db.String, primary_key=True)
    sender_id = db.Column(db.String, db.ForeignKey('senior_citizens.userId'), nullable=False)
    message = db.Column(db.String)
    timeStamp = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String, default='Pending')  # (Pending, Resolved)
    assignedCaretakerId = db.Column(db.String, db.ForeignKey('caretakers.userId'))


# -----------------------
# SOS Alert class
# -----------------------
class SOSAlert(db.Model):
    __tablename__ = 'sos_alerts'

    alertId = db.Column(db.String, primary_key=True)
    sender_id = db.Column(db.String, db.ForeignKey('senior_citizens.userId'), nullable=False)
    alertTime = db.Column(db.DateTime, default=datetime.utcnow)
    location = db.Column(db.String)
    isResolved = db.Column(db.Boolean, default=False)
    notifiedCaretaker = db.Column(db.Boolean, default=False)
    notifiedMembers = db.Column(db.Boolean, default=False)
