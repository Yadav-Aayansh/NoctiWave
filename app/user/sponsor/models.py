# /NoctiWave/app/user/sponsor/models.py

from ... import db
from ...user.models import User

class Sponsor(db.Model):
    __tablename__ = "Sponsor"
    sponsor_id = db.Column(db.Integer, primary_key=True)
    flagged = db.Column(db.String(5), default="False")
    website = db.Column(db.String(40))
    company_individual_name = db.Column(db.String(50), default="No Name")
    industry = db.Column(db.String(50))
    budget = db.Column(db.Float(10,2), default=0)
    user_id = db.Column(db.Integer, db.ForeignKey("User.user_id"), nullable=False)

    user = db.relationship("User", back_populates="sponsor", uselist=False)
    campaigns = db.relationship("Campaign", back_populates="sponsor", cascade="all, delete-orphan")
    ad_requests = db.relationship("AdRequest", back_populates="sponsor", cascade="all, delete-orphan")