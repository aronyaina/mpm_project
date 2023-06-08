from datetime import datetime
from flask import request, jsonify

from src.models.projectModel import Project
from src.models.taskModel import Task, db
import json


def create_task(project_id):
    task_data = request.get_json()
    try:
        project = Project.query.get(project_id)
        if not project:
            return jsonify({"error": "Project not found"}), 404

        task_name = task_data.get('name')
        task_duration = task_data.get('duration')
        previous_tasks_ids = task_data.get('previous_tasks_id', [])

        if previous_tasks_ids:
            all_exist = True
            ids_not_in_task = []

            for previous_task_id in previous_tasks_ids:
                previous_task_object = Task.query.filter_by(id=previous_task_id).first()

                if previous_task_object:
                    continue
                else:
                    all_exist = False
                    ids_not_in_task.append(previous_task_id)

            if not all_exist:
                return jsonify(
                    {"error": "Previous task does not exist in the database.", "ids_not_in_task": ids_not_in_task}), 404

        try:
            previous_tasks_ids_json = json.dumps(previous_tasks_ids)  # Convert to JSON string

            new_task = Task(
                task_name=task_name,
                task_duration=task_duration,
                project_id=project_id,
                previous_task_ids=previous_tasks_ids_json,  # Store as JSON string
            )
            previous_tasks = Task.query.filter(Task.id.in_(previous_tasks_ids)).all()
            new_task.previous_tasks.extend(previous_tasks)
            db.session.add(new_task)
            db.session.commit()

            new_task_data = new_task.to_json()
            return jsonify(new_task_data)
        except Exception as e:
            print(e)  # Print the error for debugging purposes
            return jsonify({"error": "An error occurred while creating the task."})

    except Exception as e:
        print(e)  # Print the error for debugging purposes
        return jsonify({"error": "An error occurred."}), 404


def update_task(project_id, task_id):
    try:
        project = Project.query.get(project_id)
        if project:
            new_task_name = request.json.get('name')
            new_task_duration = request.json.get('duration')
            new_prev_task = request.json.get('previous_task')

            # check value to update, if it exists then replace with value
            task = Task.query.get(task_id)
            if new_task_name is not None:
                task.name = new_task_name
            if new_task_duration is not None:
                task.duration = new_task_duration
            if new_prev_task is not None:
                task.prevTask = new_prev_task
            task.datetime = datetime.now()

            if task:
                db.session.commit()
                return jsonify(task.to_json())
            else:
                return jsonify({"error": "Task not found"}), 404
        else:
            return jsonify({"error": "Project not found"}), 404

    except Exception as e:
        print(e)
        return jsonify({"error": f"An error has occurred: {e}"}), 500


def delete_task(project_id, task_id):
    try:
        project = Project.query.get(project_id)
        if project:
            task = Task.query.get(task_id)
            if task:
                db.session.delete(task)
                db.session.commit()
                return jsonify(task.to_json())
            else:
                return jsonify({"error": "Task not found"}), 404
        else:
            return jsonify({"error": "Project not found"}), 404
    except Exception as e:
        print(e)
        return jsonify({"error": f"An error has occurred: {e}"}), 500


def get_tasks(project_id):
    try:
        project = Project.query.get(project_id)
        if project:
            tasks = Task.query.filter_by(project_id=project_id).all()
            print(tasks)
            task_list = [task.to_json() for task in tasks]
            print(jsonify(task_list))
            return jsonify(task_list)
        else:
            return jsonify({"error": "Project not found"}), 404
    except Exception as e:
        print(e)
        return jsonify({"error": f"An error has occurred: {e}"}), 500


def get_task_by_id(project_id, task_id):
    try:
        project = Project.query.get(project_id)
        if task_id:
            if project:
                task = Task.query.get(task_id)
                if task:
                    return jsonify(task.to_json())
                else:
                    return jsonify({"error": "Task not found"}), 404
            else:
                return jsonify({"error": "Project not found"}), 404
    except Exception as e:
        print(e)
        return jsonify({"error": f"An error has occurred: {e}"}), 500


def get_next_task(tasks, next_tasks):
    try:
        for task in tasks:
            task_id = task.id
            for task_id_prev in task.prevTask["id"]:
                if task_id_prev in next_tasks:
                    pass
                elif task_id_prev == task_id:
                    next_tasks.append(task_id_prev)
    except Exception as e:
        print(e)
        return jsonify({"error": f"An error has occurred: {e}"}), 500
