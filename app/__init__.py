"""
Flask application factory
Creates and configures the Flask app instance with blueprints and error handlers
"""

from flask import Flask, send_from_directory
from flask_cors import CORS
from models import db
from config import config
import os


def create_app(config_name='development'):
    """
    Application factory function.
    
    Strategy Pattern: Different configurations can be applied based on environment.
    This allows flexibility in deployment without code changes.
    
    Args:
        config_name: Configuration environment ('development', 'production', 'testing')
        
    Returns:
        Configured Flask application instance
    """
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Enable CORS for frontend (localhost:3000, localhost:3001)
    CORS(app, 
         origins=['http://localhost:3000', 'http://localhost:3001'],
         supports_credentials=True,
         allow_headers=['Content-Type', 'Authorization'],
         methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
    
    # Initialize database
    db.init_app(app)
    
    # Create tables with application context
    with app.app_context():
        db.create_all()
    
    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.todo import todo_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(todo_bp, url_prefix='/api')
    
    # Test page route
    @app.route('/')
    def index():
        return send_from_directory('.', 'test_api.html')
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return {'error': 'Resource not found'}, 404
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return {'error': 'Internal server error'}, 500
    
    return app
