# /NoctiWave/app/user/models.py

from .. import db
from datetime import datetime

class User(db.Model):
    __tablename__ = "User"
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(60), nullable=False)
    role = db.Column(db.String(10), nullable=False)
    name = db.Column(db.String(50), default='No Name')
    profile_picture = db.Column(db.String(50), default="user_default.svg")
    admin = db.relationship("Admin", back_populates="user", uselist=False, cascade="all, delete-orphan")
    influencer = db.relationship("Influencer", back_populates="user", uselist=False, cascade="all, delete-orphan")
    sponsor = db.relationship("Sponsor", back_populates="user", uselist=False, cascade="all, delete-orphan")
    notifications = db.relationship("Notification", back_populates="user", cascade="all, delete-orphan")


class Notification(db.Model):
    __tablename__ = "Notification"
    notification_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), nullable=False)
    description = db.Column(db.String(100), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    read = db.Column(db.String(5), default="False")
    user_id = db.Column(db.Integer, db.ForeignKey("User.user_id"), nullable=False)
    user = db.relationship("User", back_populates="notifications", uselist=False)

