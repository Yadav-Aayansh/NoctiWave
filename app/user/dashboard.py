# /NoctiWave/app/user/dashboard.py

from flask import render_template, Blueprint, session, redirect, url_for, request, jsonify, flash
from .models import User
from .sponsor.models import Sponsor
from .influencer.models import Influencer, Influence
from ..campaign.models import Campaign
from ..ad_request.models import AdRequest, Negotiation
import requests
from ..campaign.management import id_to_sponsor
from ..ad_request.management import id_to_campaign, id_to_influencer, id_to_sponsor
from werkzeug.utils import secure_filename
import os
from .. import NoctiWave
from .management import *
from .. import db
from .charts import *
from sqlalchemy import desc, func

dashboard_bp = Blueprint("dashboard_bp", __name__)

@dashboard_bp.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if session.get("user_id"):
        user_id = session["user_id"]
        base_url = request.url_root
        headers = {'Content-Type': 'application/json'}
        user = User.query.filter_by(user_id=user_id).first()
        if user.role == "admin":
            sponsors = Sponsor.query.all()
            influencers = Influencer.query.all()
            campaigns = Campaign.query.all()
            ad_requests = AdRequest.query.all()
            negotiations = Negotiation.query.all()
            return render_template("admin/dashboard_home.html", user=user, active_page="dashboard", everything=everything_chart(),
                                   campaign_distribution_chart=campaign_distribution_chart(), sponsor_influencer_ratio_chart=sponsor_influencer_ratio_chart(),
                                   ad_request_status_chart=ad_request_status_chart())
        
        
        elif user.role == "influencer":
            influencer_id = Influencer.query.filter_by(user_id=user.user_id).first().influencer_id
            if request.method == "GET":
                campaigns = Campaign.query.filter(Campaign.visibility=='Public').filter(Campaign.flagged == 'False').order_by(desc(Campaign.budget)).limit(5).all()
                influencer = Influencer.query.filter_by(user_id=user_id).first()
                negotiation = 0
                for ad_request in influencer.ad_requests:
                    if ad_request.flagged == 'False' and ad_request.negotiation:
                        negotiation += 1
                notifications = Notification.query.filter_by(user_id=user_id).order_by(Notification.timestamp.desc()).all()
                return render_template("influencer/dashboard_home.html", user=user, active_page="dashboard", campaigns=campaigns, influencer=influencer, 
                                       negotiation=negotiation, notifications=notifications, time_converter=time_converter)
            
            elif request.method == "POST":
                headers = {'Content-Type': 'application/json'}
                base_url = request.url_root
                if request.form["_method"] == "POST":
                    ad_request = request.form.to_dict()
                    ad_request["influencer_id"] = influencer_id
                    ad_request["initiator"] = "influencer"
                    requests.post(base_url + "/api/ad-request", json=ad_request, headers=headers)
                    flash("AdRequest sent successfully!", "success")
                    return redirect(url_for("dashboard_bp.ad_requests"))
        

        elif user.role == "sponsor":
            sponsor = Sponsor.query.filter_by(user_id=user_id).first()
            campaigns = Campaign.query.filter_by(sponsor_id=sponsor.sponsor_id).all()
            if request.method == "GET":
                query = request.args.to_dict()
                influencers = Influencer.query.filter_by(flagged='False').all()
                mydict, negotiation = {}, 0
                for influencer in influencers:
                    mydict[influencer] = len(list(influencer.ad_requests))
                sorted_dict = dict(sorted(mydict.items(), key=lambda item: item[1], reverse=True))
                influencers = list(sorted_dict.keys())[:3]
                for ad_request in sponsor.ad_requests:
                    if ad_request.flagged == 'False' and ad_request.negotiation:
                        negotiation += 1
                notifications = Notification.query.filter_by(user_id=user_id).order_by(Notification.timestamp.desc()).all()
                return render_template("sponsor/dashboard_home.html", user=user, active_page="dashboard", sponsor=sponsor, time_converter=time_converter,
                                   notifications=notifications, influencers=influencers, converter=my_converter, campaigns=campaigns, negotiation=negotiation)
            elif request.method == "POST":
                if request.form["_method"] == "POST":
                    ad_request = request.form.to_dict()
                    ad_request["sponsor_id"] = sponsor.sponsor_id
                    ad_request["initiator"] = "sponsor"
                    requests.post(base_url + "/api/ad-request", json=ad_request, headers=headers)
                    flash("AdRequest sent successfully!", "success")
                    return redirect(url_for("dashboard_bp.ad_requests"))
                elif request.form["_method"] == "MARKREAD":
                    data = request.form.to_dict()
                    notification = Notification.query.get(data["notification_id"])
                    db.session.delete(notification)
                    db.session.commit()
                    flash("Notification marked as read successfully!", "success")
                    return redirect(url_for("dashboard_bp.dashboard"))

                
            
        else:
            return redirect(url_for("auth_bp.login"))
    else:
        return redirect(url_for("auth_bp.login"))

