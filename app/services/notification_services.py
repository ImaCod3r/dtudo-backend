from app.models.push_subscription import PushSubscription
from app.models.user import User
from pywebpush import webpush, WebPushException
import os
import json
import logging

def _send_push_to_user(user, payload):
    vapid_private_key = os.getenv("VAPID_PRIVATE_KEY")
    vapid_claim_email = os.getenv("VAPID_CLAIM_EMAIL")

    if not vapid_private_key:
        logging.error("VAPID_PRIVATE_KEY not set")
        return

    subscriptions = PushSubscription.select().where(PushSubscription.user == user)
    for sub in subscriptions:
        try:
            webpush(
                subscription_info={
                    "endpoint": sub.endpoint,
                    "keys": {
                        "p256dh": sub.p256dh,
                        "auth": sub.auth
                    }
                },
                data=json.dumps(payload),
                vapid_private_key=vapid_private_key,
                vapid_claims={"sub": vapid_claim_email}
            )
        except WebPushException as ex:
            if ex.response and ex.response.status_code == 410:
                sub.delete_instance()
            logging.error(f"WebPush Error: {ex}")
        except Exception as e:
            logging.error(f"Error sending push: {e}")

def send_notification_to_admins(payload):
    admins = User.select().where(User.role == 'admin')
    for admin in admins:
        _send_push_to_user(admin, payload)

def send_notification_to_user(user_id, payload):
    user = User.get_or_none(User.id == user_id)
    if user:
        _send_push_to_user(user, payload)
    else:
        logging.error(f"User {user_id} not found for notification")
