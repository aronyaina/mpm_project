from src.models.taskModel import Task


class DateOperation:
    def __init__(self, task):
        self.task = task
        self.max_date = 0
        self.min_date = 0
        self.margin_date = 0

    def get_early_date(self, previous_tasks) -> int:
        if previous_tasks is None:
            return self.max_date
        else:
            for prev_task_id in self.task.prevTask["id"]:
                prev_task_early_date = Task.query.get(prev_task_id).earlyDate
                if prev_task_early_date >= self.max_date:
                    self.max_date = prev_task_early_date
            return self.max_date

    def get_late_date(self, next_tasks) -> int:
        if next_tasks is None:
            return self.min_date
        else:
            for prev_task_id in self.task.prevTask["id"]:
                prev_task_late_date = Task.query.get(prev_task_id).lateDate
                if prev_task_late_date <= self.min_date:
                    self.min_date = prev_task_late_date
            return self.min_date

    def get_margin(self) -> int:
        self.margin_date = self.max_date - self.min_date
        return self.margin_date

    def get_critic_path(self) -> bool:
        if self.margin_date == 0:
            return True
        else:
            return False
