from datetime import datetime, timezone

def error_response(code: str, message: str, details: list = None):
    return {
        "error": {
            "code": code,
            "message": message,
            "details": details or [],
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    }