from flask import Flask

def create_app():
    app = Flask(__name__)
    
    # Blueprint
    from .morse.routes import morse_bp
    from .settings.routes import settings_bp
    
    app.register_blueprint(morse_bp, url_prefix='/morse')
    app.register_blueprint(settings_bp, url_prefix='/settings')
    
    return app