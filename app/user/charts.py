# /NoctiWave/app/user/charts.py

from flask import Response, jsonify
from .models import User
from .sponsor.models import Sponsor
from .influencer.models import Influence, Influencer
from ..campaign.models import Campaign
from ..ad_request.models import AdRequest, Negotiation

def campaign_distribution_chart():
    categories = ["Fashion", "Beauty", "Technology", "Health & Fitness", "Travel", 
                  "Food & Beverage", "Gaming", "Sports", "Entertainment", "Home & Lifestyle"]
    counts = [0] * len(categories)

    campaigns = Campaign.query.all()

    for campaign in campaigns:
        category = campaign.sponsor.industry
        if category in categories:
            index = categories.index(category)
            counts[index] += 1

    chart_data = {
        "labels": categories,
        "datasets": [{
            "data": counts,
            "label": 'Campaign Distribution by Category',
            "backgroundColor": [
                'rgba(255, 99, 132, 0.5)',  # Red
                'rgba(54, 162, 235, 0.5)',  # Blue
                'rgba(255, 206, 86, 0.5)',  # Yellow
                'rgba(75, 192, 192, 0.5)',  # Green
                'rgba(153, 102, 255, 0.5)', # Purple
                'rgba(255, 159, 64, 0.5)',  # Orange
                'rgba(0, 255, 0, 0.5)',     # Lime
                'rgba(255, 215, 0, 0.5)',   # Gold
                'rgba(186, 85, 211, 0.5)',  # MediumOrchid
                'rgba(255, 69, 0, 0.5)'     # Red-Orange
            ]
        }]
    }

    return chart_data



def sponsor_influencer_ratio_chart():
    sponsors = Sponsor.query.all()
    influencers = Influencer.query.all()
    user_type = ["Sponsor", "Influencer"]
    counts = [len(sponsors), len(influencers)]
     
    chart_data = {
        "labels": user_type,
        "datasets": [{
            "data": counts,
            "backgroundColor": [
                'rgba(54, 162, 235, 0.5)',  # Blue
                'rgba(255, 99, 132, 0.5)'   # Red
            ],
            "borderColor": [
                'rgba(54, 162, 235, 1)',
                'rgba(255, 99, 132, 1)'
            ],
            "borderWidth": 1
        }]
    }

    return chart_data



def ad_request_status_chart():
    approved = AdRequest.query.filter_by(status='Approved').all()
    pending = AdRequest.query.filter_by(status='Pending').all()
    rejected = AdRequest.query.filter_by(status='Rejected').all()
    status = ["Approved", "Pending", "Rejected"]
    counts = [len(approved), len(pending), len(rejected)]

    chart_data = {
        "labels": status,
        "datasets": [{
            "data": counts,
            "label": "Ad Request Status",
            "backgroundColor": [
                'rgba(54, 162, 235, 0.5)',
                'rgba(255, 206, 86, 0.5)',
                'rgba(255, 99, 132, 0.5)'
            ],
            "borderColor": [
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(255, 99, 132, 1)'
            ],
            "borderWidth": 1
        }]
    }

    return chart_data


def flagged_campaign_chart():
    flagged = Campaign.query.filter_by(flagged="True").all()
    non_flagged = Campaign.query.filter_by(flagged="False").all()
    campaign_type = ["Flagged", "Non-Flagged"]
    counts = [len(flagged), len(non_flagged)]
     
    chart_data = {
        "labels": campaign_type,
        "datasets": [{
            "data": counts,
            "label": 'Flagged and Non-Flagged Campaign Ratio',
            "backgroundColor": [
                'rgba(255, 99, 132, 0.5)',
                'rgba(54, 162, 235, 0.5)'
            ],
            "borderColor": [
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
            ],
            "borderWidth": 1
        }]
    }

    return chart_data


def private_campaign_chart():
    private = Campaign.query.filter_by(visibility="Private").all()
    public = Campaign.query.filter_by(visibility="Public").all()
    campaign_type = ["Private", "Public"]
    counts = [len(private), len(public)]
     
    chart_data = {
        "labels": campaign_type,
        "datasets": [{
            "data": counts,
            "label": 'Private and Public Campaign Ratio',
            "backgroundColor": [
                'rgba(255, 206, 86, 0.5)',  # Yellow
                'rgba(75, 192, 192, 0.5)',  # Green
                ],
            "borderColor": [
                'rgba(255, 206, 86, 1)',  # Yellow
                'rgba(75, 192, 192, 1)',  # Green
            ],
            "borderWidth": 1
        }]
    }

    return chart_data


