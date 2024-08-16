# /NoctiWave/app/user/admin/models.py

from ... import db

class Admin(db.Model):
    __tablename__ = "Admin"
    admin_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("User.user_id"), nullable=False)
    user = db.relationship("User", back_populates="admin", uselist=False)