from datetime import datetime
from flask import jsonify, request
from src.models.projectModel import Project
from src.models.taskModel import Task
from database import db


def create_project():
    project_data = request.get_json()
    try:
        project_name = project_data.get('name')
        if Project.query.filter_by(name=project_name).first():
            return jsonify({"error": "Project name already exists."}), 400

        new_project = Project(name=project_name)
        db.session.add(new_project)
        db.session.commit()

        begin_task = Task(
            name="Begin Task",
            duration=0,
            project_id=new_project.id
        )
        begin_task.is_critic = True
        db.session.add(begin_task)

        end_task = Task(
            name="End Task",
            duration=0,
            project_id=new_project.id
        )
        end_task.is_critic = True
        db.session.add(end_task)
        db.session.commit()

        return jsonify(new_project.to_json())

    except Exception as e:
        return jsonify({"error": f"{e}"}), 500

    # Call the create_project function to create a new project


def delete_project_by_id(project_id):
    try:
        project = Project.query.get(project_id)
        if project:
            db.session.delete(project)
            db.session.commit()
            return jsonify(project.to_json())
        else:
            return jsonify({"error": "Project not found"}), 500
    except Exception as e:
        return jsonify({"error": f"{e}"}), 500


def update_project_by_id(project_id):
    try:
        new_project_name = request.json.get('name')
        project = Project.query.get(project_id)
        if project:
            project.name = new_project_name
            project.datetime = datetime.now()
        db.session.commit()
        return jsonify(project.to_json())

    except Exception as e:
        return jsonify({"error": f"{e}"}), 500


def get_project_by_id(project_id):
    try:
        # Logic to retrieve a specific project with project_id
        project = Project.query.get(project_id)
        if project:
            return jsonify(project.to_json())
        else:
            return jsonify({"error": "Project not found"}), 404
    except Exception as e:
        return jsonify({"error": f"{e}"}), 500


def get_all_project():
    try:
        # Logic to retrieve all projects
        projects = Project.query.all()
        if projects:
            return jsonify([project.to_json() for project in projects])
        else:
            return jsonify({"error": "Project not found"}), 500
    except Exception as e:
        return jsonify({"error": f"{e}"}), 500
