"""
Database Models
Defines the Todo model for the application.
"""

from database import db
from datetime import datetime


class Todo(db.Model):
    """
    Todo Model
    
    Represents a single todo item with title, description, 
    completion status, and timestamp.
    """
    
    __tablename__ = 'todos'
    
    # Primary key
    id = db.Column(db.Integer, primary_key=True)
    
    # Todo content
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    
    # Status
    completed = db.Column(db.Boolean, default=False, nullable=False)
    
    # Timestamp
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        """String representation of the Todo"""
        return f'<Todo {self.id}: {self.title}>'
    
    def to_dict(self):
        """
        Convert Todo object to dictionary for JSON serialization
        
        Returns:
            dict: Dictionary representation of the todo
        """
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'completed': self.completed,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

# Made with Bob
