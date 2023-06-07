from flask import Blueprint

from src.controllers.projectController import create, delete_project_by_id,update_project_by_id,get_one_project,get_all_project, index

# Create a Blueprint for the project routes
project_blueprint = Blueprint('projectBlueprint', __name__)

# Define the routes and associate them with the corresponding controller methods
project_blueprint.route('/index', methods=['GET'])(index)
project_blueprint.route('/create', methods=['POST'])(create)
project_blueprint.route('/<int:project_id>', methods=['GET'])(get_one_project)
project_blueprint.route('/', methods=['GET'])(get_all_project)
project_blueprint.route('/update/<int:project_id>', methods=['PUT'])(update_project_by_id)
project_blueprint.route('/delete/<int:project_id>', methods=['DELETE'])(delete_project_by_id)
