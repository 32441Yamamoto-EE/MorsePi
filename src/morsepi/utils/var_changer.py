import os, json

config_file = os.path.join(os.path.dirname(__file__), 'var_config.json')

def load_config():
    try:
        with open(config_file, 'r') as f:
            global config
            config = json.load(f)
    except:
        # 読み込み失敗時に初期値を設定
        config = {
            'unit': 0.1
        }
    
    return config

def save_config():
    with open(config_file, 'w') as f:
        json.dump(config, f)

def set_var(var_name, new_value):
    load_config()
    old_value = config.get(var_name, None)
    if var_name == 'unit':
        try:
            new_value = float(new_value)
            
            if new_value < 0: #負の数値を判定
                raise ValueError()
        except ValueError: #floatの失敗か負の数値時のエラーをキャッチ
            raise ValueError(f'無効な値です（正の数値を入力してください）。\n入力された値: {new_value}')

    config[var_name] = new_value
    save_config()
    
    return old_value

def get_var(var_name):
    config = load_config()
    return config.get(var_name, None)