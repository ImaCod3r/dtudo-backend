from flask import Blueprint, jsonify, current_app
import os
from app.models.image import Image
from app.middlewares.auth_middlewares import auth_required, is_admin
from app.utils.file_utils import get_dir_size, format_size

images_bp = Blueprint('images', __name__)

@images_bp.get('/storage-info')
@auth_required
@is_admin
def get_images_info():
    try:
        # Caminho absoluto para a pasta de uploads
        upload_path = os.path.join(current_app.root_path, 'static', 'uploads')
        
        # Calcular tamanho total
        total_bytes = get_dir_size(upload_path)
        formatted_size = format_size(total_bytes)
        
        # Buscar todas as imagens registradas no banco
        images = Image.select().order_by(Image.created_at.desc())
        
        return jsonify({
            'error': False,
            'message': 'Informações de armazenamento recuperadas com sucesso!',
            'data': {
                'total_images_registered': len(images),
                'total_storage_size': formatted_size,
                'total_bytes': total_bytes,
                'images': [
                    {
                        'id': img.id,
                        'url': img.url,
                        'filename': img.filename,
                        'created_at': img.created_at.strftime('%Y-%m-%d %H:%M:%S')
                    } for img in images
                ]
            }
        })
    except Exception as e:
        return jsonify({
            'error': True,
            'message': f'Erro ao recuperar informações de armazenamento: {str(e)}'
        }), 500
