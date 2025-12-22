import os
import uuid
from werkzeug.utils import secure_filename
from peewee import IntegrityError
from app.models.image import Image

UPLOAD_FOLDER = "app/static/uploads/products"
ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "webp"}
MAX_IMAGE_SIZE = 5 * 1024 * 1024  # 5 MB

def allowed_file(filename):
    """Pega o nome do arquivo divide pelo ponto (se houver) 
        retornando um array e verfica se o ultimo (a extensão)
        está no set de extensões permitidas"""
    return "." in filename and get_file_extension(filename) in ALLOWED_EXTENSIONS

def save_image(file):
    # Pega o nome original do arquivo
    original_filename = secure_filename(file.filename)

    # Verifica se o nome do arquivo é válido
    if not original_filename:
        raise ValueError("Nome de arquivo inválido!")

    # Verifca o formato da imagem
    if not allowed_file(file.filename):
        raise ValueError("Formato de imagem inválido!")
    
    # Verificar o tamanho real da imagem
    file.stream.seek(0, os.SEEK_END)
    size = file.stream.tell()
    file.stream.seek(0)

    if size > MAX_IMAGE_SIZE:
        raise ValueError("O tamanho da imagem é maior do que o permitido (5MB)!")
    
    ext = get_file_extension(original_filename)
    filename = f"{uuid.uuid4()}.{ext}" # Gera filename seguro

    os.makedirs(UPLOAD_FOLDER, exist_ok=True) # Cria a pasta se ela não existir
    file_path = os.path.join(UPLOAD_FOLDER, filename)

    file.save(file_path)

    url = f"/static/uploads/products/{filename}"

    # Salva a imagem banco
    try:
        image = Image.create(
            url = url,
            filename = filename
        )
    except IntegrityError:
        # Apaga o arquivo no diretório se ele não for salvo no banco
        if os.path.exists(file_path):
            os.remove(file_path)
        raise

    return image

def get_file_extension(filename):
    return filename.rsplit(".", 1)[1].lower()

def delete_image_file(image):
    file_path = image.url.replace("/static/", "app/static/")
    if os.path.exists(file_path):
        os.remove(file_path)
    image.delete_instance()