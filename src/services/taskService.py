from src.models.taskModel import Task


class TaskService:
    def __init__(self, task, project_id):
        self.next_tasks = []
        self.previous_tasks = []
        self.task = task
        self.project_id = project_id

    def get_early_date(self) -> int:
        if not self.task.previous_tasks:
            begin_task = Task.query.filter_by(name="Begin Task", project_id=self.project_id).first()
            self.task.previous_tasks.extend([begin_task])
            self.task.early_date = begin_task.early_date
            self.next_tasks = [task.to_json() for task in self.task.next_tasks]
        else:
            for previous_task in self.task.previous_tasks:
                if self.is_directly_linked_to(previous_task):
                    self.previous_tasks.append(previous_task)

            self.task.previous_tasks = self.previous_tasks
            self.task.early_date = 0
            self.task.early_date = max(previous_task.early_date for previous_task in self.task.previous_tasks) \
                                   + self.task.duration
        return self.task.early_date

    def get_late_date(self) -> int:
        self.next_tasks = [task.to_json() for task in self.task.next_tasks]
        end_task = Task.query.filter_by(name="End Task", project_id=self.project_id).first()
        if not self.next_tasks:
            self.task.next_tasks.extend([end_task])
            end_duration = self.task.early_date + self.task.duration
            end_task.early_date = 0
            if end_task.early_date <= end_duration:
                end_task.early_date = end_duration
            end_task.late_date = end_task.early_date
            self.task.late_date = end_task.late_date - self.task.duration
        else:
            for next_task in self.next_tasks:
                next_task_late_date = next_task["late_date"]
                if next_task_late_date <= self.task.late_date:
                    self.task.late_date = next_task_late_date - self.task.duration
        return max(0, self.task.late_date)

    def get_margin(self) -> int:
        self.task.margin_date = self.task.late_date - self.task.early_date
        return self.task.margin_date

    def get_critic_path(self) -> bool:
        if self.task.margin_date == 0:
            self.task.is_critic = True
            return self.task.is_critic

    def is_directly_linked_to(self, linked_task):
        visited = set()
        stack = list(self.task.previous_tasks)

        while stack:
            current_task = stack.pop()
            visited.add(current_task)

            if current_task == linked_task:
                return True
            if current_task.name == "End Task":
                continue
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
            for _previous_task in task.previous_tasks:
                if service.is_directly_linked_to(_previous_task):
                    previous_tasks.append(_previous_task)
            end_task.previous_tasks = previous_tasks
            if not end_task.previous_tasks:
                end_task.early_date = 0
                end_task.late_date = 0
        else:
            service.call_all()
