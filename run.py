import json
from datetime import datetime
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator
from airflow.models import Variable
from airflow.models import DAG

# default args, that will be used with dag
default_args = {'owner': 'airflow',
                'start_date': datetime(2020, 1, 1)
                }

# this will be executed as dag
dag = DAG(
    dag_id='test_task',
    default_args=default_args,
    schedule_interval='0 0 * * *',
    tags=['Task with bash and python operators']
)

#function for PythonOperator (must be dynamic? have no solution for generating callable from string)
def meow():
    print("python meow")
    
# dictionary for tasks
taskMap = {}

# open json - path is in Airflow variable
with open(Variable.get("json_home"), "r") as read_file:
    data = json.load(read_file)
    # iterating through json
    dagNodes = data["DagNodes"]
    for id, values in dagNodes.items():
        # get params for each task
        task_id = values["taskName"]
        command = values["command"]
        trigger_rule = values["trigger_rule"]
        command_type = values["command_type"]
        if command_type == "bash_operator":
            taskMap[task_id] = BashOperator(
                task_id=task_id,
                bash_command=command,
                trigger_rule=trigger_rule,
                dag=dag,
            )
        if command_type == "python_operator":
            taskMap[task_id] = PythonOperator(
                task_id=task_id,
                python_callable=meow,
                trigger_rule=trigger_rule,
                dag=dag,
            )
    dagEdges = data["DagEdges"]
    # lets compose tasks
    for task_id, dependencies in dagEdges.items():
        for dependency in dependencies:
            taskMap[task_id] >> taskMap[dependency]
