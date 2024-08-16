from flask_restful import Resource, marshal_with, fields, abort, reqparse
from flask import request, jsonify
from .influencer.models import Influencer, Influence
from .sponsor.models import Sponsor
from .models import User
from .. import db, NoctiWave
from sqlalchemy import or_
import os
from werkzeug.utils import secure_filename

class InfluencerResource(Resource):
    def get(self, username_or_name=None):
        results = []
        query = User.query.filter(User.role == "influencer")

        if username_or_name:
            search_pattern = f"%{username_or_name}%"
            query = query.filter(or_(User.username.ilike(search_pattern), User.name.ilike(search_pattern)))

        influencers = query.all()

        for influencer in influencers:
            more_info = Influencer.query.filter_by(user_id=influencer.user_id).filter(Influencer.flagged=='False').first()
            if more_info:
                results.append({
                    "user_id": influencer.user_id,
                    "influencer_id": more_info.influencer_id,
                    "name": influencer.name,
                    "username": influencer.username,
                    "email": influencer.email,
                    "profile_picture": influencer.profile_picture,
                    "role": influencer.role,
                    "category": more_info.category,
                    "niche": more_info.niche,
                    "bio": more_info.bio
                })

        return jsonify(results if results else {"message": "No result found"})
    
platform_fields = {
    "influence_id": fields.Integer(attribute='influence_id'),
    "platform": fields.String(attribute='platform'),
    "reach": fields.Integer(attribute='reach'),
    "url": fields.String(attribute='url')
}

resource_fields_influencer = {
    "user_id": fields.Integer(attribute='user.user_id'),
    "username": fields.String(attribute='user.username'),
    "name": fields.String(attribute='user.name'),
    "email": fields.String(attribute='user.email'),
    "role": fields.String(attribute='user.role'),
    "profile_picture": fields.String(attribute='user.profile_picture'),
    "influencer_id": fields.Integer,
    "category": fields.String,
    "flagged": fields.String,
    "niche": fields.String,
    "bio": fields.String,
    "platforms": fields.List(fields.Nested(platform_fields))
}

class InfluencerSearch(Resource):
    @marshal_with(resource_fields_influencer)
    def get(self, influencer_id=None):
        if influencer_id:
            influencer = Influencer.query\
            .join(User)\
            .filter(Influencer.influencer_id == influencer_id)\
            .first()
            if influencer:
                influences = Influence.query.filter_by(influencer_id=influencer_id)
                influencer.platforms = influences 
                return influencer, 200
            else:
                abort(404, message="Influencer not found")

        #My filter
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str)
        parser.add_argument('category', type=str)
        parser.add_argument('platform', type=str)
        parser.add_argument('reach', type=int)
        parser.add_argument('flagged', type=str)
        args = parser.parse_args()

        query = Influencer.query.join(User).outerjoin(Influence)
        if args['name'] is not None and args['name'] != "":
            query = query.filter(User.name.ilike(f"%{args['name']}%"))
        if args['category'] is not None and args['category'] != "":
            query = query.filter(Influencer.category.ilike(f"%{args['category']}%"))
        if args['platform'] is not None and args['platform'] != "":
            query = query.filter(Influence.platform.ilike(f"%{args['platform']}%"))
        if args['reach'] is not None and args['reach'] != 0:
            query = query.filter(Influence.reach >= int(args['reach']))
        if args['flagged'] is not None and args['flagged'] != "":
            query = query.filter(Influencer.flagged.ilike(f"%{args['flagged']}%"))


        influencers = query.all()

        for influencer in influencers:
            influences = Influence.query.filter_by(influencer_id=influencer.influencer_id).all()
            platforms = list()
            for influence in influences:
                platforms.append(influence)
            influencer.platforms = platforms
        return influencers, 200
    
    def post(self, influencer_id):
        influencer = Influencer.query.get(influencer_id)
        if influencer_id:
            parser = reqparse.RequestParser()
            parser.add_argument("name", type=str)
            parser.add_argument("profile_picture")
            parser.add_argument("username", type=str)
            parser.add_argument("email", type=str)
            parser.add_argument("category", type=str)
            parser.add_argument("bio", type=str)
            parser.add_argument("niches", type=list, location='json')
            parser.add_argument("platform")
            parser.add_argument("reach")
            parser.add_argument("url")

            args = parser.parse_args()

            if args["name"] is not None:
                influencer.user.name = args["name"]

            if args["profile_picture"] is not None:
                influencer.user.profile_picture = args["profile_picture"]

            if args["username"] is not None:
                allowed = "-_."
                args["username"] = args["username"].lower()
                if all(char.isalnum() or char in allowed for char in args["username"]):
                    user = User.query.filter_by(username=args["username"]).first()
                    influencer = Influencer.query.get(influencer_id)
                    if user and user.username != influencer.user.username:
                        return {"message": "Username already taken, Please try another."}, 200
                    else:
                        influencer.user.username = args["username"]
                else:
                    return {"message": "Username contains invalid characters."}, 200

            if args["email"] is not None:
                args["email"] = args["email"].lower()
                user = User.query.filter_by(email=args["email"]).first()
                if user and user.email != influencer.user.email:
                    return {"message": "Email Address is already in use."}, 200
                else:
                    influencer.user.email = args["email"]

            if args["category"] is not None:
                influencer.category = args["category"]

            if args["bio"] is not None:
                influencer.bio = args["bio"]

            if args["niches"] is not None:
                influencer.niche = ', '.join(args["niches"])

            if args["platform"] != "" and args["reach"] != "" and args["url"] != "":
                if args["platform"] is not None and args["reach"] is not None and args["url"] is not None:
                    influences = Influence.query.filter_by(influencer_id=influencer_id).all()
                    checker = True
                    for each in influences:
                        if each.platform == args["platform"]:
                            checker = False
                            break
                    if checker:
                        influence = Influence(influencer_id=influencer_id,
                                        platform=args["platform"],
                                        reach=args["reach"],
                                        url=args["url"])
                        db.session.add(influence)
                    else:
                        return {'message': 'Platform already exist.'}, 200
            db.session.commit()
            return {'message': 'Profile updated successfully!'}, 200
        
        else:
            abort(404, message="Influencer not found")


    def put(self, influencer_id):
        influence = Influence.query.get(influencer_id)
        parser = reqparse.RequestParser()
        parser.add_argument("platform")
        parser.add_argument("reach")
        parser.add_argument("url")
        args = parser.parse_args()
        if influence:
            influence.platform = args["platform"]
            influence.reach = args["reach"]
            influence.url = args["url"]
            db.session.commit()
            return {'message': 'Platform updated successfully!'}, 200
        else:
            abort(404, message="Platform not found")


    def delete(self, influencer_id):
        influence = Influence.query.get(influencer_id)
        if influence:
            db.session.delete(influence)
            db.session.commit()
            return {'message': 'Platform deleted successfully!'}, 200
        else:
            abort(404, message="Platform not found")


