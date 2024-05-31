from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
ma = Marshmallow()

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')
    
    db.init_app(app)
    ma.init_app(app)
    
    from .routes import bp as routes_bp
    app.register_blueprint(routes_bp)
    
    with app.app_context():
        from . import routes
        db.create_all()
    
    return app