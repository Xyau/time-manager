from __future__ import annotations
import logging
from typing import Optional
import streamlit as st

TaskName: str

class TasksManagerConfig:
    # If none, you have unlimited seconds
    seconds_to_answer: Optional[int] = 10

class Task:
    name: TaskName
    seconds: float = 0
    min_seconds: Optional[float] = None
    max_seconds: Optional[float] = None
    impacts: dict[TaskName, float] = {}

    def __init__(self, name: str, impacts: dict[TaskName, float]):
        self.name = name
        self.impacts = impacts

    def __str__(self):
        return self.name

class TaskManager:
    tasks_by_name: dict[TaskName, Task] = {}
    active_task_name: Optional[TaskName] = None

    def __init__(self):
        self.tasks_by_name = {}

    def add_task(self, task: Task):
        if task.name in self.tasks_by_name:
            logging.error("Already exists a task with that name")
            old_seconds = self.get_task(task.name).seconds
            task.seconds = old_seconds
        self.tasks_by_name[task.name] = task

    def get_task(self, task_name: TaskName) -> Task:
        if task_name not in self.tasks_by_name:
            raise f'No task with this name: {task_name}'
        else:
            return self.tasks_by_name[task_name]

    def change_active_task(self, task_name: TaskName):
        logging.error(f'Chaning actinve task {task_name}')
        if task_name not in self.tasks_by_name:
            raise f'No task with this name: {task_name}'
        else:
            self.active_task_name = task_name

    def reset_active_task(self):
        logging.error(f'Reset actinve task ')
        self.active_task_name = None

    def seconds_passed(self, seconds: int):
        if self.active_task_name is not None:
            task: Task = self.get_task(task_name=self.active_task_name)
            for impact_name, constant in task.impacts.items():
                if impact_name in self.tasks_by_name:
                    impacted_task = self.get_task(impact_name)
                    impacted_task.seconds += seconds * constant
                    if impacted_task.max_seconds is not None and impacted_task.seconds > impacted_task.max_seconds:
                        impacted_task.seconds = impacted_task.max_seconds
                    if impacted_task.min_seconds is not None and impacted_task.seconds < impacted_task.min_seconds:
                        impacted_task.seconds = impacted_task.min_seconds

@st.experimental_singleton
def get_task_manager() -> TaskManager:
    return TaskManager()
