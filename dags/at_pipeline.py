"""
Code that goes along with the Airflow located at:
http://airflow.readthedocs.org/en/latest/tutorial.html
"""

# import gzip
from airflow import DAG
from airflow.operators import PythonOperator
from datetime import datetime, timedelta

from at.at_api import get_key, get_bus_locations

from json import dumps


default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2018, 10, 22, 12, 0, 0),
    "email": ["airflow@airflow.com"],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2016, 1, 1),
}

dag = DAG("at-pipeline", default_args=default_args,
          schedule_interval=timedelta(minutes=1))


def pipe_bus_locations(ds, **kwargs):
    print(kwargs)

    # retrieve API key
    api_key = get_key()

    # retrieve bus locations from API
    response = get_bus_locations(api_key)

    # store bus locations to disk
    file_name = 'data/%s.json' % kwargs['ts_nodash'][:-5]
    with open(file_name, 'w') as f:
        print('Exporting response to "%s"' % file_name)
        f.write(dumps(response))

    return 'Done'


run_this = PythonOperator(
    task_id='busloc',
    provide_context=True,
    python_callable=pipe_bus_locations,
    dag=dag)
