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
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'))
    datetime = db.Column(db.DateTime, default=lambda: datetime.now())
    previous_task_ids = db.Column(db.String(200), default=[])
    previous_tasks = db.relationship('Task', secondary=lambda: Task_Previous_Task,
                                     primaryjoin=lambda: Task.id == Task_Previous_Task.c.task_id,
                                     secondaryjoin=lambda: Task.id == Task_Previous_Task.c.previous_task_id,
                                     backref=db.backref('next_tasks', lazy='dynamic'))

    def __init__(self, project_id, task_name, task_duration, previous_task_ids):
        self.project_id = project_id
        self.name = task_name
        self.duration = task_duration
        self.previous_task_ids = previous_task_ids

    def to_json(self):
        # Convert the task object to a JSON-compatible dictionary
        task_json = {'task_id': self.id, 'task_name': self.name, 'task_duration': self.duration,
                     'early_date': self.early_date, 'late_date': self.late_date, 'project_id': self.project_id,
                     'previous_tasks_id': json.loads(self.previous_task_ids)
                     }

        return task_json

    def __repr__(self) -> str:
        data = {
            'name': self.name,
            'id': self.id,
            'date_operation': [self.duration, self.early_date, self.late_date],
            'previous_tasks_ids': json.loads(self.previous_task_ids),
        }

        # Convert the data structure to a JSON string
        json_data = json.dumps(data)
        return json_data
