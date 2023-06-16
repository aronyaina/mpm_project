from datetime import datetime
from database import db


class Project(db.Model):
    """Table for project model"""
    __tablename__ = 'projects'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    datetime = db.Column(db.DateTime, default=lambda: datetime.now())
    tasks = db.relationship('Task', backref='projects', lazy=True)

    def __init__(self, name):
        # Initialize the Project object with a name
        self.name = name

    def to_json(self):
        # Convert the Project object to a JSON format
        return {
            'id': self.id,
            'name': self.name,
            'created_at': self.datetime.strftime('%Y-%m-%d %H:%M:%S'),
            'tasks': [task.to_json() for task in self.tasks if task],
        }

    def __repr__(self):
        # Return a string representation of the Project object
        return f"({self.id} : {self.name})"
