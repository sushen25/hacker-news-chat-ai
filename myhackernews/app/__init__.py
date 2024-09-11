from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    db_uri = "postgresql://admin:admin@localhost:5432/mydb"
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri 
    
    # Initialize extensions with the app
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Register blueprints (routes)
    from app.routes import main
    app.register_blueprint(main)
    
    return app