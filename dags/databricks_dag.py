from airflow import DAG
from airflow.providers.databricks.operators.databricks import DatabricksRunNowOperator
from airflow.utils.dates import days_ago

default_args = {
    'owner': 'airflow'
}

with DAG('databricks_dag',
    start_date = days_ago(2),
    schedule_interval = None,
    default_args = default_args
) as dag:
    
    opr_run_now = DatabricksRunNowOperator(
        task_id = 'run_now',
        databricks_conn_id = 'databricks', # Nome do Conn Id da List Connection
        job_id = 154868913729452 # Access tokens gerado no Databricks 
    )