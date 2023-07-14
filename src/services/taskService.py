from database import db
from src.models.taskModel import Task


class TaskService:
    def __init__(self, task, project_id):
        self.next_tasks = []
        self.previous_tasks = []
        self.task = task
        self.project_id = project_id
        self.inverted_tasks = []
        self.critic_tasks = []

    def get_early_date(self) -> int:
        if not self.task.previous_tasks:
            begin_task = Task.query.filter_by(name="Begin Task", project_id=self.project_id).first()
            self.task.previous_tasks.extend([begin_task])
            self.task.early_date = 0
            self.next_tasks = [task.to_json() for task in self.task.next_tasks]
        else:
            for previous_task in self.task.previous_tasks:
                if self.is_directly_linked_to(previous_task):
                    self.previous_tasks.append(previous_task)

            self.task.previous_tasks = self.previous_tasks
            self.task.early_date = 0

            for previous_task in self.task.previous_tasks:
                if previous_task.name == "Begin Task":
                    self.task.early_date = 0
                elif previous_task.early_date == 0:
                    self.task.early_date = previous_task.duration
                else:
                    max_previous_early_date = max(task.early_date + task.duration for task in self.task.previous_tasks)
                    self.task.early_date = max_previous_early_date

        return self.task.early_date

    def get_late_date(self) -> int:
        # self.next_tasks = [task.to_json() for task in self.task.next_tasks]
        # if not self.next_tasks:
        #     self.task.next_tasks.extend([end_task])
        #     end_duration = self.task.early_date + self.task.duration
        #     end_task.early_date = 0
        #     if end_task.early_date <= end_duration:
        #         end_task.early_date = end_duration
        #         end_task.late_date = end_task.early_date
        #         self.task.late_date = end_task.late_date - self.task.duration
        # else:
        #     for next_task in self.next_tasks:
        #         next_task_late_date = next_task["late_date"]
        #         if next_task_late_date > self.task.late_date:
        #             self.task.late_date = next_task_late_date - self.task.duration
        end_task = Task.query.filter_by(name="End Task", project_id=self.project_id).first()
        end_task.early_date = 0
        self.task.late_date = 0
        for prev_task in end_task.previous_tasks:
            if end_task.early_date < (prev_task.early_date + prev_task.duration):
                end_task.early_date = prev_task.early_date + prev_task.duration
                end_task.late_date = end_task.early_date
        for prev_task in end_task.previous_tasks:
            if prev_task.id == self.task.id:
                self.task.late_date = end_task.late_date - self.task.duration
            if (self.task.late_date - self.task.early_date) == 0:
                self.critic_tasks.append(self.task)
        for task in self.critic_tasks:
            for t in task.previous_tasks:
                if task.late_date - t.duration == t.early_date:
                    t.late_date = task.late_date - t.duration
                    self.critic_tasks.append(t)

        self.critic_tasks.insert(0, end_task)
        # print([task.name for task in self.critic_tasks])
        # for prev_task in self.critic_tasks:
        #     for prev_prev_task in prev_task.previous_tasks:
        #         if prev_prev_task in self.critic_tasks:
        #             continue
        #         elif prev_prev_task.late_date <= prev_task.late_date - prev_prev_task.duration:
        #             prev_prev_task.late_date = prev_task.late_date - prev_task.duration

        tasks = Task.query.filter_by(project_id=self.project_id).all()
        self.inverted_tasks = tasks[::-1]
        for task in self.inverted_tasks:
            next_tasks = [task.to_json() for task in task.next_tasks]
            n_late = end_task.late_date
            for next_task in next_tasks:
                next_task_late_date = next_task["late_date"]
                if next_task_late_date <= n_late:
                    n_late = next_task_late_date
            for next_task in next_tasks:
                next_task_late_date = next_task["late_date"]
                if next_task_late_date == n_late:
                    task.late_date = next_task_late_date - task.duration
        return self.task.late_date

    def get_margin(self) -> int:
        self.task.margin_date = self.task.late_date - self.task.early_date
        return self.task.margin_date

    def get_critic_path(self) -> bool:
        if self.task.margin_date == 0:
            self.task.is_critic = True
        else:
            self.task.is_critic = False
        return self.task.is_critic

    def is_directly_linked_to(self, linked_task):
        visited = set()
        stack = list(self.task.previous_tasks)

        while stack:
            current_task = stack.pop()
            visited.add(current_task)

            if current_task == linked_task:
                return True
            for prev_task in current_task.previous_tasks:
                if prev_task not in visited:
                    stack.append(prev_task)
        return False

    def call_all(self):
        self.get_early_date()
        self.get_late_date()
        self.get_margin()
        self.get_critic_path()


def synchronize_all_task(project_id):
    tasks = Task.query.filter_by(project_id=project_id).all()
    end_task = Task.query.filter_by(name="End Task", project_id=project_id).first()
    end_task_id = end_task.id
    begin_task = Task.query.filter_by(name="Begin Task", project_id=project_id).first()
    for task in tasks:
        service = TaskService(task, project_id)
        if task.name == "Begin Task":
            begin_task.next_tasks = [task for task in begin_task.next_tasks if task.id != end_task_id]
            next_t = [task for task in begin_task.next_tasks]
            for t in next_t:
                next_service = TaskService(t, project_id)
                if next_service.is_directly_linked_to(end_task_id):
                    continue
                else:
                    t.next_tasks = [task for task in t.next_tasks if task.name != "End Task"]

        elif task.name == "End Task":
            previous_tasks = []
            # print(f"{end_task.previous_tasks}\n\n")
            for _previous_task in task.previous_tasks:
                if service.is_directly_linked_to(_previous_task):
                    previous_tasks.append(_previous_task)
            if not end_task.previous_tasks:
                end_task.early_date = 0
                end_task.late_date = 0
        else:
            service.call_all()
