# /NoctiWave/app/__init__.py

import os
from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from datetime import timedelta
from flask_restful import Api

NoctiWave = Flask(__name__)

current_directory = os.path.abspath(os.path.dirname(__file__))
parent_of_parent_directory = os.path.abspath(os.path.join(current_directory, os.pardir))
db_directory = os.path.join(parent_of_parent_directory, "instance", "noctiwave.sqlite3")

NoctiWave.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + db_directory
db = SQLAlchemy(NoctiWave)
enc = Bcrypt(NoctiWave)
api = Api(NoctiWave)

def app_creator():
    NoctiWave.config["SECRET_KEY"] = "@Emperor_Noctivagous"
    NoctiWave.config["PERMANENT_SESSION_LIFETIME"] = timedelta(days=30)
    NoctiWave.config["UPLOAD_FOLDER"] = "app/static/img/profile"

    from flask import render_template, Blueprint
    from app.user.auth import auth_bp
    from app.user.dashboard import dashboard_bp
    from app.campaign.api import CampaignResource
    from app.ad_request.api import AdRequestResource, NegotiationResource
    from app.user.api import InfluencerResource, InfluencerSearch, SponsorResource

    @NoctiWave.route("/")
    def home():
        return redirect(url_for("auth_bp.login"))
    
    NoctiWave.register_blueprint(auth_bp)
    NoctiWave.register_blueprint(dashboard_bp)

    api.add_resource(CampaignResource, "/api/campaign", "/api/campaign/<string:campaign_id>")
    api.add_resource(AdRequestResource, "/api/ad-request", "/api/ad-request/<int:ad_request_id>")
    api.add_resource(NegotiationResource, "/api/negotiation", "/api/negotiation/<int:negotiation_id>")
    api.add_resource(InfluencerResource, "/api/search_influencer", "/api/search_influencer/<string:username_or_name>")
    api.add_resource(InfluencerSearch, "/api/search_influencerid", "/api/search_influencerid/<int:influencer_id>")
    api.add_resource(SponsorResource, "/api/search_sponsor", "/api/search_sponsor/<int:sponsor_id>")


    NoctiWave.run(debug=True, port=6969)

    return NoctiWave


def database_creator():
    from app.user.models import User, Notification
    from app.user.admin.models import Admin
    from app.user.sponsor.models import Sponsor
    from app.user.influencer.models import Influencer
    from app.campaign.models import Campaign
    from app.ad_request.models import AdRequest, Negotiation

    if not os.path.exists(db_directory):
        os.makedirs(os.path.dirname(db_directory), exist_ok=True)
        with NoctiWave.app_context():
            db.create_all()
            print("Database created and tables initialized. Let's Go!")
    else:
            print("Database already exists. Let's Go!")
