from flask import request
from app.services.log_services import create_log
from queue import Queue, Empty
from threading import Thread


_log_queue = Queue()
_worker_started = False


def _log_worker():
    while True:
        try:
            item = _log_queue.get()
            if item is None:
                _log_queue.task_done()
                break
            log_type, ip_address, path, method, status_code = item
            create_log(log_type, ip_address, path, method, status_code)
        finally:
            _log_queue.task_done()


def _ensure_worker():
    global _worker_started
    if not _worker_started:
        Thread(target=_log_worker, daemon=True).start()
        _worker_started = True


def log_request(response):
    if request.path.startswith("/static") or request.path.startswith("/logs"):
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

    _ensure_worker()
    _log_queue.put((log_type, ip_address, path, method, status_code))

    return response