def influencer_distribution_chart():
    categories = ["Fashion", "Beauty", "Technology", "Health & Fitness", "Travel", 
                  "Food & Beverage", "Gaming", "Sports", "Entertainment", "Home & Lifestyle"]
    counts = [0] * len(categories)

    influencers = Influencer.query.all()

    for influencer in influencers:
        category = influencer.category
        if category in categories:
            index = categories.index(category)
            counts[index] += 1

    chart_data = {
        "labels": categories,
        "datasets": [{
            "data": counts,
            "label": 'Influencer Distribution by Category',
            "backgroundColor": [
                'rgba(255, 99, 132, 0.5)',  # Red
                'rgba(54, 162, 235, 0.5)',  # Blue
                'rgba(255, 206, 86, 0.5)',  # Yellow
                'rgba(75, 192, 192, 0.5)',  # Green
                'rgba(153, 102, 255, 0.5)', # Purple
                'rgba(255, 159, 64, 0.5)',  # Orange
                'rgba(0, 255, 0, 0.5)',     # Lime
                'rgba(255, 215, 0, 0.5)',   # Gold
                'rgba(186, 85, 211, 0.5)',  # MediumOrchid
                'rgba(255, 69, 0, 0.5)'     # Red-Orange
            ]
        }]
    }

    return chart_data


def flagged_influencer_chart():
    flagged = Influencer.query.filter_by(flagged="True").all()
    non_flagged = Influencer.query.filter_by(flagged="False").all()
    influencer_type = ["Flagged", "Non-Flagged"]
    counts = [len(flagged), len(non_flagged)]
     
    chart_data = {
        "labels": influencer_type,
        "datasets": [{
            "data": counts,
            "label": 'Flagged and Non-Flagged Influencer Ratio',
            "backgroundColor": [
                'rgba(255, 99, 132, 0.5)',
                'rgba(54, 162, 235, 0.5)'
            ],
            "borderColor": [
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
            ],
            "borderWidth": 1
        }]
    }

    return chart_data


def influencer_platform_chart():
    influences = Influence.query.all()
    platform_data = dict()
    for influence in influences:
        if influence.platform in platform_data:
            platform_data[influence.platform] += 1
        else:
            platform_data[influence.platform] = 0
    influence_type = list(platform_data.keys())
    counts = list(platform_data.values())

    chart_data = {
        "labels": influence_type,
        "datasets": [{
            "data": counts,
            "label": 'Influencer by Platform',
            "backgroundColor": [
                'rgba(255, 99, 132, 0.5)',  # Red
                'rgba(54, 162, 235, 0.5)',  # Blue
                'rgba(255, 206, 86, 0.5)',  # Yellow
                'rgba(75, 192, 192, 0.5)',  # Green
                'rgba(153, 102, 255, 0.5)', # Purple
                'rgba(255, 159, 64, 0.5)',  # Orange
            ],
            "borderColor": [
                'rgba(255, 99, 132, 1)',  # Red
                'rgba(54, 162, 235, 1)',  # Blue
                'rgba(255, 206, 86, 1)',  # Yellow
                'rgba(75, 192, 192, 1)',  # Green
                'rgba(153, 102, 255, 1)', # Purple
                'rgba(255, 159, 64, 1)',  # Orange
            ],
            "borderWidth": 1
        }]
    }

    return chart_data

def sponsor_distribution_chart():
    categories = ["Fashion", "Beauty", "Technology", "Health & Fitness", "Travel", 
                  "Food & Beverage", "Gaming", "Sports", "Entertainment", "Home & Lifestyle"]
    counts = [0] * len(categories)

    sponsors = Sponsor.query.all()

    for sponsor in sponsors:
        category = sponsor.industry
        if category in categories:
            index = categories.index(category)
            counts[index] += 1

    chart_data = {
        "labels": categories,
        "datasets": [{
            "data": counts,
            "label": 'Sponsor Distribution by Category',
            "backgroundColor": [
                'rgba(255, 99, 132, 0.5)',  # Red
                'rgba(54, 162, 235, 0.5)',  # Blue
                'rgba(255, 206, 86, 0.5)',  # Yellow
                'rgba(75, 192, 192, 0.5)',  # Green
                'rgba(153, 102, 255, 0.5)', # Purple
                'rgba(255, 159, 64, 0.5)',  # Orange
                'rgba(0, 255, 0, 0.5)',     # Lime
                'rgba(255, 215, 0, 0.5)',   # Gold
                'rgba(186, 85, 211, 0.5)',  # MediumOrchid
                'rgba(255, 69, 0, 0.5)'     # Red-Orange
            ]
        }]
    }

    return chart_data


