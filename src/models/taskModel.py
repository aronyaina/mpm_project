from datetime import datetime
from database import db

task_dependencies = db.Table(
    'task_dependencies',
    db.Column('parent_task_id', db.Integer, db.ForeignKey('tasks.id')),
    db.Column('child_task_id', db.Integer, db.ForeignKey('tasks.id'))
)


class Task(db.Model):
    """Table for task model"""
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    duration = db.Column(db.Integer)
    earlyDate = db.Column(db.Integer, default=0)
    lateDate = db.Column(db.Integer, default=0)
    projectId = db.Column(db.Integer, db.ForeignKey('projects.id'))
    datetime = db.Column(db.DateTime, default=lambda:datetime.now())
    prevTasks = db.relationship(
        'Task',
        secondary=task_dependencies,
        primaryjoin=(task_dependencies.c.child_task_id == id),
        secondaryjoin=(task_dependencies.c.parent_task_id == id),
        backref=db.backref('nextTasks', lazy='dynamic'),
        lazy='dynamic'
    )

    def __init__(self, project_id , task_name, task_duration):
        self.projectId = project_id
        self.name = task_name
        self.duration = task_duration

    def to_json(self):
        # Convert the task object to a JSON-compatible dictionary
        task_json = {'task_id': self.id, 'task_name': self.name, 'task_duration': self.duration,
                     'early_date': self.earlyDate, 'late_date': self.lateDate, 'project_id': self.projectId}

        return task_json
    def __repr__(self) -> str:
        # String representation of the task object
        return f"({self.id} : {self.taskName})"



