import streamlit as st
import requests
from datetime import datetime
import time

st.set_page_config(
    page_title= "📝Todo Task Manager", 
    layout='wide'
)

if 'msg' in st.session_state:
    st.success(st.session_state['msg'])
    del st.session_state['msg']

BASE_URL = 'http://127.0.0.1:8000'

# Making a Sidebar
sidebar = st.sidebar
sidebar.title('📋TODO APP')
# sidebar.markdown('----')
sidebar.markdown('----')
sidebar.header('Task Management System')
sidebar.write(
    """
    ## 🚀Features 
    - Create Tasks
    - View Tasks
    - Delete Tasks 
    - Mark Complete 
    """
)


# ======================================
# CREATE TASK SECTION
# ======================================

## Input Area
st.header('✍️Create New Task')
with st.form('create_task', clear_on_submit=True):
    title = st.text_input(label = 'Task Title ')
    description = st.text_area(label = 'Task Description')
    priority = st.selectbox(
        label = 'Task Priority', 
        options = ['Low', 'Medium', 'High']
    )
    create_task_button = st.form_submit_button('➕ Create Task')

if create_task_button:
    if title.strip() == '':
        st.warning("Title Cannot Be Empty")
    elif description.strip() == '':
        st.warning("Description Cannot Be Empty")
    else:
        task_data = {
            "title": title,
            "description": description,
            "priority": priority
        }

        post_response = requests.post(f'{BASE_URL}/tasks', json=task_data)

        if post_response.status_code == 200:
            st.session_state['msg'] = 'Task Created Successfully'
            st.rerun()
        else:
            st.error('Failed to Create Task')




## GET ALL THE TASKS
try:
    get_response = requests.get(f'{BASE_URL}/tasks', timeout = 10)
    tasks = get_response.json()['tasks']
except Exception:
    st.error("Can't Connect to FastAPI Server. Make Sure Uvicorn is Running")
    st.stop()

st.header('📊Tasks Information')

# ===========================================
# TASK MATRICS SECTION
# ===========================================

total_tasks = len(tasks)
completed_tasks = sum([1 for task in tasks if task['completed'] == 1])
pending_tasks = total_tasks - completed_tasks

c1, c2, c3 = st.columns(3)

c1.metric(label = 'Total Tasks', value = total_tasks, border = True)
c2.metric(label = 'Completed', value = completed_tasks, border = True)
c3.metric(label = 'Pending Tasks', value = pending_tasks, border= True)




# =======================================
# VIEW TASK SECTION
# =======================================

if len(tasks) == 0:
    st.info('No Task Available')
else:
    all_tasks = []
    for task in tasks:

        colored_priority = ''
        if task['priority'] == 'High':
            colored_priority = '🔴High'
        elif task['priority'] == 'Medium':
            colored_priority = '🟡Medium'
        else:
            colored_priority = '🟢Low'

        updated_colname_task = {
            'ID' : str(task['id']),
            'Title': task['title'], 
            'Description': task['description'],
            'Priority' : colored_priority,
            'Status': "Completed✔️" if task['completed'] == 1 else 'Pending⌛',
            'Created At': datetime.fromisoformat(task['created_at'])
        }
        all_tasks.append(updated_colname_task)

    st.dataframe(
        all_tasks, 
        use_container_width = True
    )
st.divider()



# ==============================
# TASK ACTION SECTION
# ==============================

st.header('🛠️Task Action')
if tasks:
    task_options = {f"{task['id']} - {task['title']}" : task['id'] for task in tasks}

    selected_task = st.selectbox(
        label = 'Select Task',
        options= list(task_options.keys())
    )

    selected_task_id = task_options[selected_task]

    col1, col2 = st.columns(2)

    # col1 -> Mark Complete Button
    mark_complete_button = col1.button('✅Mark Complete')
    if mark_complete_button:
        complete_response = requests.patch(f'{BASE_URL}/tasks/{selected_task_id}')
        if complete_response.status_code == 200:
            st.success('Task Marked Completed')
            time.sleep(1.5)
            st.rerun()
        else:
            st.error('Failed to Mark Complete')


    # col2 -> Delete Button
    del_button = col2.button('🗑️Delete Task')
    if del_button:
        del_response = requests.delete(f'{BASE_URL}/tasks/{selected_task_id}')
        if del_response.status_code == 200:
            st.success('Task Deleted Successfully')
            time.sleep(1.5)
            st.rerun()
        else:
            st.error('Failed to Delete Task')
else:
    st.info('Add Tasks To Perform Actions')