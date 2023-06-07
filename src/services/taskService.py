from datetime import datetime
from flask import request, jsonify

from src.models.projectModel import Project
from src.models.taskModel import Task, db


def create_task(project_id):
    """
    Create a new task and associate it with a project.

    Args:
        project_id (int): The ID of the project to associate the task with.

    Returns:
        Response: A JSON response containing the created task if successful,
        or an error message if an error occurs.
    """
    task_data = request.get_json()
    try:
        project = Project.query.get(project_id)
        if not project:
            return jsonify({"error": "Project not found"}), 404
        db.create_all()

        task_name = task_data.get('name')
        task_duration = task_data.get('duration')
        previous_tasks = task_data.get('previous_tasks')

        if previous_tasks is not None:
            all_exist = True
            id_not_in_task = []

            for previous_task in previous_tasks:
                id = previous_task['id']
                previous_task_object = Task.query.filter_by(id=id).first()

                if previous_task_object:
                    continue
                else:
                    all_exist = False
                    id_not_in_task.append(id)

            if not all_exist:
                return jsonify(
                    {"error": "Previous task does not exist in the database.", "id_not_in_task": id_not_in_task}), 404

        try:
            new_task = Task(
                task_name=task_name,
                task_duration=task_duration,
                project_id=project_id
            )

            if previous_tasks is not None:
                for previous_task in previous_tasks:
                    id = previous_task['id']
                    previous_task_object = Task.query.get(id)
                    previous_task_data = previous_task_object.to_json()
                    print(f"previous_task_data:{previous_task_data}")
                    previous_task_data['previous_task_data'] = previous_task_data
                    new_task.prevTasks.append(previous_task_data)

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
            tasks = Task.query.filter_by(projectId=project_id).all()
            task_list = [task.to_json() for task in tasks]
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
