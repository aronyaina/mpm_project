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
    name = db.Column(db.String(200), nullable=False, unique=True)
    duration = db.Column(db.Integer)
    early_date = db.Column(db.Integer, default=0)
    late_date = db.Column(db.Integer, default=0)
    margin_date = db.Column(db.Integer, default=0)
    is_critic = db.Column(db.Boolean, default=False)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'))
    datetime = db.Column(db.DateTime, default=lambda: datetime.now())
    previous_tasks_names = db.Column(db.String(200), default=[])
    previous_tasks = db.relationship('Task', secondary=lambda: Task_Previous_Task,
                                     primaryjoin=lambda: Task.id == Task_Previous_Task.c.task_id,
                                     secondaryjoin=lambda: Task.id == Task_Previous_Task.c.previous_task_id,
                                     backref=db.backref('next_tasks', lazy='dynamic'))

    def __init__(self, project_id, name, duration, previous_tasks_names):
        self.project_id = project_id
        self.name = name
        self.duration = duration
        self.previous_tasks_names = previous_tasks_names

    def __repr__(self) -> str:
        data = {'task_id': self.id, 'task_name': self.name, 'task_duration': self.duration,
                'is_critic': self.is_critic,
                'previous_tasks_names': json.loads(self.previous_tasks_names),
                'next_tasks': [task.id for task in self.next_tasks],
                'duration': self.duration,
                'early_date': self.get_early_date(),
                'late_date': self.get_late_date(),
                'created_at': self.datetime.strftime('%Y-%m-%d %H:%M:%S'),
                }

        json_data = json.dumps(data)
        return json_data

    def to_json(self):
        # Convert the task object to a JSON-compatible dictionary
        task_json = {'task_id': self.id, 'task_name': self.name, 'task_duration': self.duration,
                     'date_operation': [self.duration, self.get_early_date(), self.get_late_date(), self.margin_date],
                     'is_critic': self.is_critic,
                     'previous_tasks_names': json.loads(self.previous_tasks_names),
                     'next_tasks': [task.id for task in self.next_tasks]
                     }

        return task_json

    def get_early_date(self) -> int:
        if not self.previous_tasks:
            self.early_date = self.duration
            return self.early_date
        else:
            for previous_task in self.previous_tasks:
                prev_task_early_date = previous_task.early_date
                if prev_task_early_date >= self.early_date:
                    self.early_date = prev_task_early_date + self.duration
            return self.early_date

    def get_late_date(self) -> int:
        if not self.next_tasks:
            self.late_date = self.early_date
            return self.late_date
        else:
            for next_task in self.next_tasks:
                next_task_late_date = next_task.late_date
                if next_task_late_date <= self.late_date:
                    self.late_date = next_task_late_date - self.duration
            if self.late_date < 0:
                return 0
            else:
                return self.late_date

    def get_margin(self):
        return self.get_early_date() - self.get_late_date()

    def get_critic_path(self) -> bool:
        if self.get_margin() == 0:
            return True
        else:
            return False