@dashboard_bp.route("/dashboard/campaigns", methods=["GET", "POST", "PUT", "DELETE"])
def campaigns():
    if session.get("user_id"):
        user_id = session["user_id"]
        user = User.query.filter_by(user_id=user_id).first()
        base_url = request.url_root
        headers = {'Content-Type': 'application/json'}
        if user.role == "admin":
            if request.method == "GET":
                args = request.args.to_dict()
                cards = requests.get(base_url + "/api/campaign", headers=headers, json={}).json()
                campaigns = requests.get(base_url + "/api/campaign", headers=headers, json=args).json()
                total_sponsors = len(Sponsor.query.all())
                return render_template("admin/campaigns.html", user=user, active_page="campaigns", campaigns=campaigns, id_to_sponsor=id_to_sponsor, total_sponsors=total_sponsors,
                                       campaign_distribution_chart=campaign_distribution_chart(), flagged_campaign_chart=flagged_campaign_chart(),
                                       private_campaign_chart=private_campaign_chart(), query=args, campaign_const=cards, converter=my_converter)
            elif request.method == "POST":
                if request.form["_method"] == "FLAG":
                    data = request.form.to_dict()
                    campaign = Campaign.query.get(data["campaign_id"])
                    campaign.flagged = "True"
                    campaign_flagged(campaign)
                    db.session.commit()
                    flash("Campaign flagged successfully!", "danger")
                    return redirect(url_for("dashboard_bp.campaigns"))
                elif request.form["_method"] == "UNFLAG":
                    data = request.form.to_dict()
                    campaign = Campaign.query.get(data["campaign_id"])
                    campaign.flagged = "False"
                    campaign_unflagged(campaign)
                    db.session.commit()
                    flash("Campaign unflagged successfully!", "success")
                    return redirect(url_for("dashboard_bp.campaigns"))

                elif request.form["_method"] == "DELETE":
                    data = request.form.to_dict()
                    campaign = Campaign.query.get(data["campaign_id"])
                    db.session.delete(campaign)
                    campaign_deleted(campaign)
                    db.session.commit()
                    flash("Campaign deleted successfully!", "danger")
                    return redirect(url_for("dashboard_bp.campaigns"))


        elif user.role == "influencer":
            influencer_id = Influencer.query.filter_by(user_id=user_id).first().influencer_id
            if request.method == "GET":
                args = request.args.to_dict()
                campaigns = requests.get(base_url + "/api/campaign", headers=headers, json=args).json()
                notifications = Notification.query.filter_by(user_id=user_id).order_by(Notification.timestamp.desc()).all()
                return render_template("influencer/campaigns.html", user=user, active_page="campaigns", query=args, campaigns=campaigns, id_to_sponsor=id_to_sponsor,
                                       notifications=notifications, time_converter=time_converter)
            elif request.method == "POST":
                headers = {'Content-Type': 'application/json'}
                if request.form["_method"] == "POST":
                    ad_request = request.form.to_dict()
                    ad_request["influencer_id"] = influencer_id
                    ad_request["initiator"] = "influencer"
                    requests.post(base_url + "/api/ad-request", json=ad_request, headers=headers)
                    flash("AdRequest sent successfully!", "success")
                    return redirect(url_for("dashboard_bp.ad_requests"))
                elif request.form["_method"] == "MARKREAD":
                    data = request.form.to_dict()
                    notification = Notification.query.get(data["notification_id"])
                    db.session.delete(notification)
                    db.session.commit()
                    flash("Notification marked as read successfully!", "success")
                    return redirect(url_for("dashboard_bp.campaigns"))

        elif user.role == "sponsor":
            sponsor_id = Sponsor.query.filter_by(user_id=user_id).first().sponsor_id
            query = Campaign.query.filter_by(sponsor_id=sponsor_id).filter(Campaign.flagged == 'False')
            if request.method == "GET":
                args = request.args.to_dict()
                if args:
                    if args['name'] is not None and args['name'] != "":
                        query = query.filter(Campaign.name.ilike(f"%{args['name']}%"))
                    if args['visibility'] is not None and args['visibility'] != "":
                        query = query.filter(Campaign.visibility.ilike(f"%{args['visibility']}%"))
                    if args['budget'] is not None and args['budget'] != "":
                        query = query.filter(Campaign.budget >= int(args['budget']))
                campaigns = query.all()
                notifications = Notification.query.filter_by(user_id=user_id).order_by(Notification.timestamp.desc()).all()
                return render_template("sponsor/campaigns.html", user=user, active_page="campaigns", campaigns=campaigns, id_to_sponsor=id_to_sponsor, query=args, notifications=notifications, time_converter=time_converter)
            elif request.method == "POST":
                if request.form["_method"] == "POST":
                    campaign = request.form.to_dict()
                    campaign['sponsor_id'] = sponsor_id
                    requests.post(base_url + "/api/campaign", json=campaign, headers=headers)
                    flash("Campaign created successfully!", "success")
                    return redirect(url_for("dashboard_bp.campaigns"))
                elif request.form["_method"] == "PUT":
                    campaign = request.form.to_dict()
                    campaign_id = campaign.pop('campaign_id')
                    campaign['sponsor_id'] = sponsor_id
                    requests.put(base_url + "/api/campaign/" + campaign_id, json=campaign, headers=headers)
                    flash("Campaign updated successfully!", "success")
                    return redirect(url_for("dashboard_bp.campaigns"))
                elif request.form["_method"] == "DELETE":
                    campaign = request.form.to_dict()
                    campaign_id = campaign.pop('campaign_id')
                    requests.delete(base_url + "/api/campaign/" + campaign_id)
                    flash("Campaign deleted successfully!", "danger")
                    return redirect(url_for("dashboard_bp.campaigns"))
                elif request.form["_method"] == "ADPOST":
                    ad_request = request.form.to_dict()
                    ad_request["sponsor_id"] = sponsor_id
                    ad_request["initiator"] = "sponsor"
                    requests.post(base_url + "/api/ad-request", json=ad_request, headers=headers)
                    flash("AdRequest sent successfully!", "success")
                    return redirect(url_for("dashboard_bp.ad_requests"))
                elif request.form["_method"] == "MARKREAD":
                    data = request.form.to_dict()
                    notification = Notification.query.get(data["notification_id"])
                    db.session.delete(notification)
                    db.session.commit()
                    flash("Notification marked as read successfully!", "success")
                    return redirect(url_for("dashboard_bp.campaigns"))
        else:
            return redirect(url_for("auth_bp.login"))
    else:
        return redirect(url_for("auth_bp.login"))

