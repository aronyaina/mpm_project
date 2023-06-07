from src.services.projectService import create_project, delete_project, update_project, get_all_project , get_one_project


def index():
    # Return a dictionary with API endpoints and their descriptions
    return {
        'status': 'OK',
        'localhost:5000/project/': 'Read all projects',
        'localhost:5000/project/<int:project_id>': 'Read one project',
        'localhost:5000/project/create': 'Create project',
        'localhost:5000/project/update': 'Update project',
        'localhost:5000/project/delete': 'Delete project',
    }


def create():
    # Call the create_project function to create a new project
    return create_project()


def delete_project_by_id():
    # Call the delete_project function to delete a project by its ID
    return delete_project()


def update_project_by_id():
    # Call the update_table function to update a project by its ID
    return update_project()


def get_project_by_id(project_id):
    # Call the get_one_project function to retrieve a project by its ID
    return get_one_project(project_id)


def get_projects():
    return get_all_project()

