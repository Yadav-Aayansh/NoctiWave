# /NoctiWave/app/user/influencer/models.py

from ... import db
from ...user.models import User

class Influencer(db.Model):
    __tablename__ = "Influencer"
    influencer_id = db.Column(db.Integer, primary_key=True)
    flagged = db.Column(db.String(5), default="False")
    category = db.Column(db.String(50))
    niche = db.Column(db.String(100))
    bio = db.Column(db.String(50))
    user_id = db.Column(db.Integer, db.ForeignKey("User.user_id"), nullable=False)

    user = db.relationship("User", back_populates="influencer", uselist=False)
    influence = db.relationship("Influence", back_populates="influencer", cascade="all, delete-orphan")
    ad_requests = db.relationship("AdRequest", back_populates="influencer", cascade="all, delete-orphan")

class Influence(db.Model):
    __tablename__ = "Influence"
    influence_id = db.Column(db.Integer, primary_key=True)
    platform = db.Column(db.String(20), nullable=False)
    reach = db.Column(db.Integer, nullable=False)
    url = db.Column(db.String(50), nullable=False)
    influencer_id = db.Column(db.Integer, db.ForeignKey("Influencer.influencer_id"), nullable=False)

    influencer = db.relationship("Influencer", back_populates="influence", uselist=False)