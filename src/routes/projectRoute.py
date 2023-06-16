from flask import Blueprint

from src.controllers.projectController import create_project, delete_project_by_id, update_project_by_id, \
    get_project_by_id, \
    get_all_project

# Create a Blueprint for the project routes
project_blueprint = Blueprint('projectBlueprint', __name__)

# Define the routes and associate them with the corresponding controller methods
project_blueprint.route('/create', methods=['POST'])(create_project)
project_blueprint.route('/<int:project_id>', methods=['GET'])(get_project_by_id)
project_blueprint.route('/', methods=['GET'])(get_all_project)
project_blueprint.route('/update/<int:project_id>', methods=['PUT'])(update_project_by_id)
project_blueprint.route('/delete/<int:project_id>', methods=['DELETE'])(delete_project_by_id)
