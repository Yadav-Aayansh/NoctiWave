# /NoctiWave/app/ad-request/models.py

from .. import db
from ..campaign.models import Campaign
from ..user.influencer.models import Influencer
from ..user.sponsor.models import Sponsor


class AdRequest(db.Model):
    __tablename__ = "AdRequest"
    ad_request_id = db.Column(db.Integer, primary_key=True)
    campaign_id = db.Column(db.Integer, db.ForeignKey("Campaign.campaign_id"), nullable=False)
    influencer_id = db.Column(db.Integer, db.ForeignKey("Influencer.influencer_id"), nullable=False)
    sponsor_id = db.Column(db.Integer, db.ForeignKey("Sponsor.sponsor_id"), nullable=False)
    flagged = db.Column(db.String(5), default="False")
    initiator = db.Column(db.String(10), nullable=False)
    requirements = db.Column(db.String(60), nullable=False)
    payment_amount = db.Column(db.Numeric(10,2), nullable=False)
    messages = db.Column(db.String(60), nullable=False)
    status = db.Column(db.String(10), nullable=False, default="Pending")
    
    campaign = db.relationship("Campaign", back_populates="ad_requests")
    influencer = db.relationship("Influencer", back_populates="ad_requests")
    sponsor = db.relationship("Sponsor", back_populates="ad_requests")
    negotiation = db.relationship("Negotiation", back_populates="ad_request", uselist=False, cascade="all, delete-orphan")


class Negotiation(db.Model):
    __tablename__ = "Negotiation"
    negotiation_id = db.Column(db.Integer, primary_key=True)
    ad_request_id = db.Column(db.Integer, db.ForeignKey("AdRequest.ad_request_id"), nullable=False)
    initiator = db.Column(db.String(10), nullable=False)
    message = db.Column(db.String(60), nullable=False)
    status = db.Column(db.String(10), nullable=False)
    
    ad_request = db.relationship("AdRequest", back_populates="negotiation")