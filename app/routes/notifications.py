from flask import Blueprint, request, jsonify
from app.middlewares.auth_middlewares import auth_required
from app.models.push_subscription import PushSubscription
from app.services.user_services import get_user_by_id
import os
import logging

notifications_bp = Blueprint('notifications', __name__)

@notifications_bp.post("/subscribe")
@auth_required
def subscribe():
    try:
        data = request.json
        user_id = request.user["sub"]
        user = get_user_by_id(user_id)
        
        if not user:
             return jsonify({'error': True, 'message': 'User not found'}), 404

        subscription_info = data
        
        endpoint = subscription_info.get('endpoint')
        keys = subscription_info.get('keys', {})
        p256dh = keys.get('p256dh')
        auth = keys.get('auth')

        if not endpoint or not p256dh or not auth:
            return jsonify({'error': True, 'message': 'Invalid subscription object'}), 400

        existing = PushSubscription.select().where(PushSubscription.endpoint == endpoint).first()
        if existing:
            existing.user = user
            existing.p256dh = p256dh
            existing.auth = auth
            existing.save()
        else:
            PushSubscription.create(
                user=user,
                endpoint=endpoint,
                p256dh=p256dh,
                auth=auth
            )

        return jsonify({'error': False, 'message': 'Subscribed successfully'}), 201
    except Exception as e:
        logging.error(f"Error subscribing: {e}")
        return jsonify({'error': True, 'message': 'Internal Server Error'}), 500

@notifications_bp.get("/vapid-public-key")
def get_vapid_key():
    key = os.getenv("VAPID_PUBLIC_KEY")
    if not key:
        return jsonify({'error': True, 'message': 'VAPID key not configured'}), 500
    return jsonify({'publicKey': key})
