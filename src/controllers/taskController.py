from src.services.taskService import create_task, delete_task, update_task, get_tasks, get_task_by_id


def index():
    # Return a dictionary with API endpoints and their descriptions
    return {
        'status': 'OK',
        'localhost:5000/project/task/create': 'Create task',
        'localhost:5000/project/task/<int:task_id>': 'Read one task',
        'localhost:5000/project/task/': 'Read all tasks',
        'localhost:5000/project/update/task/': 'Update task',
        'localhost:5000/project/delete/task/': 'Delete task',
    }


def get_one_task(project_id, task_id):
    return get_task_by_id(project_id, task_id)


def get_all_task(project_id):
    return get_tasks(project_id)


def create(project_id):
    # Call the create_task function to create a new task within a specific project
    return create_task(project_id)


def delete_task_by_id(project_id, task_id):
    # Call the delete_task function to delete a task by its ID within a specific project
    return delete_task(project_id, task_id)


def update_task_by_id(project_id, task_id):
    # Call the update_task function to update a task by its ID within a specific project
    return update_task(project_id, task_id)
