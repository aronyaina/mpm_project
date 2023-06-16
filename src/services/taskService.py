from src.models.taskModel import Task


class TaskService:
    def __init__(self, task):
        self.next_tasks = []
        self.task = task

    def get_early_date(self) -> int:
        if not self.task.previous_tasks:
            begin_task = Task.query.get(1)
            self.task.previous_tasks.extend([begin_task])
            self.task.early_date = self.task.duration + begin_task.early_date
        else:
            for previous_task in self.task.previous_tasks:
                prev_task_early_date = previous_task.early_date
                if prev_task_early_date >= self.task.early_date:
                    self.task.early_date = prev_task_early_date + self.task.duration
        return self.task.early_date

    def get_late_date(self) -> int:
        self.next_tasks = [task.to_json() for task in self.task.next_tasks]
        if not self.next_tasks:
            end_task = Task.query.get(2)
            self.task.next_tasks.extend([end_task])
            end_duration = self.task.early_date + self.task.duration
            if end_task.early_date <= end_duration:
                end_task.early_date = self.task.early_date + self.task.duration
            end_task.late_date = end_task.early_date
            self.task.late_date = end_task.late_date - self.task.duration
        else:
            for next_task in self.next_tasks:
                next_task_late_date = next_task.late_date
                if next_task_late_date <= self.task.late_date:
                    self.task.late_date = next_task_late_date - self.task.duration
        if self.task.late_date < 0:
            return 0
        else:
            return self.task.late_date

    def get_margin(self) -> int:
        self.task.margin_date = self.task.late_date - self.task.early_date
        return self.task.margin_date

    def get_critic_path(self) -> bool:
        if self.task.margin_date == 0:
            self.task.is_critic = True
            return self.task.is_critic
