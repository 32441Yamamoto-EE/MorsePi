from flask import request, jsonify
from functools import wraps

API_KEY = 'YOUR_API_KEY_HERE'

# APIキー認証用デコレータ
def require_api_key(func):
    @wraps(func)
    def _wrapper(*args, **kwargs):
        key = request.headers.get('X-API-Key')
        if key == API_KEY:
            return func(*args, **kwargs)
        else:
            error = {
                'error_type': 'UnauthorizedError',
                'error_message': 'APIキーが無効、あるいは設定されていません。'
            }
            return jsonify(error), 401
    return _wrapper