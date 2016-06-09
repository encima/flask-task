from taskw import TaskWarrior
from tabulate import tabulate
from operator import itemgetter
from flask_table import Table, Col
import re

class TaskTable(Table):
	#match bootstrap classes
    classes = ["table-responsive", "table-condensed", "table-bordered"]
    id = Col('id')
    description = Col('Description')
    urgency = Col('Urgency')

    def tr_format(self, item):
        if item['urgency'] >= 6:
            return '<tr data-id="{0}" class="{1}">'.format(item['id'], 'important') + "{}</tr>"
        elif item['urgency'] >= 1 and item['urgency'] < 6:
            return '<tr data-id="{0}" class="{1}">'.format(item['id'], 'moderate') + "{}</tr>"
        else:
            return '<tr data-id="{0}" class="{1}">'.format(item['id'], 'normal') + "{}</tr>"

class TW_Loader:

	symbol = "*"

	def __init__(self, config=None):
		if config is not None:
			self.w =  TaskWarrior(config_filename=config)
		else:
			self.w = TaskWarrior()
		self.refresh_tasks()

	def refresh_tasks(self):
		self.tasks = self.w.load_tasks()
		pending = self.tasks['pending']
		# newlist = sorted(pending, key=itemgetter('project', 'urgency'), reverse=True) #reverse=True sorts descending
		self.tasks = {}
		self.task_tables = {}
		for task in pending:
			pr = 'unassigned'
			if 'project' in task:
				pr = task['project']
			if pr in self.tasks:
				self.tasks[pr].append(task)
			else:
				self.tasks[pr] = []
				self.tasks[pr].append(task)
		#create tables from sorted tasks
		for project in self.tasks.keys():
			table = TaskTable(self.tasks[project])
			self.task_tables[project] = table

	def get_tasks(self, project=None):
		if project is None:
			return self.tasks
		elif project in self.tasks:
			return self.tasks[project]
		else:
			return None

	def add_task(self, text):
		#positive lookbehind to match and extract terms
		#task MUST come before project
		task = re.search("(?<=task:)(?:(?!project:).)*", text)
		project = re.search("(?<=project:).*?(?=\s)", text)
		tags = re.findall("\+(\S+)", text)
		urgency = re.search("(?<=urgency:).*?(?=\s)", text)
		due = re.search("(?<=due:).*?(?=\s)", text)
		parsed_task = {}
		if project is not None:
			project = project.group().strip()
		if urgency is not None:
			urgency =  urgency.group().strip()
		if task is not None:
			task =  task.group().strip()
		if due is not None:
			due = due.group().strip()
			#TODO convert to epoch
		self.w.task_add(task, project=project, tags=tags, priority=urgency)
		self.refresh_tasks()
		print(self.tasks)
		parsed_task['task'] = task
		parsed_task['project'] = project
		parsed_task['urgency'] = urgency
		parsed_task['tags'] = tags
		return parsed_task


	def print_tasks(self):
		for project in self.tasks.keys():
			proj = "* {0} *".format(project)
			print(proj)
			print("*" * len(proj))
			print(tabulate(self.tasks[project], headers="keys", tablefmt="pipe"))
			print()

	def get_tables(self, project=None):
		if project is None:
			return self.task_tables
		elif project in self.tasks:
			table = TaskTable(self.tasks[project])
			return table
		else:
			return None

if __name__ == '__main__':
	twl = TW_Loader('./config/taskrc')
	twl.add_task("task:hello there stranger")
	twl.print_tasks()
