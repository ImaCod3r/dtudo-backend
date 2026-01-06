from flask import Blueprint, jsonify, request
from app.services.log_services import get_all_logs, delete_all_logs
from app.middlewares.auth_middlewares import auth_required, is_admin

logs_bp = Blueprint('logs', __name__)

@logs_bp.get('/')
@auth_required
@is_admin
def get_logs():
    try:
        logs = get_all_logs()
        return jsonify({
            'error': False,
            'message': 'Logs recuperados com sucesso!',
            'logs': [log.to_dict() for log in logs]
        })
    except Exception as e:
        return jsonify({
            'error': True,
            'message': f'Erro ao recuperar logs: {str(e)}'
        }), 500

@logs_bp.delete('/clear')
@auth_required
@is_admin
def clear_logs():
    success, error = delete_all_logs()
    if not success:
        return jsonify({
            'error': True,
            'message': error
        }), 400
    
    return jsonify({
        'error': False,
        'message': 'Logs limpos com sucesso!'
    }), 200
