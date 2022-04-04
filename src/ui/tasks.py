import streamlit as st
import time

from src.tasks.tasks import Task, get_task_manager, TaskManager

def format_time(seconds: float) -> str:
    seconds = int(seconds)
    negative = seconds < 0
    seconds = -1*seconds if negative else seconds
    s = '-' if negative else ""
    if seconds > 3600:
        hours = int(seconds / 3600)
        s += f'{hours}h '
        seconds = seconds % 3600
    if seconds > 60:
        mins = int(seconds / 60)
        s += f'{mins}m '
        seconds = seconds % 60
    if s != 0:
        s += f'{seconds}s'
    return s.strip()

def show_tasks():
    task_manager: TaskManager = get_task_manager()
    tasks: list[Task] = list(task_manager.tasks_by_name.values())
    placeholders = []
    impact_per_task = {}
    if task_manager.active_task_name is not None:
        impact_per_task = task_manager.get_task(task_manager.active_task_name).impacts
    for task in tasks:
        col1, col2, col3 = st.columns(3)
        if col3.button(label="Reset", key=f'Reset{task.name}'):
            task.seconds = 0
        if task_manager.active_task_name == task.name:
            if col2.button(label=f'Deactivate: {task.name}'):
                task_manager.reset_active_task()
                st.experimental_rerun()
        else:
            if col2.button(label=f'Activate: {task.name}'):
                task_manager.change_active_task(task.name)
                st.experimental_rerun()
        placeholder = col1.empty()
        placeholders.append((task, placeholder))

    while True:
        for task, placeholder in placeholders:
            active = task_manager.active_task_name == task.name
            active_str = "ACTIVE" if active else "INACTIVE"
            delta = impact_per_task[task.name] if task.name in impact_per_task else 0
            color = "red" if delta < 0 else "green"
            delta_str = "" if delta == 0 else f'<span style="color:{color}">({"+" if delta > 0 else ""}{delta})</span>'
            placeholder.markdown(f'**{active_str}**: {task.name} has {format_time(task.seconds)} {delta_str} available', unsafe_allow_html=True)
        time.sleep(1)
        task_manager.seconds_passed(1)
        if task_manager.active_task_name is None:
            st.stop()


