import sqlite3
conn = sqlite3.connect('data.db', check_same_thread=False)
c = conn.cursor()


def create_table():
	c.execute('CREATE TABLE IF NOT EXISTS taskstable(task TEXT,task_status TEXT,task_due_date DATE,task_start_time TEXT,task_notes Text)')


def add_data(task, task_status, task_due_date, task_start_time, task_notes):
	c.execute('INSERT INTO taskstable(task,task_status,task_due_date,task_start_time,task_notes) VALUES (?,?,?,?,?)', (task, task_status, task_due_date, task_start_time, task_notes))
	conn.commit()


def view_all_data():
	c.execute('SELECT * FROM taskstable')
	data = c.fetchall()
	return data


def view_all_task_names():
	c.execute('SELECT DISTINCT task FROM taskstable')
	data = c.fetchall()
	return data


def view_all_status_names():
	c.execute('SELECT DISTINCT task_status FROM taskstable')
	data = c.fetchall()
	return data


def view_all_date_names():
	c.execute('SELECT DISTINCT task_due_date FROM taskstable')
	data = c.fetchall()
	return data


def get_task(task):
	c.execute('SELECT * FROM taskstable WHERE task="{}"'.format(task))
	data = c.fetchall()
	return data


def get_task_by_status(task_status):
	c.execute('SELECT * FROM taskstable WHERE task_status="{}"'.format(task_status))
	data = c.fetchall()
	return data


def edit_task_data(new_task, new_task_status, new_task_due_date, new_task_start_time, new_task_notes, task, task_status, task_due_date, task_start_time, task_notes):
	c.execute("UPDATE taskstable SET task =?,task_status=?,task_due_date=?,task_start_time=?,task_notes=? WHERE task=? and task_status=? and task_due_date=? and task_start_time=?and task_notes=?", (new_task, new_task_status, new_task_due_date, new_task_start_time, new_task_notes, task, task_status, task_due_date, task_start_time, task_notes))
	conn.commit()
	data = c.fetchall()
	return data


def delete_data_task(task):
	c.execute('DELETE FROM taskstable WHERE task="{}"'.format(task))
	conn.commit()


def delete_data_date(date):
	c.execute('DELETE FROM taskstable WHERE task_due_date="{}"'.format(date))
	conn.commit()


def delete_data_status(status):
	c.execute('DELETE FROM taskstable WHERE task_status="{}"'.format(status))
	conn.commit()
