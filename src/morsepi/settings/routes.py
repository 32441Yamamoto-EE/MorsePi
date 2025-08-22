from flask import Blueprint, request, jsonify
from ..utils import require_api_key, set_var

settings_bp = Blueprint('settings', __name__)

# varChanger
@settings_bp.route('/var_changer', methods=['POST'])
@require_api_key
def var_changer():
    data = request.get_json()
    var_name = data.get('var_name')
    new_value = data.get('new_value')
    
    try:
        old_value = set_var(var_name, new_value)
    except ValueError as e:
        error = {
            'error_type': 'ValueError',
            'error_message': str(e)
        }
        return jsonify(error), 400
    
    response = {
        'status': 'Change Successful',
        'message': f'"{var_name}" has been changed from "{old_value}" to "{new_value}".'
    }
    return jsonify(response)