def flagged_sponsor_chart():
    flagged = Sponsor.query.filter_by(flagged="True").all()
    non_flagged = Sponsor.query.filter_by(flagged="False").all()
    influencer_type = ["Flagged", "Non-Flagged"]
    counts = [len(flagged), len(non_flagged)]
     
    chart_data = {
        "labels": influencer_type,
        "datasets": [{
            "data": counts,
            "label": 'Flagged and Non-Flagged Sponsor Ratio',
            "backgroundColor": [
                'rgba(255, 99, 132, 0.5)',
                'rgba(54, 162, 235, 0.5)'
            ],
            "borderColor": [
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
            ],
            "borderWidth": 1
        }]
    }

    return chart_data


def sponsor_budget_chart():
    categories = ["₹0-1 Lakh", "₹1-5 Lakh", "₹5-10 Lakh", "₹10 Lakh+"]
    counts = [0] * len(categories)

    sponsors = Sponsor.query.all()

    for sponsor in sponsors:
        budget = sponsor.budget
        if budget >= 0 and budget <= 100000:
            counts[0] += 1
        elif budget <= 500000:
            counts[1] += 1
        elif budget <= 1000000:
            counts[2] += 1
        else:
            counts[3] += 1

    chart_data = {
        "labels": categories,
        "datasets": [{
            "data": counts,
            "label": 'Sponsor Distribution by budget',
            "backgroundColor": [
                'rgba(255, 99, 132, 0.5)',  # Red
                'rgba(54, 162, 235, 0.5)',  # Blue
                'rgba(255, 206, 86, 0.5)',  # Yellow
                'rgba(75, 192, 192, 0.5)',  # Green
            ]
        }]
    }

    return chart_data


def ad_distribution_chart():
    categories = ["Fashion", "Beauty", "Technology", "Health & Fitness", "Travel", 
                  "Food & Beverage", "Gaming", "Sports", "Entertainment", "Home & Lifestyle"]
    counts = [0] * len(categories)

    ad_requests = AdRequest.query.all()

    for ad_request in ad_requests:
        category = ad_request.sponsor.industry
        if category in categories:
            index = categories.index(category)
            counts[index] += 1

    chart_data = {
        "labels": categories,
        "datasets": [{
            "data": counts,
            "label": 'Ad Distribution by Category',
            "backgroundColor": [
                'rgba(255, 99, 132, 0.5)',  # Red
                'rgba(54, 162, 235, 0.5)',  # Blue
                'rgba(255, 206, 86, 0.5)',  # Yellow
                'rgba(75, 192, 192, 0.5)',  # Green
                'rgba(153, 102, 255, 0.5)', # Purple
                'rgba(255, 159, 64, 0.5)',  # Orange
                'rgba(0, 255, 0, 0.5)',     # Lime
                'rgba(255, 215, 0, 0.5)',   # Gold
                'rgba(186, 85, 211, 0.5)',  # MediumOrchid
                'rgba(255, 69, 0, 0.5)'     # Red-Orange
            ]
        }]
    }

    return chart_data


def flagged_ad_chart():
    flagged = AdRequest.query.filter_by(flagged="True").all()
    non_flagged = AdRequest.query.filter_by(flagged="False").all()
    ad_request_type = ["Flagged", "Non-Flagged"]
    counts = [len(flagged), len(non_flagged)]
     
    chart_data = {
        "labels": ad_request_type,
        "datasets": [{
            "data": counts,
            "label": 'Flagged and Non-Flagged Ad Request Ratio',
            "backgroundColor": [
                'rgba(255, 99, 132, 0.5)',
                'rgba(54, 162, 235, 0.5)'
            ],
            "borderColor": [
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
            ],
            "borderWidth": 1
        }]
    }

    return chart_data


def ad_status_chart():
    approved = AdRequest.query.filter_by(status="Approved").all()
    pending = AdRequest.query.filter_by(status="Pending").all()
    rejected = AdRequest.query.filter_by(status="Rejected").all()

    ad_request_type = ["Approved", "Pending", "Rejected"]
    counts = [len(approved), len(pending), len(rejected)]
     
    chart_data = {
        "labels": ad_request_type,
        "datasets": [{
            "data": counts,
            "label": 'Ad Request Distribution by Status',
            "backgroundColor": [
                'rgba(54, 162, 235, 0.5)',
                'rgba(255, 215, 0, 0.5)',
                'rgba(255, 99, 132, 0.5)'
            ],
            "borderColor": [
                'rgba(54, 162, 235, 1)',
                'rgba(255, 215, 0, 1)',
                'rgba(255, 99, 132, 1)'

            ],
            "borderWidth": 1
        }]
    }

    return chart_data


def everything_chart():
    sponsors = len(Sponsor.query.all())
    influencers = len(Influencer.query.all())
    campaigns = len(Campaign.query.all())
    ad_requests = len(AdRequest.query.all())
    negotiations = len(Negotiation.query.all())

    mylist = [influencers+sponsors, influencers, sponsors, campaigns, ad_requests, negotiations]

    return mylist
