# /NoctiWave/app/ad_request/api.py

from flask_restful import Resource, reqparse, fields, marshal_with, abort
from datetime import datetime
from .. import db
from .models import AdRequest, Negotiation

resource_fields_adrequests = {
    "ad_request_id": fields.Integer,
    "campaign_id": fields.Integer,
    "influencer_id": fields.Integer,
    "sponsor_id": fields.Integer,
    "initiator": fields.String,
    "requirements": fields.String,
    "payment_amount": fields.Float,
    "messages": fields.String,
    "status": fields.String
}

resource_fields_negotiation = {
    "negotiation_id": fields.Integer,
    "ad_request_id": fields.Integer,
    "initiator": fields.String,
    "message": fields.String,
    "status": fields.String
}

class AdRequestResource(Resource):
    @marshal_with(resource_fields_adrequests)
    def get(self, ad_request_id=None):
        if ad_request_id:
            ad_request = AdRequest.query.get(ad_request_id)
            if ad_request:
                return ad_request, 200
            else:
                abort(404, message="AdRequest not found")
        ad_requests = AdRequest.query.all()
        return ad_requests


    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("campaign_id", type=int, required=True)
        parser.add_argument("influencer_id", type=int, required=True)
        parser.add_argument("sponsor_id", type=int, required=True)
        parser.add_argument("initiator", type=str, required=True)
        parser.add_argument("requirements", type=str, required=True)
        parser.add_argument("payment_amount", type=float, required=True)
        parser.add_argument("messages", type=str, required=True)

        args = parser.parse_args()

        new_ad_request = AdRequest(campaign_id=args["campaign_id"], influencer_id=args["influencer_id"],
                                   sponsor_id=args["sponsor_id"], initiator=args["initiator"],
                                   requirements=args["requirements"], payment_amount=args["payment_amount"],
                                   messages=args["messages"])
        db.session.add(new_ad_request)
        db.session.commit()
        return {'message': 'AdRequest created successfully'}, 201


    def put(self, ad_request_id):
        ad_request = AdRequest.query.get(ad_request_id)
        if ad_request:
            parser = reqparse.RequestParser()
            parser.add_argument("requirements", type=str)
            parser.add_argument("payment_amount", type=float)
            parser.add_argument("messages", type=str)
            parser.add_argument("status", type=str)

            args = parser.parse_args()

            if args["requirements"] is not None:
                ad_request.requirements = args["requirements"]

            if args["payment_amount"] is not None:
                ad_request.payment_amount = args["payment_amount"]

            if args["messages"] is not None:
                ad_request.messages = args["messages"]

            if args["status"] is not None:
                ad_request.status = args["status"]

            db.session.commit()
            return {'message': 'AdRequest updated successfully'}, 200
        else:
            abort(404, message="AdRequest not found")


    def delete(self, ad_request_id):
        ad_request = AdRequest.query.get(ad_request_id)
        if ad_request:
            db.session.delete(ad_request)
            db.session.commit()
            return {'message': 'AdRequest deleted successfully'}, 200
        else:
            abort(404, message="AdRequest not found")


# Negotiation API

class NegotiationResource(Resource):
    @marshal_with(resource_fields_negotiation)
    def get(self, negotiation_id=None):
        if negotiation_id:
            negotiation = Negotiation.query.get(negotiation_id)
            if negotiation:
                return negotiation, 200
            else:
                abort(404, message="Negotiation not found")
        negotiations = Negotiation.query.all()
        return negotiations


    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("ad_request_id", type=int, required=True)
        parser.add_argument("initiator", type=str, required=True)
        parser.add_argument("message", type=str, required=True)
        parser.add_argument("status", type=str, required=True)

        args = parser.parse_args()

        new_negotiation = Negotiation(ad_request_id=args["ad_request_id"], initiator=args["initiator"],
                                      message=args["message"], status=args["status"])
        db.session.add(new_negotiation)
        db.session.commit()
        return {'message': 'Negotiation initiated successfully'}, 201


    def put(self, negotiation_id):
        negotiation = Negotiation.query.get(negotiation_id)
        if negotiation:
            parser = reqparse.RequestParser()
            parser.add_argument("initiator", type=str)
            parser.add_argument("message", type=str)
            parser.add_argument("status", type=str)

            args = parser.parse_args()

            if args["initiator"] is not None:
                negotiation.initiator = args["initiator"]

            if args["message"] is not None:
                negotiation.message = args["message"]

            if args["status"] is not None:
                negotiation.status = args["status"]

            db.session.commit()
            return {'message': 'Negotiation updated successfully'}, 200
        else:
            abort(404, message="Negotiation not found")


    def delete(self, negotiation_id):
        negotiation = Negotiation.query.get(negotiation_id)
        if negotiation:
            db.session.delete(negotiation)
            db.session.commit()
            db.session.close()
            return {'message': 'Negotiation canceled successfully'}, 200
        else:
            abort(404, message="Negotiation not found")