@dashboard_bp.route("/dashboard/profile", methods=["GET", "POST", "PUT", "DELETE"])
def profile():
    if session.get("user_id"):
        user_id = session["user_id"]
        user = User.query.filter_by(user_id=user_id).first()
        base_url = request.url_root
        if user.role == "influencer":
            influencer_id = Influencer.query.filter_by(user_id=user_id).first().influencer_id
            influencer = requests.get(base_url + "/api/search_influencerid/" + str(influencer_id)).json()
            notifications = Notification.query.filter_by(user_id=user_id).order_by(Notification.timestamp.desc()).all()
            if request.method == "GET":
                message = session.pop("message", None)
                def checker(niche):
                    if influencer['niche'] is not None:
                        return True if niche in influencer['niche'] else False
                    return False
                return render_template("influencer/profile.html", user=influencer, active_page="profile", checker=checker, message=message, converter=my_converter,
                                       notifications=notifications, time_converter=time_converter)
            elif request.method == "POST":
                headers = {'Content-Type': 'application/json'}
                base_url = request.url_root
                if request.form["_method"] == "PUT1":
                    profile = request.form.to_dict()
                    profile_picture = request.files["profile_picture"]
                    if profile_picture:
                        file_format = profile_picture.filename.split(".")[-1]
                        filename = secure_filename(f"{user.username}.{file_format}")
                        filepath = os.path.join(NoctiWave.config['UPLOAD_FOLDER'], filename)
                        profile_picture.save(filepath)
                        profile["profile_picture"] = filename
                    lautu = requests.post(base_url + "/api/search_influencerid/" + str(influencer_id), json=profile, headers=headers)
                    session["message"] = lautu.json()
                    return redirect(url_for("dashboard_bp.profile"))
                elif request.form["_method"] == "PUT2":
                    niches = request.form.getlist('niches')
                    profile = request.form.to_dict()
                    profile['niches'] = niches
                    lautu = requests.post(base_url + "/api/search_influencerid/" + str(influencer_id), json=profile, headers=headers)
                    session["message"] = lautu.json()
                    return redirect(url_for("dashboard_bp.profile"))
                elif request.form["_method"] == "PUT3":
                    influence = request.form.to_dict()
                    lautu = requests.put(base_url + "/api/search_influencerid/" + str(influence['influence_id']), json=influence, headers=headers)
                    session["message"] = lautu.json()
                    return redirect(url_for("dashboard_bp.profile"))
                elif request.form["_method"] == "DELETE":
                    influence = request.form.to_dict()
                    influence_id = influence.pop('influence_id')
                    lautu = requests.delete(base_url + "/api/search_influencerid/" + str(influence_id), json=influence, headers=headers)
                    session["message"] = lautu.json()
                    return redirect(url_for("dashboard_bp.profile"))
                elif request.form["_method"] == "DPDELETE":
                    lautu = requests.delete(base_url + "/api/search_sponsor/" + str(user_id), headers=headers)
                    session["message"] = lautu.json()
                    return redirect(url_for("dashboard_bp.profile"))
                elif request.form["_method"] == "MARKREAD":
                    data = request.form.to_dict()
                    notification = Notification.query.get(data["notification_id"])
                    db.session.delete(notification)
                    db.session.commit()
                    flash("Notification marked as read successfully!", "success")
                    return redirect(url_for("dashboard_bp.profile"))
                

        elif user.role == "sponsor":
            sponsor_id = Sponsor.query.filter_by(user_id=user_id).first().sponsor_id
            sponsor = requests.get(base_url + "/api/search_sponsor/" + str(sponsor_id)).json()
            if request.method == "GET":
                message = session.pop("message", None)
                notifications = Notification.query.filter_by(user_id=user_id).order_by(Notification.timestamp.desc()).all()
                return render_template("sponsor/profile.html", user=sponsor, active_page="profile", message=message, notifications=notifications, time_converter=time_converter)
            elif request.method == "POST":
                headers = {'Content-Type': 'application/json'}
                base_url = request.url_root
                if request.form["_method"] == "PUT1":
                    profile = request.form.to_dict()
                    profile_picture = request.files["profile_picture"]
                    if profile_picture:
                        file_format = profile_picture.filename.split(".")[-1]
                        filename = secure_filename(f"{user.username}.{file_format}")
                        filepath = os.path.join(NoctiWave.config['UPLOAD_FOLDER'], filename)
                        profile_picture.save(filepath)
                        profile["profile_picture"] = filename
                    lautu = requests.put(base_url + "/api/search_sponsor/" + str(sponsor_id), json=profile, headers=headers)
                    session["message"] = lautu.json()
                    return redirect(url_for("dashboard_bp.profile"))
                elif request.form["_method"] == "PUT2":
                    profile = request.form.to_dict()
                    lautu = requests.put(base_url + "/api/search_sponsor/" + str(sponsor_id), json=profile, headers=headers)
                    session["message"] = lautu.json()
                    return redirect(url_for("dashboard_bp.profile"))
                elif request.form["_method"] == "DPDELETE":
                    lautu = requests.delete(base_url + "/api/search_sponsor/" + str(user_id), headers=headers)
                    session["message"] = lautu.json()
                    return redirect(url_for("dashboard_bp.profile"))
                elif request.form["_method"] == "MARKREAD":
                    data = request.form.to_dict()
                    notification = Notification.query.get(data["notification_id"])
                    db.session.delete(notification)
                    db.session.commit()
                    flash("Notification marked as read successfully!", "success")
                    return redirect(url_for("dashboard_bp.profile"))
        else:
            return redirect(url_for("auth_bp.login"))
    else:
        return redirect(url_for("auth_bp.login"))
    

