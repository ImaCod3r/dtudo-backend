from app.models.log import Log

def create_log(log_type, ip_address, path, method, status_code):
    try:
        log = Log.create(
            log_type=log_type,
            ip_address=ip_address,
            path=path,
            method=method,
            status_code=status_code
        )

        return log, None
    except Exception as e:
        return None, str(e)

def get_all_logs():
    return Log.select().order_by(Log.timestamp.desc())

def delete_all_logs():
    try:
        Log.delete().execute()
        return True, None
    except Exception as e:
        return False, str(e)
