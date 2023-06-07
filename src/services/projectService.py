from datetime import datetime
from flask import jsonify, request
from src.models.projectModel import Project, db


def create_project():
    try:
        db.create_all()
        project_data = request.get_json()
        project_name = project_data.get('name')
        new_project = Project(name=project_name)
        db.session.add(new_project)
        db.session.commit()
        return jsonify(new_project.to_json())
    except Exception as e:
        return f'An error has occurred: {e}'


def update_project(project_id):
    try:
        new_project_name = request.json.get('name')
        project = Project.query.get(project_id)
        if project:
            project.name = new_project_name
            project.datetime = datetime.now()
        db.session.commit()
        return jsonify(project.to_json())

    except Exception as e:
        return jsonify({"error": f"An error has occurred: {e}"}), 500


def delete_project(project_id):
    try:
        project = Project.query.get(project_id)
        if project:
            db.session.delete(project)
            db.session.commit()
            return jsonify(project.to_json())
        else:
            return jsonify({"error": "Project not found"}), 500
    except Exception as e:
        return jsonify({"error": f"An error has occurred: {e}"}), 500


def get_all_project():
    try:
        # Logic to retrieve all projects
        projects = Project.query.all()
        if projects:
            return jsonify([project.to_json() for project in projects])
        else:
            return jsonify({"error": "Project not found"}), 500
    except Exception as e:
        return jsonify({"error": f"An error has occurred: {e}"}), 500


def get_one_project(project_id):
    try:
        # Logic to retrieve a specific project with project_id
        project = Project.query.get(project_id)
        if project:
            return jsonify(project.to_json())
        else:
            return jsonify({"error": "Project not found"}), 404
    except Exception as e:
        return jsonify({"error": f"An error has occurred: {e}"}), 500
