from flask import Flask
from flask_migrate import Migrate
from src.routes.projectRoute import project_blueprint
from src.routes.taskRoute import task_blueprint
from database import db


def create_app():
    """
    Create and configure the Flask application.

    Returns:
        Flask: The configured Flask application instance.
    """
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/mpm'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    return app


application = create_app()

# Registering blueprints
application.register_blueprint(project_blueprint, url_prefix='/project')
application.register_blueprint(task_blueprint, url_prefix='/project/<int:project_id>/task')

migrate = Migrate(application, db)

if __name__ == '__main__':
    # Run the application when executed directly
    application.run(debug=True, port=5000, host='0.0.0.0')
