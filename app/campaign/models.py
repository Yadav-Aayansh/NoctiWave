# /NoctiWave/app/campaign/models.py

from .. import db
from ..user.sponsor.models import Sponsor

class Campaign(db.Model):
    __tablename__ = "Campaign"
    campaign_id = db.Column(db.Integer, primary_key=True)
    sponsor_id = db.Column(db.Integer, db.ForeignKey("Sponsor.sponsor_id"), nullable=False)
    flagged = db.Column(db.String(5), default="False")
    name = db.Column(db.String(60), nullable=False)
    description = db.Column(db.String(60), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    budget = db.Column(db.Float(10,2), nullable=False)
    visibility = db.Column(db.String(10), nullable=False)
    goals = db.Column(db.String(60), nullable=False)
    
    sponsor = db.relationship("Sponsor", back_populates="campaigns")
    ad_requests = db.relationship("AdRequest", back_populates="campaign", cascade="all, delete-orphan")