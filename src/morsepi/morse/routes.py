from flask import Blueprint, request, jsonify
from ..utils import require_api_key, text_to_morse, morse_output, get_var
import threading

morse_bp = Blueprint('morse', __name__)

@morse_bp.route('/', methods=['POST'])
@require_api_key
def morse():
    # 文字列を受取り変換
    data = request.get_json()
    text = data.get('text', '')
    unit = get_var('unit')
    
    try:
        morse_list, morse_str = text_to_morse(text)
    except ValueError as e:
        error = {
            'error_type': 'ValueError',
            'error_message': str(e)
        }
        return jsonify(error), 400
    
    # 非同期処理で出力
    thread = threading.Thread(target=morse_output, args=(morse_list, text, unit))
    thread.start()
    
    response = {
        'input_text': text,
        'morse_str': morse_str
    }
    return jsonify(response)