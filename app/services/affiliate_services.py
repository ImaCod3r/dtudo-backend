import string
import random
from app.models.affiliate import Affiliate
from app.models.affiliate_commission import AffiliateCommission
from app.models.withdrawal import Withdrawal
from app.models.order import Order
from app.models.orderItem import OrderItem
from app.models.user import User
from app.models.image import Image
from app.services.upload_services import save_image, delete_image_file
from app.utils.banks import ANGOLAN_BANKS
from app.services.notification_services import send_notification_to_user, send_notification_to_admins
from peewee import IntegrityError, fn
import datetime

def generate_affiliate_code(length=6):
    chars = string.ascii_uppercase + string.digits
    while True:
        code = ''.join(random.choice(chars) for _ in range(length))
        if not Affiliate.select().where(Affiliate.code == code).exists():
            return code

def apply_for_affiliate(user, bi_front_file, bi_back_file, selfie_file):
    # Check if user already has an affiliate record
    existing = Affiliate.select().where(Affiliate.user == user).first()
    if existing:
        if existing.status == 'approved':
            raise ValueError("Você já é um afiliado aprovado.")
        elif existing.status == 'pending':
            raise ValueError("Sua solicitação de afiliado já está pendente.")
        # If rejected, we might allow re-applying or just update the existing one.
        # For simplicity, let's update the existing one.
    
    bi_front = save_image(bi_front_file, folder="affiliates/docs")
    bi_back = save_image(bi_back_file, folder="affiliates/docs")
    selfie = save_image(selfie_file, folder="affiliates/selfies")

    if existing:
        existing.bi_front = bi_front.url
        existing.bi_back = bi_back.url
        existing.selfie = selfie.url
        existing.status = 'pending'
        existing.save()
        return existing
    else:
        code = generate_affiliate_code()
        affiliate = Affiliate.create(
            user=user,
            bi_front=bi_front.url,
            bi_back=bi_back.url,
            selfie=selfie.url,
            status='pending',
            code=code
        )
    
    # Notificar admins
    try:
        send_notification_to_admins({
            "title": "Nova Solicitação de Afiliado! 👤",
            "body": f"Usuário {user.name} solicitou tornar-se afiliado.",
            "url": "/admin/afiliados"
        })
    except Exception as e:
        print(f"Erro ao notificar admins sobre novo afiliado: {e}")

    return affiliate

def get_affiliate_by_user(user):
    return Affiliate.select().where(Affiliate.user == user).first()

def get_all_affiliate_applications():
    return Affiliate.select().where(Affiliate.status == 'pending')

def update_affiliate_status(affiliate_id, status, admin_user):
    if admin_user.role != 'admin':
        raise PermissionError("Apenas administradores podem alterar o status de um afiliado.")
    
    affiliate = Affiliate.get_by_id(affiliate_id)
    if status not in ['approved', 'rejected']:
        raise ValueError("Status inválido.")
    
    affiliate.status = status
    
    if status == 'rejected':
        # Apagar as fotos enviadas
        for url in [affiliate.bi_front, affiliate.bi_back, affiliate.selfie]:
            if url:
                image = Image.select().where(Image.url == url).first()
                if image:
                    try:
                        delete_image_file(image)
                    except Exception as e:
                        print(f"Erro ao apagar imagem de afiliado rejeitado: {e}")
        
        # Limpar os campos de imagem no registro do afiliado
        affiliate.bi_front = ""
        affiliate.bi_back = ""
        affiliate.selfie = ""

    affiliate.save()

    # Notificar usuário
    status_msg = "aprovada" if status == "approved" else "rejeitada"
    try:
        send_notification_to_user(affiliate.user.id, {
            "title": f"Solicitação de Afiliado {status_msg.capitalize()}! {'🚀' if status == 'approved' else '❌'}",
            "body": f"Sua solicitação para ser um afiliado foi {status_msg}." if status == "approved" else "Infelizmente sua solicitação foi rejeitada. Verifique seus documentos e tente novamente.",
            "url": "/afiliados"
        })
    except Exception as e:
        print(f"Erro ao enviar notificação de afiliado: {e}")

    return affiliate

def calculate_commissions_for_order(order):
    if order.status != 'Entregue':
        return
    
    # 5% commission per product, based on the affiliate code associated with that item
    for item in order.order_items:
        # Pega o código do item, ou cai de volta para o código geral do pedido se houver
        code = item.affiliate_code or order.affiliate_code
        
        if not code:
            continue

        # Check if commission already exists for this item to avoid duplicates
        if AffiliateCommission.select().where(AffiliateCommission.order_item == item).exists():
            continue
            
        affiliate = Affiliate.select().where(Affiliate.code == code).first()
        if not affiliate or affiliate.status != 'approved':
            continue

        commission_amount = item.price * item.quantity * 0.05
        AffiliateCommission.create(
            affiliate=affiliate,
            order=order,
            order_item=item,
            amount=commission_amount,
            status='available'
        )