@dashboard_bp.route("/dashboard/ad-requests", methods=["GET", "POST", "PUT", "DELETE"])
def ad_requests():
    if session.get("user_id"):
        user_id = session["user_id"]
        user = User.query.filter_by(user_id=user_id).first()
        if user.role == "admin":
            if request.method == "GET":
                ad_requests = AdRequest.query.all()
                negotiations = Negotiation.query.all()
                return render_template("admin/ad-requests.html", user=user, active_page="ad-requests", ad_requests=ad_requests, negotiations=negotiations,
                                       ad_status_chart=ad_status_chart(), flagged_ad_chart=flagged_ad_chart(), ad_distribution_chart=ad_distribution_chart())
            elif request.method == "POST":
                if request.form["_method"] == "FLAG":
                    data = request.form.to_dict()
                    ad_request = AdRequest.query.get(data["ad_request_id"])
                    ad_request.flagged = "True"
                    sponsor_ad_request_flagged(ad_request)
                    influencer_ad_request_flagged(ad_request)
                    db.session.commit()
                    flash("AdRequest flagged successfully!", "danger")
                    return redirect(url_for("dashboard_bp.ad_requests"))
                elif request.form["_method"] == "UNFLAG":
                    data = request.form.to_dict()
                    ad_request = AdRequest.query.get(data["ad_request_id"])
                    ad_request.flagged = "False"
                    sponsor_ad_request_unflagged(ad_request)
                    influencer_ad_request_unflagged(ad_request)
                    db.session.commit()
                    flash("AdRequest unflagged successfully!", "success")
                    return redirect(url_for("dashboard_bp.ad_requests"))
                elif request.form["_method"] == "DELETE":
                    data = request.form.to_dict()
                    ad_request = AdRequest.query.get(data["ad_request_id"])
                    negotiation = Negotiation.query.filter_by(ad_request_id=data["ad_request_id"]).first()
                    if negotiation:
                        db.session.delete(negotiation)
                    db.session.delete(ad_request)
                    sponsor_ad_request_deleted(ad_request)
                    influencer_ad_request_deleted(ad_request)
                    db.session.commit()
                    flash("AdRequest deleted successfully!", "danger")
                    return redirect(url_for("dashboard_bp.ad_requests"))

        elif user.role == "influencer":
            influencer_id = Influencer.query.filter_by(user_id=user_id).first().influencer_id
            if request.method == "GET":
                ad_requests = AdRequest.query.filter_by(influencer_id=influencer_id).all()
                negotiations = Negotiation.query.join(AdRequest).filter(AdRequest.influencer_id==influencer_id).all()
                notifications = Notification.query.filter_by(user_id=user_id).order_by(Notification.timestamp.desc()).all()
                return render_template("influencer/ad-requests.html", user=user, active_page="ad-requests", ad_requests=ad_requests, negotiations=negotiations, id_to_sponsor=id_to_sponsor,
                                       id_to_influencer=id_to_influencer , id_to_campaign=id_to_campaign, notifications=notifications, time_converter=time_converter)
            elif request.method == "POST":
                headers = {'Content-Type': 'application/json'}
                base_url = request.url_root
                if request.form["_method"] == "POST":
                    ad_request = request.form.to_dict()
                    ad_request["influencer_id"] = influencer_id
                    ad_request["initiator"] = "influencer"
                    requests.post(base_url + "/api/ad-request", json=ad_request, headers=headers)
                    flash("AdRequest sent successfully!", "success")
                    return redirect(url_for("dashboard_bp.ad_requests"))
                elif request.form["_method"] == "PUT":
                    ad_request = request.form.to_dict()
                    ad_request_id = ad_request.pop("ad_request_id")
                    requests.put(base_url + "/api/ad-request/" + ad_request_id, json=ad_request, headers=headers)
                    flash("AdRequest updated successfully!", "success")
                    return redirect(url_for("dashboard_bp.ad_requests"))
                elif request.form["_method"] == "DELETE":
                    ad_request = request.form.to_dict()
                    ad_request_id = ad_request.pop("ad_request_id")
                    requests.delete(base_url + "/api/ad-request/" + ad_request_id)
                    flash("AdRequest deleted successfully!", "danger")
                    return redirect(url_for("dashboard_bp.ad_requests"))
                elif request.form["_method"] == "ACCEPT":
                    ad_request = request.form.to_dict()
                    ad_request_id = ad_request.pop("ad_request_id")
                    ad_request = {"status": "Approved"}
                    requests.put(base_url + "/api/ad-request/" + ad_request_id, json=ad_request, headers=headers)
                    flash("AdRequest has been approved successfully!", "success")
                    return redirect(url_for("dashboard_bp.ad_requests"))
                elif request.form["_method"] == "REJECT":
                    ad_request = request.form.to_dict()
                    ad_request_id = ad_request.pop("ad_request_id")
                    ad_request = {"status": "Rejected"}
                    requests.put(base_url + "/api/ad-request/" + ad_request_id, json=ad_request, headers=headers)
                    flash("AdRequest has been rejected successfully!", "danger")
                    return redirect(url_for("dashboard_bp.ad_requests"))
                elif request.form["_method"] == "NEGOTIATE":
                    negotiation = request.form.to_dict()
                    requests.post(base_url + "/api/negotiation", json=negotiation, headers=headers)
                    flash("Negotiation request sent successfully!", "success")
                    return redirect(url_for("dashboard_bp.ad_requests"))
                elif request.form["_method"] == "UPDATENEGO" or request.form["_method"] == "NEGOBACK":
                    negotiation = request.form.to_dict()
                    negotiation_id = negotiation.pop("negotiation_id")
                    requests.put(base_url + "/api/negotiation/" + negotiation_id, json=negotiation, headers=headers)
                    flash("Negotiation request updated successfully!", "success")
                    return redirect(url_for("dashboard_bp.ad_requests"))
                elif request.form["_method"] == "NEGODEL":
                    negotiation = request.form.to_dict()
                    negotiation_id = negotiation.pop("negotiation_id")
                    requests.delete(base_url + "/api/negotiation/" + negotiation_id, headers=headers)
                    flash("Negotiation request deleted successfully!", "danger")
                    return redirect(url_for("dashboard_bp.ad_requests"))
                elif request.form["_method"] == "MARKREAD":
                    data = request.form.to_dict()
                    notification = Notification.query.get(data["notification_id"])
                    db.session.delete(notification)
                    db.session.commit()
                    flash("Notification marked as read successfully!", "success")
                    return redirect(url_for("dashboard_bp.ad_requests"))


        elif user.role == "sponsor":
            sponsor_id = Sponsor.query.filter_by(user_id=user_id).first().sponsor_id
            ad_requests = AdRequest.query.filter_by(sponsor_id=sponsor_id).all()
            campaigns = Campaign.query.filter_by(sponsor_id=sponsor_id).all()
            notifications = Notification.query.filter_by(user_id=user_id).order_by(Notification.timestamp.desc()).all()
            if request.method == "GET":
                negotiations = Negotiation.query.join(AdRequest).filter(AdRequest.sponsor_id==sponsor_id).all()
                return render_template("sponsor/ad-requests.html", user=user, active_page="ad-requests", ad_requests=ad_requests, negotiations=negotiations ,id_to_influencer=id_to_influencer, id_to_campaign=id_to_campaign, campaigns=campaigns,
                                       notifications=notifications, time_converter=time_converter)
            elif request.method == "POST":
                headers = {'Content-Type': 'application/json'}
                base_url = request.url_root
                if request.form["_method"] == "POST":
                    ad_request = request.form.to_dict()
                    ad_request["sponsor_id"] = sponsor_id
                    ad_request["initiator"] = "sponsor"
                    requests.post(base_url + "/api/ad-request", json=ad_request, headers=headers)
                    flash("AdRequest sent successfully!", "success")
                    return redirect(url_for("dashboard_bp.ad_requests"))
                elif request.form["_method"] == "PUT":
                    ad_request = request.form.to_dict()
                    ad_request_id = ad_request.pop("ad_request_id")
                    requests.put(base_url + "/api/ad-request/" + ad_request_id, json=ad_request, headers=headers)
                    flash("AdRequest updated successfully!", "success")
                    return redirect(url_for("dashboard_bp.ad_requests"))
                elif request.form["_method"] == "DELETE":
                    ad_request = request.form.to_dict()
                    ad_request_id = ad_request.pop("ad_request_id")
                    requests.delete(base_url + "/api/ad-request/" + ad_request_id)
                    flash("AdRequest deleted successfully!", "danger")
                    return redirect(url_for("dashboard_bp.ad_requests"))
                elif request.form["_method"] == "ACCEPT":
                    ad_request = request.form.to_dict()
                    ad_request_id = ad_request.pop("ad_request_id")
                    ad_request = {"status": "Approved"}
                    requests.put(base_url + "/api/ad-request/" + ad_request_id, json=ad_request, headers=headers)
                    flash("AdRequest has been approved successfully!", "success")
                    return redirect(url_for("dashboard_bp.ad_requests"))
                elif request.form["_method"] == "REJECT":
                    ad_request = request.form.to_dict()
                    ad_request_id = ad_request.pop("ad_request_id")
                    ad_request = {"status": "Rejected"}
                    requests.put(base_url + "/api/ad-request/" + ad_request_id, json=ad_request, headers=headers)
                    flash("AdRequest has been rejected successfully!", "danger")
                    return redirect(url_for("dashboard_bp.ad_requests"))
                elif request.form["_method"] == "NEGOTIATE":
                    ad_request = request.form.to_dict()
                    requests.post(base_url + "/api/negotiation", json=ad_request, headers=headers)
                    flash("Negotiation request sent successfully!", "success")
                    return redirect(url_for("dashboard_bp.ad_requests"))
                elif request.form["_method"] == "UPDATENEGO" or request.form["_method"] == "NEGOBACK":
                    negotiation = request.form.to_dict()
                    negotiation_id = negotiation.pop("negotiation_id")
                    requests.put(base_url + "/api/negotiation/" + negotiation_id, json=negotiation, headers=headers)
                    flash("Negotiation request updated successfully!", "success")
                    return redirect(url_for("dashboard_bp.ad_requests"))
                elif request.form["_method"] == "NEGODEL":
                    negotiation = request.form.to_dict()
                    negotiation_id = negotiation.pop("negotiation_id")
                    requests.delete(base_url + "/api/negotiation/" + negotiation_id, headers=headers)
                    flash("Negotiation request deleted successfully!", "danger")
                    return redirect(url_for("dashboard_bp.ad_requests"))
                elif request.form["_method"] == "MARKREAD":
                    data = request.form.to_dict()
                    notification = Notification.query.get(data["notification_id"])
                    db.session.delete(notification)
                    db.session.commit()
                    flash("Notification marked as read successfully!", "success")
                    return redirect(url_for("dashboard_bp.ad_requests"))
                
        else:
            return redirect(url_for("auth_bp.login"))
    else:
        return redirect(url_for("auth_bp.login"))


