# /NoctiWave/app/user/management.py

from datetime import datetime, timedelta, timezone
from .models import Notification
from .. import db

def my_converter(num):
    suffixes = ['', 'K', 'M', 'B', 'T']
    index = 0
    while num >= 1000 and index < len(suffixes) - 1:
        num /= 1000.0
        index += 1
    formatted_num = f'{num:.1f}'.rstrip('0').rstrip('.')
    return f'{formatted_num}{suffixes[index]}'


def time_converter(created_at):
    now = datetime.utcnow()
    delta = now - created_at

    if delta < timedelta(seconds=60):
        return 'Just Now'
    elif delta < timedelta(minutes=60):
        minutes = delta.seconds // 60
        return f'{minutes} minute{"s" if minutes > 1 else ""} ago'
    elif delta < timedelta(hours=24):
        hours = delta.seconds // 3600
        return f'{hours} hour{"s" if hours > 1 else ""} ago'
    elif delta <timedelta(days=30) :
        days = delta.days
        return f'{days} day{"s" if days > 1 else ""} ago'
    else:
        return created_at.strftime('%Y-%m-%d')


def campaign_flagged(campaign):
    title = "<strong>Campaign Flagged</strong>"
    description = f'Dear {campaign.sponsor.user.username.capitalize()}, Your campaign <strong>{campaign.name}</strong> has been flagged for violating our terms and conditions. It is currently hidden for all users, including yourself. If you believe this action is incorrect, please contact us for further review.'
    notification = Notification(user_id=campaign.sponsor.user_id, title=title, description=description)
    db.session.add(notification)
    db.session.commit()

def campaign_unflagged(campaign):
    title = "<strong>Campaign Unflagged</strong>"
    description = f'Good news, {campaign.sponsor.user.username.capitalize()}! Your campaign <strong>{campaign.name}</strong> has been successfully reviewed and is now available to all users, including yourself. Carry on with your campaign!'
    notification = Notification(user_id=campaign.sponsor.user_id, title=title, description=description)
    db.session.add(notification)
    db.session.commit()

def campaign_deleted(campaign):
    title = "<strong>Campaign Deleted</strong>"
    description = f'Dear {campaign.sponsor.user.username.capitalize()}, Your campaign <strong>{campaign.name}</strong> has been deleted for violating our terms and conditions multiple times. If you believe this action is incorrect, please contact us for further review.'
    notification = Notification(user_id=campaign.sponsor.user_id, title=title, description=description)
    db.session.add(notification)
    db.session.commit()

def sponsor_ad_request_flagged(ad_request):
    title = "<strong>AdRequest Flagged</strong>"
    description = f'Dear {ad_request.sponsor.user.username.capitalize()}, Your AdRequest <strong>ID-{ad_request.ad_request_id}</strong> to <strong>{ad_request.influencer.user.username.capitalize()}</strong> has been flagged for violating our terms and conditions. It is currently inaccessible to both of you. If you believe this action is incorrect, please contact us for further review.'
    notification = Notification(user_id=ad_request.sponsor.user.user_id, title=title, description=description)
    db.session.add(notification)
    db.session.commit()

def influencer_ad_request_flagged(ad_request):
    title = "<strong>AdRequest Flagged</strong>"
    description = f'Dear {ad_request.influencer.user.username.capitalize()}, Your AdRequest <strong>ID-{ad_request.ad_request_id}</strong> to <strong>{ad_request.sponsor.user.username.capitalize()}</strong> has been flagged for violating our terms and conditions. It is currently inaccessible to both of you. If you believe this action is incorrect, please contact us for further review.'
    notification = Notification(user_id=ad_request.influencer.user.user_id, title=title, description=description)
    db.session.add(notification)
    db.session.commit()

def sponsor_ad_request_unflagged(ad_request):
    title = "<strong>AdRequest Unflagged</strong>"
    description = f'Good news, {ad_request.sponsor.user.username.capitalize()}! Your AdRequest <strong>ID-{ad_request.ad_request_id}</strong> to <strong>{ad_request.influencer.user.username.capitalize()}</strong> has been successfully reviewed and is now accessible to both of you. Continue collaborating smoothly!'
    notification = Notification(user_id=ad_request.sponsor.user.user_id, title=title, description=description)
    db.session.add(notification)
    db.session.commit()

def influencer_ad_request_unflagged(ad_request):
    title = "<strong>AdRequest Unflagged</strong>"
    description = f'Good news, {ad_request.influencer.user.username.capitalize()}! Your AdRequest <strong>ID-{ad_request.ad_request_id}</strong> to <strong>{ad_request.sponsor.user.username.capitalize()}</strong> has been successfully reviewed and is now accessible to both of you. Continue collaborating smoothly!'
    notification = Notification(user_id=ad_request.influencer.user.user_id, title=title, description=description)
    db.session.add(notification)
    db.session.commit()

def sponsor_ad_request_deleted(ad_request):
    title = "<strong>AdRequest Deleted</strong>"
    description = f'Dear {ad_request.sponsor.user.username.capitalize()}, Your AdRequest <strong>ID-{ad_request.ad_request_id}</strong> to <strong>{ad_request.influencer.user.username.capitalize()}</strong> has been deleted for violating our terms and conditions. If you believe this action is incorrect, please contact us for further review.'
    notification = Notification(user_id=ad_request.sponsor.user.user_id, title=title, description=description)
    db.session.add(notification)
    db.session.commit()

def influencer_ad_request_deleted(ad_request):
    title = "<strong>AdRequest Deleted</strong>"
    description = f'Dear {ad_request.influencer.user.username.capitalize()}, Your AdRequest <strong>ID-{ad_request.ad_request_id}</strong> to <strong>{ad_request.sponsor.user.username.capitalize()}</strong> has been deleted for violating our terms and conditions. If you believe this action is incorrect, please contact us for further review.'
    notification = Notification(user_id=ad_request.influencer.user.user_id, title=title, description=description)
    db.session.add(notification)
    db.session.commit()

def user_flagged(user):
    title = "<strong>Account Flagged</strong>"
    description = f'Dear {user.user.username.capitalize()}, Your account <strong>@{user.user.username}</strong> has been flagged for violating our terms and conditions. It is currently hidden from all users. If you continue this behavior, your account could be subject to deletion.'
    notification = Notification(user_id=user.user.user_id, title=title, description=description)
    db.session.add(notification)
    db.session.commit()

def user_unflagged(user):
    title = "<strong>Account Unflagged</strong>"
    description = f'Good news, {user.user.username.capitalize()}! Your account <strong>@{user.user.username}</strong> has been successfully unflagged and is now visible to all users again.'
    notification = Notification(user_id=user.user.user_id, title=title, description=description)
    db.session.add(notification)
    db.session.commit()