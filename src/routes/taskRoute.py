from flask import Blueprint
from src.controllers.taskController import get_one_task,get_all_task, create, delete_task_by_id, update_task_by_id, index

# Create a Blueprint for the task routes
task_blueprint = Blueprint('taskBlueprint', __name__)

# Define the routes and associate them with the corresponding controller methods
task_blueprint.route('/index', methods=['GET'])(index)
task_blueprint.route('/create', methods=['POST'])(create)
task_blueprint.route('/<int:task_id>', methods=['GET'])(get_one_task)
task_blueprint.route('/', methods=['GET'])(get_all_task)
task_blueprint.route('/update/<int:task_id>', methods=['PUT'])(update_task_by_id)
task_blueprint.route('/delete/<int:task_id>', methods=['DELETE'])(delete_task_by_id)