@dashboard_bp.route("/dashboard/influencers", methods=["GET", "POST", "PUT", "DELETE"])
def influencers():
    if session.get("user_id"):
        user_id = session["user_id"]
        user = User.query.filter_by(user_id=user_id).first()
        headers = {'Content-Type': 'application/json'}
        base_url = request.url_root
        if user.role == "admin":
            if request.method == "GET":
                cards = requests.get(base_url + "/api/search_influencerid", headers=headers, json={}).json()
                query = request.args.to_dict()
                influencers = requests.get(base_url + "/api/search_influencerid", headers=headers, json=query).json()
                ad_requests = AdRequest.query.all()
                return render_template("admin/influencers.html", user=user, active_page="influencers", influencers=influencers, converter=my_converter, ad_requests=ad_requests,
                                       influencer_distribution_chart=influencer_distribution_chart(), flagged_influencer_chart=flagged_influencer_chart(),
                                       influencer_platform_chart=influencer_platform_chart(), query=query, cards=cards)
            elif request.method == "POST":
                if request.form["_method"] == "FLAG":
                    data = request.form.to_dict()
                    influencer = Influencer.query.get(data["influencer_id"])
                    influencer.flagged = "True"
                    user_flagged(influencer)
                    db.session.commit()
                    flash("Influencer flagged successfully!", "danger")
                    return redirect(url_for("dashboard_bp.influencers"))
                elif request.form["_method"] == "UNFLAG":
                    data = request.form.to_dict()
                    influencer = Influencer.query.get(data["influencer_id"])
                    influencer.flagged = "False"
                    user_unflagged(influencer)
                    db.session.commit()
                    flash("Influencer unflagged successfully!", "success")
                    return redirect(url_for("dashboard_bp.influencers"))
                elif request.form["_method"] == "DELETE":
                    data = request.form.to_dict()
                    user = User.query.get(data["user_id"])
                    db.session.delete(user)
                    db.session.commit()
                    flash("Influencer deleted successfully!", "danger")
                    return redirect(url_for("dashboard_bp.influencers"))


        elif user.role == "sponsor":
            sponsor_id = Sponsor.query.filter_by(user_id=user_id).first().sponsor_id
            campaigns = Campaign.query.filter_by(sponsor_id=sponsor_id).all()
            if request.method == "GET":
                query = request.args.to_dict()
                influencers = requests.get(base_url + "/api/search_influencerid", headers=headers, json=query).json()
                notifications = Notification.query.filter_by(user_id=user_id).order_by(Notification.timestamp.desc()).all()
                return render_template("sponsor/influencers.html", user=user, active_page="influencers", influencers=influencers, converter=my_converter, campaigns=campaigns, query=query,
                                       notifications=notifications, time_converter=time_converter)
            elif request.method == "POST":
                if request.form["_method"] == "POST":
                    ad_request = request.form.to_dict()
                    ad_request["sponsor_id"] = sponsor_id
                    ad_request["initiator"] = "sponsor"
                    requests.post(base_url + "/api/ad-request", json=ad_request, headers=headers)
                    flash("AdRequest sent successfully!", "success")
                    return redirect(url_for("dashboard_bp.ad_requests"))
                elif request.form["_method"] == "MARKREAD":
                    data = request.form.to_dict()
                    notification = Notification.query.get(data["notification_id"])
                    db.session.delete(notification)
                    db.session.commit()
                    flash("Notification marked as read successfully!", "success")
                    return redirect(url_for("dashboard_bp.influencers"))
        else:
            return redirect(url_for("auth_bp.login"))
    else:
        return redirect(url_for("auth_bp.login"))
    

