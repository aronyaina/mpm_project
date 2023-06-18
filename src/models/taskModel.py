import json
from datetime import datetime
from database import db

Task_Previous_Task = db.Table('task_previous_task',
                              db.Column('task_id', db.Integer, db.ForeignKey('tasks.id'), primary_key=True),
                              db.Column('previous_task_id', db.Integer, db.ForeignKey('tasks.id'), primary_key=True)
                              )


class Task(db.Model):
    """Table for task model"""
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    duration = db.Column(db.Integer)
    early_date = db.Column(db.Integer, default=0)
    late_date = db.Column(db.Integer, default=0)
    margin_date = db.Column(db.Integer, default=0)
    is_critic = db.Column(db.Boolean, default=False)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'))
    datetime = db.Column(db.DateTime, default=lambda: datetime.now())
    previous_tasks = db.relationship('Task', secondary=lambda: Task_Previous_Task,
                                     primaryjoin=lambda: Task.id == Task_Previous_Task.c.task_id,
                                     secondaryjoin=lambda: Task.id == Task_Previous_Task.c.previous_task_id,
                                     backref=db.backref('next_tasks', lazy='dynamic'))

    def __init__(self, project_id, name, duration):
        self.project_id = project_id
        self.name = name
        self.duration = duration

    def __repr__(self) -> str:
        data = {'task_id': self.id,
                'task_name': self.name,
                'task_duration': self.duration,
                'is_critic': self.is_critic,
                'next_tasks': [task.id for task in self.next_tasks],
                'duration': self.duration,
                'early_date': self.early_date,
                'late_date': self.late_date,
                'created_at': self.datetime.strftime('%Y-%m-%d %H:%M:%S'),
                }

        json_data = json.dumps(data)
        return json_data

    def to_json(self):
        # Convert the task object to a JSON-compatible dictionary
        task_json = {
            'task_id': self.id,
            'task_name': self.name,
            'duration': self.duration,
            'early_date': self.early_date,
            'late_date': self.late_date,
            'margin_date': self.margin_date,
            'is_critic': self.is_critic,
            'next_tasks': [task.id for task in self.next_tasks],
            'previous_tasks': [task.id for task in self.previous_tasks]
        }
        return task_json
