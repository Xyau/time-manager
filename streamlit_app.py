import streamlit as st

import src.ui.tasks as ui
st.set_page_config(layout="wide")
st.title("Time Manager")

from src.tasks.tasks import get_task_manager, TaskManager, Task

task_manager: TaskManager = get_task_manager()

CHORES = "Chores"
REMASA = "Remasa"
MEDALLIA = "Medallia"
PLAY = "Play"

chores = Task(CHORES, {
    CHORES: -1.0,
    REMASA: 0.3,
    MEDALLIA: 0.6,
    PLAY: 0.1
})

remasa = Task(REMASA, {
    REMASA: -1.0,
    CHORES: 0.05,
    PLAY: 0.15,
    MEDALLIA: 0.75
})

medallia = Task(MEDALLIA, {
    MEDALLIA: -1.0,
    CHORES: 0.05,
    PLAY: 0.15,
    REMASA: 0.2,
})

play = Task(PLAY, {
    PLAY: -1.0,
    CHORES: 0.3,
    MEDALLIA: 0.4,
    REMASA: 0.3,
})

task_manager.add_task(medallia)
task_manager.add_task(remasa)
task_manager.add_task(play)
task_manager.add_task(chores)

ui.show_tasks()

# import time
#
#
# with st.empty():
#      for seconds in range(60):
#          st.write(f"⏳ {seconds} seconds have passed")
#          time.sleep(1)
#      st.write("✔️ 1 minute over!")
#
# my_bar = st.progress(0)
#
# for percent_complete in range(100):
#      time.sleep(0.1)
#      my_bar.progress(percent_complete + 1)

