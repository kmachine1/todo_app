import streamlit as st
import pandas as pd 
from db_funcs import *
from PIL import Image
import plotly.express as px
from datetime import datetime


def color_df(val):
	if val == "Done":
		color = "green"
	elif val == "Doing":
		color = "orange"
	else:
		color = "red"

	return f'background-color: {color}'


st.set_page_config(
	page_title="ToDo",
	page_icon="📝",
	layout="wide",
	initial_sidebar_state="expanded",
)

top_image = Image.open('static/banner_top.png')
bottom_image = Image.open('static/banner_bottom.png')
main_image = Image.open('static/main_banner.png')

st.image(main_image, use_column_width='always')
st.title("📄 ToDo App 🗣")

st.sidebar.image(top_image, use_column_width='auto')
choice = st.sidebar.selectbox("Menu", ["Create Task ✅", "Update Task 👨‍💻", "Delete Task ❌", "View Tasks' Status 👨‍💻"])
st.sidebar.image(bottom_image, use_column_width='auto')
create_table()

if choice == "Create Task ✅":
	st.subheader("Add Item")

	col1, col2 = st.columns(2)

	with col1:
		task = st.text_area("Task To Do")
		task_notes = st.text_area("Task Notes")

	with col2:
		task_status = st.selectbox("Status", ["ToDo", "Doing", "Done"])
		task_due_date = st.date_input("Due Date")
		task_start_time = str(st.time_input("Due Time"))

	if st.button("Add Task"):
		list_of_tasks = [i[0] for i in view_all_task_names()]
		if (task != '') and (task not in list_of_tasks):
			add_data(task, task_status, task_due_date, task_start_time, task_notes)
			st.success("Added Task \"{}\" ✅".format(task))
			st.snow()
		else:
			st.error('This is an error', icon="🚨")

	with st.expander("View Updated Data 💫"):
		result = view_all_data()
		# st.write(result)
		clean_df = pd.DataFrame(result, columns=["Task", "Status", "Date", "Due_Time", "Notes"])
		st.dataframe(clean_df.style.applymap(color_df, subset=['Status']))

elif choice == "Update Task 👨‍💻":
	st.subheader("Edit Items")
	with st.expander("Current Data"):
		result = view_all_data()
		clean_df = pd.DataFrame(result, columns=["Task", "Status", "Date", "Due_Time", "Notes"])
		st.dataframe(clean_df.style.applymap(color_df, subset=['Status']))

	list_of_tasks = [i[0] for i in view_all_task_names()]
	selected_task = st.selectbox("Task", list_of_tasks)
	task_result = get_task(selected_task)

	if task_result:
		task = task_result[0][0]
		task_status = task_result[0][1]
		task_due_date = task_result[0][2]
		task_start_time = task_result[0][3]
		task_notes = task_result[0][4]

		col1, col2 = st.columns(2)

		with col1:
			new_task = st.text_area("Task To Do", task)
			new_task_notes = st.text_area("Task Notes", task_notes)

		with col2:

			status_list = ["ToDo", "Done", "Doing"]
			old_status = [i for i, j in enumerate(status_list) if j == task_status]

			new_task_status = st.selectbox("Task Status", status_list, index=old_status[0])
			task_due_date = datetime.strptime(task_due_date, '%Y-%m-%d').date()
			new_task_due_date = st.date_input('Due Date', value=task_due_date)
			new_task_start_time = str(st.time_input("Due Time"))

		if st.button("Update Task 👨‍💻"):
			edit_task_data(new_task, new_task_status, new_task_due_date, new_task_start_time, new_task_notes, task, task_status, task_due_date, task_start_time, task_notes)
			st.success("Updated Task \"{}\" ✅".format(task, new_task))

		with st.expander("View Updated Data 💫"):
			result = view_all_data()
			# st.write(result)
			clean_df = pd.DataFrame(result, columns=["Task", "Status", "Date", "Due_Time", "Notes"])
			st.dataframe(clean_df.style.applymap(color_df, subset=['Status']))

elif choice == "Delete Task ❌":
	st.subheader("Delete")
	with st.expander("View Data"):
		result = view_all_data()
		# st.write(result)
		clean_df = pd.DataFrame(result, columns=["Task", "Status", "Date", "Due_Time", "Notes"])
		st.dataframe(clean_df.style.applymap(color_df, subset=['Status']))

	unique_list = [i[0] for i in view_all_task_names()]
	unique_list1 = [i[0] for i in view_all_date_names()]
	unique_list2 = [i[0] for i in view_all_status_names()]

	delete_by_task_date = st.selectbox("Select Date", unique_list1)
	if st.button("Delete by Date ❌"):
		delete_data_date(delete_by_task_date)
		st.warning("Deleted Date \"{}\" ✅".format(delete_by_task_date))

	delete_by_task_name = st.selectbox("Select Task", unique_list)
	if st.button("Delete by Task ❌"):
		delete_data_task(delete_by_task_name)
		st.warning("Deleted Task \"{}\" ✅".format(delete_by_task_name))

	delete_by_task_status = st.selectbox("Select Status", unique_list2)
	if st.button("Delete by Status 💯"):
		delete_data_status(delete_by_task_status)
		st.warning("Deleted Status \"{}\" ✅".format(delete_by_task_status))

	with st.expander("View Updated Data 💫"):
		result = view_all_data()
		# st.write(result)
		clean_df = pd.DataFrame(result, columns=["Task", "Status", "Date", "Due_Time", "Notes"])
		st.dataframe(clean_df.style.applymap(color_df, subset=['Status']))

else:
	result = view_all_data()
	# st.write(result)
	clean_df = pd.DataFrame(result, columns=["Task", "Status", "Date", "Due_Time", "Notes"])

	clean_df['Date'] = pd.to_datetime(clean_df['Date'])

	clean_df = clean_df[clean_df['Date'].dt.date == datetime.today().date()]
	with st.expander("View All 📝"):

		st.dataframe(clean_df.style.applymap(color_df, subset=['Status']))

	with st.expander("Task Status 📝"):
		task_df = clean_df['Status'].value_counts().to_frame()
		task_df = task_df.reset_index()
		st.dataframe(task_df)

		p1 = px.pie(task_df, names='Status', values='count', color_discrete_map={'ToDo': 'red', 'Done': 'green', 'Doing': 'orange'})
		st.plotly_chart(p1, use_container_width=True)

	with st.expander("Task Score 🏆"):
		task_df = clean_df['Status'].value_counts().to_frame()
		task_df = task_df.reset_index()
		try:
			task_score = len(clean_df[clean_df['Status'] == 'Done'])/len(clean_df['Status'])
		except ZeroDivisionError:
			task_score = 0

		st.dataframe(task_df)

		if task_score < 0.6:
			st.write(f'<p style="font-size:40px; text-align: center; color:red;">You FAILED, do better next time!!! {task_score:.0%}</p>', unsafe_allow_html=True)

		elif 0.6 < task_score < 0.8:
			st.write(f'<p style="font-size:40px; text-align: center; color:orange;">You are doing ALRIGHT, keep improving!!! {task_score:.0%}</p>', unsafe_allow_html=True)

		else:
			st.write(f'<p style="font-size:40px; text-align: center; color:green;">SUCCESS keep, consistent!!! {task_score:.0%}</p>', unsafe_allow_html=True)
