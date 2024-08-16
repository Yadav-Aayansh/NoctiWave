# /NoctiWave/app/ad_request/management.py

from ..user.influencer.models import Influencer
from ..user.sponsor.models import Sponsor
from ..user.models import User
from ..campaign.models import Campaign

def id_to_influencer(id):
    influencer = Influencer.query.get(id)
    user_id = influencer.user_id
    user = User.query.get(user_id)
    return user.name

def id_to_campaign(id):
    campaign = Campaign.query.get(id)
    return campaign.name

def id_to_sponsor(id):
    sponsor = Sponsor.query.get(id)
    return sponsor.company_individual_name