# Sponsor API 

sponsor_fields = {
    "username": fields.String(attribute='user.username'),
    "name": fields.String(attribute='user.name'),
    "role": fields.String(attribute='user.role'),
    "email": fields.String(attribute='user.email'),
    "profile_picture": fields.String(attribute='user.profile_picture'),
    "website": fields.String(attribute='website'),
    "company_individual_name": fields.String(attribute='company_individual_name'),
    "industry": fields.String(attribute='industry'),
    "budget": fields.Float(attribute='budget'),
}

class SponsorResource(Resource):
    @marshal_with(sponsor_fields)
    def get(self, sponsor_id=None):
        if sponsor_id:
            sponsor = Sponsor.query.get(sponsor_id)
            if sponsor:
                return sponsor, 200
            else:
                abort(404, message="Sponsor not found")
        sponsors = Sponsor.query.join(User).all()
        return sponsors, 200

    def put(self, sponsor_id):
        sponsor = Sponsor.query.get(sponsor_id)
        if sponsor:
            parser = reqparse.RequestParser()
            parser.add_argument("name", type=str)
            parser.add_argument("profile_picture")
            parser.add_argument("username", type=str)
            parser.add_argument("email", type=str)
            parser.add_argument("website", type=str)
            parser.add_argument("company_individual_name", type=str)
            parser.add_argument("industry", type=str)
            parser.add_argument("budget", type=float)
            args = parser.parse_args()

            if args["name"] is not None:
                sponsor.user.name = args["name"]

            if args["profile_picture"] is not None:
                sponsor.user.profile_picture = args["profile_picture"]

            if args["username"] is not None:
                allowed = "-_."
                args["username"] = args["username"].lower()
                if all(char.isalnum() or char in allowed for char in args["username"]):
                    user = User.query.filter_by(username=args["username"]).first()
                    if user and user.username != sponsor.user.username:
                        return {"message": "Username already taken, Please try another."}, 200
                    else:
                        sponsor.user.username = args["username"]
                else:
                    return {"message": "Username contains invalid characters."}, 200

            if args["email"] is not None:
                args["email"] = args["email"].lower()
                user = User.query.filter_by(email=args["email"]).first()
                if user and user.email != sponsor.user.email:
                    return {"message": "Email Address is already in use."}, 200
                else:
                    sponsor.user.email = args["email"]

            if args["website"] is not None:
                sponsor.website = args["website"]

            if args["company_individual_name"]:
                sponsor.company_individual_name = args["company_individual_name"]

            if args["industry"] is not None:
                sponsor.industry = args["industry"]

            if args["budget"] is not None:
                sponsor.budget = args["budget"]

            db.session.commit()
            return {"message": "Profile updated successfully!"}, 200
        
        else:
            abort(404, message="Sponsor not found")

    
    def delete(self, sponsor_id):
        user = User.query.get(sponsor_id)
        user.profile_picture = 'user_default.svg'
        db.session.commit()
        return {"message": "Profile picture removed successfully!"}, 200