@dashboard_bp.route("/dashboard/sponsors", methods=["GET", "POST", "PUT", "DELETE"])
def sponsors():
    if session.get("user_id"):
        user_id = session["user_id"]
        user = User.query.filter_by(user_id=user_id).first()
        headers = {'Content-Type': 'application/json'}
        base_url = request.url_root
        if user.role == "admin":
            if request.method == "GET":
                cards = Sponsor.query.all()
                query = Sponsor.query
                campaigns = Campaign.query.all()
                args = request.args.to_dict()
                if args:
                    if args['name'] is not None and args['name'] != "":
                        query = query.filter(Sponsor.company_individual_name.ilike(f"%{args['name']}%"))
                    if args['industry'] is not None and args['industry'] != "":
                        query = query.filter(Sponsor.industry.ilike(f"%{args['industry']}%"))
                    if args['budget'] is not None and args['budget'] != "":
                        query = query.filter(Sponsor.budget >= int(args['budget']))
                    if args['flagged'] is not None and args['flagged'] != "":
                        query = query.filter(Sponsor.flagged==args['flagged'])
                sponsors = query.all()
                return render_template("admin/sponsors.html", user=user, active_page="sponsors", sponsor_const=cards, sponsors=sponsors, campaigns=campaigns,
                                       sponsor_distribution_chart=sponsor_distribution_chart(), flagged_sponsor_chart=flagged_sponsor_chart(),
                                       sponsor_budget_chart=sponsor_budget_chart(), query=args)
            elif request.method == "POST":
                if request.form["_method"] == "FLAG":
                    data = request.form.to_dict()
                    sponsor = Sponsor.query.get(data["sponsor_id"])
                    sponsor.flagged = "True"
                    user_flagged(sponsor)
                    db.session.commit()
                    flash("Sponsor flagged successfully!", "danger")
                    return redirect(url_for("dashboard_bp.sponsors"))
                elif request.form["_method"] == "UNFLAG":
                    data = request.form.to_dict()
                    sponsor = Sponsor.query.get(data["sponsor_id"])
                    sponsor.flagged = "False"
                    user_unflagged(sponsor)
                    db.session.commit()
                    flash("Sponsor unflagged successfully!", "success")
                    return redirect(url_for("dashboard_bp.sponsors"))
                elif request.form["_method"] == "DELETE":
                    data = request.form.to_dict()
                    user = User.query.get(data["user_id"])
                    db.session.delete(user)
                    db.session.commit()
                    flash("Sponsor deleted successfully!", "danger")
                    return redirect(url_for("dashboard_bp.sponsors"))
                
        elif user.role == "influencer":
            influencer_id = Influencer.query.filter_by(user_id=user_id).first().influencer_id
            if request.method == "GET":
                query = Sponsor.query
                campaigns = Campaign.query.all()
                args = request.args.to_dict()
                if args:
                    if args['name'] is not None and args['name'] != "":
                        query = query.filter(Sponsor.company_individual_name.ilike(f"%{args['name']}%"))
                    if args['industry'] is not None and args['industry'] != "":
                        query = query.filter(Sponsor.industry.ilike(f"%{args['industry']}%"))
                    if args['budget'] is not None and args['budget'] != "":
                        query = query.filter(Sponsor.budget >= int(args['budget']))
                sponsors = query.all()
                notifications = Notification.query.filter_by(user_id=user_id).order_by(Notification.timestamp.desc()).all()
                return render_template("influencer/sponsors.html", user=user, active_page="sponsors", sponsors=sponsors, campaigns=campaigns, query=args, notifications=notifications, time_converter=time_converter)
            
            elif request.method == "POST":
                if request.form["_method"] == "POST":
                    ad_request = request.form.to_dict()
                    ad_request["influencer_id"] = influencer_id
                    ad_request["initiator"] = "influencer"
                    requests.post(base_url + "/api/ad-request", json=ad_request, headers=headers)
                    flash("AdRequest sent successfully!", "success")
                    return redirect(url_for("dashboard_bp.ad_requests"))
                elif request.form["_method"] == "MARKREAD":
                    data = request.form.to_dict()
                    notification = Notification.query.get(data["notification_id"])
                    db.session.delete(notification)
                    db.session.commit()
                    flash("Notification marked as read successfully!", "success")
                    return redirect(url_for("dashboard_bp.sponsors"))
        else:
            return redirect(url_for("auth_bp.login"))
    else:
        return redirect(url_for("auth_bp.login"))


