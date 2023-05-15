from flask_sqlalchemy import SQLAlchemy 
db=SQLAlchemy()


class inserttable(db.model):
    __tablename__='task'

    id=db.Column(db.Integer, primary_key=True, auto_increment=True)
    taskName=db.Column(db.String(200), nullable=False)
    taskDuration=db.Column(db.Integer)
    prevTask=db.Column(db.String(50))
    earlyDate=db.Column(db.Integer)
    lateDate=db.Column(db.Integer)


