from flask import Blueprint, request, jsonify
from app.middlewares.auth_middlewares import auth_required, is_admin
from app.services.affiliate_services import (
    apply_for_affiliate, get_affiliate_by_user, get_affiliate_stats,
    request_withdrawal, get_all_affiliate_applications, update_affiliate_status,
    get_pending_withdrawals, process_withdrawal
)
from app.models.user import User

affiliates_bp = Blueprint('affiliates', __name__)

@affiliates_bp.post('/apply')
@auth_required
def apply():
    user_id = request.user["sub"]
    user = User.get_or_none(User.id == user_id)
    if not user:
        return jsonify({"error": "Usuário não encontrado."}), 404
    
    bi_front = request.files.get('bi_front')
    bi_back = request.files.get('bi_back')
    selfie = request.files.get('selfie')
    
    if not all([bi_front, bi_back, selfie]):
        return jsonify({"error": "Todos os documentos são obrigatórios (BI frente, verso e selfie)."}), 400
    
    try:
        affiliate = apply_for_affiliate(user, bi_front, bi_back, selfie)
        return jsonify({
            "message": "Solicitação de afiliado enviada com sucesso!",
            "affiliate": affiliate.to_dict()
        }), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Erro ao processar solicitação: {str(e)}"}), 500

@affiliates_bp.get('/me')
@auth_required
def get_my_affiliate_info():
    user_id = request.user["sub"]
    user = User.get_or_none(User.id == user_id)
    if not user:
        return jsonify({"is_affiliate": False, "error": "Usuário não encontrado."}), 404
    
    affiliate = get_affiliate_by_user(user)
    if not affiliate:
        return jsonify({"is_affiliate": False}), 200
    
    stats = get_affiliate_stats(affiliate)
    return jsonify({
        "is_affiliate": True,
        "affiliate": affiliate.to_dict(),
        "stats": stats
    }), 200

@affiliates_bp.post('/withdraw')
@auth_required
def withdraw():
    user_id = request.user["sub"]
    user = User.get_or_none(User.id == user_id)
    if not user:
        return jsonify({"error": "Usuário não encontrado."}), 404
    
    affiliate = get_affiliate_by_user(user)
    if not affiliate or affiliate.status != 'approved':
        return jsonify({"error": "Apenas afiliados aprovados podem solicitar saques."}), 403
    
    data = request.get_json()
    amount = data.get('amount')
    iban = data.get('iban')
    bank = data.get('bank')
    
    if not all([amount, iban, bank]):
        return jsonify({"error": "Valor, IBAN e Banco são obrigatórios."}), 400
    
    try:
        withdrawal = request_withdrawal(affiliate, float(amount), iban, bank)
        return jsonify({
            "message": "Solicitação de saque enviada com sucesso!",
            "withdrawal": withdrawal.to_dict()
        }), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Erro ao processar saque: {str(e)}"}), 500

# Admin Routes
@affiliates_bp.get('/admin/applications')
@auth_required
@is_admin
def list_applications():
    apps = get_all_affiliate_applications()
    return jsonify({
        "applications": [a.to_dict() for a in apps]
    }), 200

@affiliates_bp.post('/admin/approve/<int:id>')
@auth_required
@is_admin
def approve_app(id):
    user_id = request.user["sub"]
    admin = User.get_by_id(user_id)
    
    try:
        affiliate = update_affiliate_status(id, 'approved', admin)
        return jsonify({
            "message": "Afiliado aprovado com sucesso!",
            "affiliate": affiliate.to_dict()
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@affiliates_bp.post('/admin/reject/<int:id>')
@auth_required
@is_admin
def reject_app(id):
    user_id = request.user["sub"]
    admin = User.get_by_id(user_id)
    
    try:
        affiliate = update_affiliate_status(id, 'rejected', admin)
        return jsonify({
            "message": "Afiliado rejeitado.",
            "affiliate": affiliate.to_dict()
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@affiliates_bp.get('/admin/withdrawals')
@auth_required
@is_admin
def list_withdrawals():
    withdrawals = get_pending_withdrawals()
    return jsonify({
        "withdrawals": [w.to_dict() for w in withdrawals]
    }), 200

@affiliates_bp.post('/admin/withdrawals/<int:id>/paid')
@auth_required
@is_admin
def mark_paid(id):
    user_id = request.user["sub"]
    admin = User.get_by_id(user_id)
    
    try:
        withdrawal = process_withdrawal(id, 'paid', admin)
        return jsonify({
            "message": "Saque marcado como pago.",
            "withdrawal": withdrawal.to_dict()
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@affiliates_bp.post('/admin/withdrawals/<int:id>/reject')
@auth_required
@is_admin
def reject_withdrawal_route(id):
    user_id = request.user["sub"]
    admin = User.get_by_id(user_id)
    
    try:
        withdrawal = process_withdrawal(id, 'rejected', admin)
        return jsonify({
            "message": "Saque rejeitado.",
            "withdrawal": withdrawal.to_dict()
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400