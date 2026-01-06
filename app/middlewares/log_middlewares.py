from flask import request
from app.services.log_services import create_log

def log_request(response):
    # Ignore specific paths if necessary (e.g., /static, /logs)
    if request.path.startswith('/static') or request.path.startswith('/logs'):
        return response

    if 200 <= response.status_code < 400:
        log_type = "Success"
    elif 400 <= response.status_code < 500:
        log_type = "Warning"
    else:
        log_type = "Error"

    ip_address = request.remote_addr
    path = request.path
    method = request.method
    status_code = response.status_code

    create_log(log_type, ip_address, path, method, status_code)

    
    return response