@dashboard_bp.route("/dashboard/payments", methods=["GET", "POST"])
def payments():
    if session.get("user_id"):
        user_id = session["user_id"]
        user = User.query.filter_by(user_id=user_id).first()
        if user.role == "admin":
            ad_requests = AdRequest.query.filter(AdRequest.status=="Approved").all()
            return render_template("admin/payments.html", ad_requests=ad_requests, user=user, active_page='payments')

        if user.role == "influencer":
            if request.method == "GET":
                influencer_id = Influencer.query.filter_by(user_id=user_id).first().influencer_id
                ad_requests = AdRequest.query.filter(AdRequest.status=="Approved").filter(AdRequest.influencer_id==influencer_id).all()
                notifications = Notification.query.filter_by(user_id=user_id).order_by(Notification.timestamp.desc()).all()
                return render_template("influencer/payments.html", ad_requests=ad_requests, user=user, active_page="payments", notifications=notifications, time_converter=time_converter)
            elif request.method == "POST":
                if request.form["_method"] == "MARKREAD":
                    data = request.form.to_dict()
                    notification = Notification.query.get(data["notification_id"])
                    db.session.delete(notification)
                    db.session.commit()
                    flash("Notification marked as read successfully!", "success")
                    return redirect(url_for("dashboard_bp.payments"))

        elif user.role == "sponsor":
            if request.method == "GET":
                sponsor_id = Sponsor.query.filter_by(user_id=user_id).first().sponsor_id
                ad_requests = AdRequest.query.filter(AdRequest.status=="Approved").filter(AdRequest.sponsor_id==sponsor_id).all()
                notifications = Notification.query.filter_by(user_id=user_id).order_by(Notification.timestamp.desc()).all()
                return render_template("sponsor/payments.html", user=user, active_page="payments", ad_requests=ad_requests, notifications=notifications, time_converter=time_converter)
            elif request.method == "POST":
                if request.form["_method"] == "MARKREAD":
                    data = request.form.to_dict()
                    notification = Notification.query.get(data["notification_id"])
                    db.session.delete(notification)
                    db.session.commit()
                    flash("Notification marked as read successfully!", "success")
                    return redirect(url_for("dashboard_bp.payments"))
                
        else:
            return redirect(url_for("auth_bp.login"))
    else:
        return redirect(url_for("auth_bp.login"))