from datetime import datetime

from flask import request, jsonify

from database import db
from src.models.projectModel import Project
from src.models.taskModel import Task
from src.services.taskService import TaskService, synchronize_all_task


def create_task(project_id):
    task_data = request.get_json()
    try:
        project = Project.query.get(project_id)
        if not project:
            return jsonify({"error": "Project not found"}), 404

        task_name = task_data.get('name')
        task_duration = task_data.get('duration')
        previous_tasks_names = task_data.get('previous_tasks_name', [])

        if Task.query.filter_by(name=task_name, project_id=project_id).first():
            return jsonify({"error": "Task name already exists."}), 400

        previous_tasks = []
        if previous_tasks_names:
            name_not_in_task = []

            for previous_task_name in previous_tasks_names:
                previous_task_object = Task.query.filter_by(name=previous_task_name).first()
                if previous_task_object:
                    previous_tasks.append(previous_task_object)
                else:
                    name_not_in_task.append(previous_task_name)

            if name_not_in_task:
                return jsonify({"name_not_in_task": name_not_in_task}), 404

        try:
            new_task = Task(
                name=task_name,
                duration=task_duration,
                project_id=project_id
            )
            new_task.previous_tasks.extend(previous_tasks)
            db.session.add(new_task)
            db.session.commit()
            new_service = TaskService(new_task, project_id)
            try:
                new_service.call_all()

                db.session.commit()
            except Exception as e:
                print(e)
                db.session.delete(Task.query.filter_by(name=task_name).first())
                db.session.commit()

            new_task_data = new_task.to_json()
            return jsonify(new_task_data)

        except Exception as e:
            print(e)  # Print the error for debugging purposes
            return jsonify({"error": f"{e}"})

    except Exception as e:
        print(e)  # Print the error for debugging purposes
        return jsonify({"error": f"{e}"}), 500


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


def get_all_task(project_id):
    try:
        project = Project.query.get(project_id)
        if project:
            task_name = request.args.get('task_name')
            if task_name:
                task = Task.query.filter_by(name=task_name, project_id=project_id).first()
                if task:
                    return jsonify(task.to_json())
                else:
                    return jsonify({"error": "Task not found"}), 404

            synchronize_all_task(project_id)
            tasks = Task.query.filter_by(project_id=project_id).all()
            task_list = [task.to_json() for task in tasks]
            return jsonify(task_list)
        else:
            return jsonify({"error": "Project not found"}), 404
    except Exception as e:
        print(e)
        return jsonify({"error": f"{e}"}), 500


def delete_task_by_id(project_id, task_id):
    try:
        project = Project.query.get(project_id)
        if not project:
            return jsonify({"error": "Project not found"}), 404

        task = Task.query.get(task_id)
        if task_id == 1:
            return jsonify({"error": "Impossible to delete beginning task"})
        if task_id == 2:
            return jsonify({"error": "Impossible to delete end task"})
        if not task:
            return jsonify({"error": "Task not found"}), 404
        # begin task
        tasks_with_previous_task = Task.query.filter(Task.previous_tasks.any(id=task_id)).all()

        for t in tasks_with_previous_task:
            t.previous_tasks.remove(task)
            # new_task_service = TaskService(t, project_id)
            # new_task_service.get_early_date()

        db.session.delete(task)
        db.session.commit()

        return jsonify({"message": "Task deleted successfully"})

    except Exception as e:
        return jsonify({"error": f"{e}"}), 500
    # Call the delete_task function to delete a task by its ID within a specific project


def update_task_by_id(project_id, task_id):
    try:
        project = Project.query.get(project_id)
        if not project:
            return jsonify({"error": "Project not found"}), 404

        task = Task.query.get(task_id)
        if not task:
            return jsonify({"error": "Task not found"}), 404

        new_task_name = request.json.get('name')
        new_task_duration = request.json.get('duration')
        new_prev_task = request.json.get('previous_task_id')

        if new_task_name is not None:
            task.name = new_task_name
        if new_task_duration is not None:
            task.duration = new_task_duration

        # Check if the previous task exists
        if new_prev_task is not None:
            previous_task = Task.query.filter_by(name=new_prev_task).first()
            if previous_task:
                task.previous_task = previous_task.id
            else:
                return jsonify({"error": "Previous task name doesn't exist.", "name_not_in_task": new_prev_task}), 404

        task.datetime = datetime.now()
        db.session.commit()

        return jsonify(task.to_json())

    except Exception as e:
        print(e)
        return jsonify({"error": "An error occurred."}), 500
    # Call the update_task function to update a task by its ID within a specific project

# def get_task_by_name(project_id):
#     task_name = request.args.get('task_name')
#     print(task_name)
#     try:
#         project = Project.query.get(project_id)
#         if task_name:
#             if project:
#                 task = Task.query.filter_by(name=task_name).first()
#                 if task:
#                     return jsonify(task.to_json())
#                 else:
#                     return jsonify({"error": "Task not found"}), 404
#             else:
#                 return jsonify({"error": "Project not found"}), 404
#     except Exception as e:
#         print(e)
#         return jsonify({"error": f"An error has occurred: {e}"}), 500
