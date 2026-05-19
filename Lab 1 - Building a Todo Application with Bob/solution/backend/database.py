"""
Database Configuration
Initializes and configures the SQLAlchemy database.
"""

from flask_sqlalchemy import SQLAlchemy

# Create SQLAlchemy instance
db = SQLAlchemy()


def init_db(app):
    """
    Initialize the database with the Flask application
    
    Args:
        app: Flask application instance
    """
    db.init_app(app)
    
    with app.app_context():
        # Import models here to avoid circular imports
        import models
        
        # Create all tables
        db.create_all()
        
        print("Database initialized successfully!")

# Made with Bob
