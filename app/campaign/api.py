# /NoctiWave/app/campaign/api.py

from .. import db
from flask_restful import Resource, reqparse, fields, marshal_with, abort
from flask import jsonify
from ..user.sponsor.models import Sponsor
from ..user.models import User
from .models import Campaign
from datetime import datetime

resource_fields = {
        "campaign_id": fields.Integer,
        "sponsor_id": fields.Integer,
        "name": fields.String,
        "sponsor_name": fields.String(attribute='sponsor.company_individual_name'),
        "sponsor_username": fields.String(attribute='sponsor.user.username'),
        "sponsor_profile": fields.String(attribute='sponsor.user.profile_picture'),
        "flagged": fields.String,
        "description" : fields.String,
        "start_date" : fields.String,
        "end_date" : fields.String,
        "budget" : fields.Float,
        "visibility" : fields.String,
        "goals" : fields.String
    }

class CampaignResource(Resource):
    @marshal_with(resource_fields)
    def get(self, campaign_id=None):
        if campaign_id is None:
            #My filter
            parser = reqparse.RequestParser()
            parser.add_argument('name', type=str)
            parser.add_argument('sponsor_name', type=str)
            parser.add_argument('industry', type=str)
            parser.add_argument('budget', type=str)
            parser.add_argument('flagged', type=str)
            args = parser.parse_args()
            query = db.session.query(Campaign).join(Sponsor).join(User)
            if args.get('name') is not None and args['name'] != "":
                query = query.filter(Campaign.name.ilike(f"%{args['name']}%"))
            if args.get('sponsor_name') is not None and args['sponsor_name'] != "":
                query = query.filter(Sponsor.company_individual_name.ilike(f"%{args['sponsor_name']}%"))
            if args.get('industry') is not None and args['industry'] != "":
                query = query.filter(Sponsor.industry.ilike(f"%{args['industry']}%"))
            if args['budget'] is not None and args['budget'] != "":
                query = query.filter(Campaign.budget >= int(args['budget']))
            if args.get('flagged') is not None and args['flagged'] != "":
                query = query.filter(Campaign.flagged.ilike(f"%{args['flagged']}%"))
            campaigns = query.all()
            return campaigns, 200
        elif campaign_id.isdigit():
            return self.get_by_id(int(campaign_id))
        else:
            return self.get_by_name(campaign_id)
    
    def get_by_id(self, campaign_id):
        campaign = Campaign.query.filter_by(campaign_id=campaign_id).first()
        if campaign:
            return campaign, 200
        else:
            abort(404, message="Campaign not found")
        return campaign, 200
    
    def get_by_name(self, campaign_name):
        results = []
        campaigns = Campaign.query.filter(Campaign.name.ilike(f"%{campaign_name}%")).filter(Campaign.flagged=='False').all()
        for campaign in campaigns:
            more_info = Sponsor.query.filter_by(sponsor_id=campaign.sponsor_id).first()
            results.append({
                "campaign_id": campaign.campaign_id,
                "sponsor_id": campaign.sponsor_id,
                "name": campaign.name,
            })

        return results, 200


    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("sponsor_id", type=int, required=True)
        parser.add_argument("name", type=str, required=True)
        parser.add_argument("description", type=str, required=True)
        parser.add_argument("start_date", type=str, required=True)
        parser.add_argument("end_date", type=str, required=True)
        parser.add_argument("budget", type=float, required=True)
        parser.add_argument("visibility", type=str, required=True)
        parser.add_argument("goals", type=str, required=True)

        args = parser.parse_args()
        start_date = datetime.strptime(args["start_date"], '%Y-%m-%d').date()
        end_date = datetime.strptime(args["end_date"], '%Y-%m-%d').date()
        
        new_campaign = Campaign(sponsor_id=args["sponsor_id"], name=args["name"],
                                description=args["description"], start_date=start_date,
                                end_date=end_date, budget=args["budget"],
                                visibility=args["visibility"], goals=args["goals"])
        db.session.add(new_campaign)
        db.session.commit()
        return {'message': 'Campaign created successfully'}, 201
    

    def put(self, campaign_id):
        campaign = Campaign.query.get(campaign_id)
        if campaign:
            parser = reqparse.RequestParser()
            parser.add_argument("name", type=str)
            parser.add_argument("description", type=str)
            parser.add_argument("start_date", type=str)
            parser.add_argument("end_date", type=str)
            parser.add_argument("budget", type=float)
            parser.add_argument("visibility", type=str)
            parser.add_argument("goals", type=str)

            args = parser.parse_args()

            if args["name"] is not None:
                campaign.name = args["name"]

            if args["description"] is not None:
                campaign.description = args["description"]

            if args["start_date"] is not None:
                start_date = datetime.strptime(args["start_date"], '%Y-%m-%d').date()
                campaign.start_date = start_date

            if args["end_date"] is not None:
                end_date = datetime.strptime(args["end_date"], '%Y-%m-%d').date()
                campaign.end_date = end_date

            if args["budget"] is not None:
                campaign.budget = args["budget"]
            
            if args["visibility"] is not None:
                campaign.visibility = args["visibility"]

            if args["goals"] is not None:
                campaign.goals = args["goals"]
            
            db.session.commit()
            return {'message': 'Campaign updated successfully'}, 200
        else:
            abort(404, message="Campaign not found")

    
    def delete(self, campaign_id):
        campaign = Campaign.query.get(campaign_id)
        if campaign:
            db.session.delete(campaign)
            db.session.commit()
            return {'message': 'Campaign deleted successfully'}, 200
        else:
            abort(404, message="Campaign not found")