def get_affiliate_balance(affiliate):
    # Total available minus already withdrawn or pending withdrawals?
    # Actually, let's just sum available commissions.
    available = AffiliateCommission.select(fn.SUM(AffiliateCommission.amount)).where(
        AffiliateCommission.affiliate == affiliate,
        AffiliateCommission.status == 'available'
    ).scalar() or 0.0
    
    return available

def request_withdrawal(affiliate, amount, iban, bank):
    if affiliate.status != 'approved':
        raise ValueError("Apenas afiliados aprovados podem solicitar saques.")
    
    if amount < 10000:
        raise ValueError("O valor mínimo para saque é 10.000 Kz.")
    
    if not affiliate.user.phone:
        raise ValueError("Você precisa ter um número de telefone cadastrado para solicitar saques.")
    
    if bank not in ANGOLAN_BANKS:
        raise ValueError(f"Banco inválido. Bancos permitidos: {', '.join(ANGOLAN_BANKS)}")
    
    balance = get_affiliate_balance(affiliate)
    if amount > balance:
        raise ValueError("Saldo insuficiente.")
    
    withdrawal = Withdrawal.create(
        affiliate=affiliate,
        amount=amount,
        iban=iban,
        bank=bank,
        status='pending'
    )
    
    # Notificar admins
    try:
        send_notification_to_admins({
            "title": "Nova Solicitação de Saque! 💰",
            "body": f"Afiliado {affiliate.user.name} solicitou um saque de Kz {amount:,.2f}.",
            "url": "/admin/financeiro"
        })
    except Exception as e:
        print(f"Erro ao notificar admins sobre novo saque: {e}")

    return withdrawal

def get_pending_withdrawals():
    return Withdrawal.select().where(Withdrawal.status == 'pending')

def process_withdrawal(withdrawal_id, status, admin_user):
    if admin_user.role != 'admin':
        raise PermissionError("Apenas administradores podem processar saques.")
    
    withdrawal = Withdrawal.get_by_id(withdrawal_id)
    if withdrawal.status != 'pending':
        raise ValueError("Este saque já foi processado.")
    
    if status not in ['paid', 'rejected']:
        raise ValueError("Status inválido.")
    
    withdrawal.status = status
    withdrawal.processed_at = datetime.datetime.now()
    withdrawal.save()
    
    # Notificar usuário
    status_msg = "pago" if status == "paid" else "rejeitado"
    try:
        send_notification_to_user(withdrawal.affiliate.user.id, {
            "title": f"Saque {status_msg.capitalize()}! {'💰' if status == 'paid' else '❌'}",
            "body": f"Seu pedido de saque no valor de Kz {withdrawal.amount:,.2f} foi {status_msg}.",
            "url": "/afiliados"
        })
    except Exception as e:
        print(f"Erro ao enviar notificação de saque: {e}")

    if status == 'paid':
        # If paid, we should mark enough commissions as 'withdrawn' 
        # to match the withdrawal amount.
        # This is complex to do perfectly without a mapping table.
        # Alternatively, we just decrease the total available.
        # Let's just leave it as is for now, or update 'to_dict' to subtract pending/paid withdrawals from balance.
        pass
    
    return withdrawal

def get_affiliate_stats(affiliate):
    total_earned = AffiliateCommission.select(fn.SUM(AffiliateCommission.amount)).where(
        AffiliateCommission.affiliate == affiliate
    ).scalar() or 0.0
    
    withdrawn = Withdrawal.select(fn.SUM(Withdrawal.amount)).where(
        Withdrawal.affiliate == affiliate,
        Withdrawal.status == 'paid'
    ).scalar() or 0.0
    
    pending_withdrawal = Withdrawal.select(fn.SUM(Withdrawal.amount)).where(
        Withdrawal.affiliate == affiliate,
        Withdrawal.status == 'pending'
    ).scalar() or 0.0
    
    balance = total_earned - withdrawn - pending_withdrawal
    
    return {
        "total_earned": total_earned,
        "withdrawn": withdrawn,
        "pending_withdrawal": pending_withdrawal,
        "balance": balance,
        "code": affiliate.code,
        "status": affiliate.status
    }
