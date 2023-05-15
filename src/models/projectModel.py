from flask_sqlalchemy import SQLAlchemy 
db = SQLAlchemy()


class Inserttable(db.Model):
    '''Table for project model'''
    __tablename__ = 'project'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100),nullable=False)

