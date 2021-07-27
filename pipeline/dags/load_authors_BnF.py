import os.path
from datetime import timedelta
from re import template

# The DAG object; we'll need this to instantiate a DAG
from airflow import DAG
from airflow.models import Variable
from airflow.models.connection import Connection
# Operators; we need this to operate!
from airflow.operators.bash import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago

# These args will get passed on to each operator
# You can override them on a per-task basis during operator initialization
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email": ["airflow@example.com"],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 0,
    "retry_delay": timedelta(minutes=5),
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2016, 1, 1),
    # 'wait_for_downstream': False,
    # 'dag': dag,
    # 'sla': timedelta(hours=2),
    # 'execution_timeout': timedelta(seconds=300),
    # 'on_failure_callback': some_function,
    # 'on_success_callback': some_other_function,
    # 'on_retry_callback': another_function,
    # 'sla_miss_callback': yet_another_function,
    # 'trigger_rule': 'all_success'
}

DATA_DIR = Variable.get("data_path", "/data")

download_command = 'curl {{params.source}} -o {{params.destination}} --create-dirs'
#download_command_wget = 'compgen -A function -abck'
extract_command_tar = 'tar xzf {{params.file}}'
load_command_curl = ' echo "my loop curl -D -H \"Content-Type:application/n-triples\" --upload-file file -X POST \"{{params.url}}/namespace/{{params.namespace}}/sparql?context-uri={{params.graph}}\"'
clean_command_rm = ' rm {{params.files}}'

with DAG(
    "load_authors_BnF_test",
    default_args=default_args,
    description="Extract the large RDF dumps from the French National Library (BnF) containing authors and load them into a named graph in a triple store.",
    schedule_interval=None,  # timedelta(days=1),
    start_date=days_ago(2),
    tags=["authors", "authorities", "BnF", "RDF"]
) as dag:

    #
    # Download dump files (1/4)
    #
    download_authors_persons = BashOperator(
        task_id="download_authors_persons_bnf_test",
        bash_command=download_command,
        params={'source': Variable.get("data_source_authors_persons_bnf"),
                'destination': os.path.join(*[DATA_DIR, Variable.get("data_dest_authors_bnf"), Variable.get("data_dest_authors_persons_bnf")])}
    )

    download_authors_orgs = BashOperator(
        task_id="download_authors_orgs_bnf_test",
        bash_command=download_command,
        params={'source': Variable.get("data_source_authors_orgs_bnf"),
                'destination': os.path.join(*[DATA_DIR, Variable.get("data_dest_authors_bnf"), Variable.get("data_dest_authors_orgs_bnf")])}
    )

    #
    # Extract triples from dumps (2/4)
    #
    extract_authors_persons = BashOperator(
        task_id="extract_authors_persons_bnf_test",
        bash_command=extract_command_tar,
        params={'file': os.path.join(*[DATA_DIR, Variable.get("data_dest_authors_bnf"), Variable.get("data_dest_authors_persons_bnf")])}
    )

    extract_authors_orgs = BashOperator(
        task_id="extract_authors_orgs_bnf_test",
        bash_command=extract_command_tar,
        params={'file': os.path.join(*[DATA_DIR, Variable.get("data_dest_authors_bnf"), Variable.get("data_dest_authors_orgs_bnf")])}
    )

    #
    # Load triples into triple store (3/4)
    #
    load_authors = BashOperator(
        task_id="load_authors_bnf_test",
        bash_command=load_command_curl,
        # No trailing slash at the end of the url
        params={'url': "http://localhost:8090/", 'namespace': Variable.get("namespace_bnf"), 'graph': Variable.get("graph_authors_bnf")}
    )

    #
    # Clean up what was downloaded/extracted (4/4)
    #
    clean_rdf_files = BashOperator(
        task_id="clean_rdf_files_authors_bnf_test",
        bash_command=clean_command_rm,
        params={'files': os.path.join(*[DATA_DIR, Variable.get("data_dest_authors_bnf"), "*.nt"])}
    )

    clean_dump_files = BashOperator(
        task_id="clean_dump_files_authors_bnf_test",
        bash_command=clean_command_rm,
        params={'files': os.path.join(*[DATA_DIR, Variable.get("data_dest_authors_bnf"), "*.tar.gz"])}
    )

download_authors_persons >> extract_authors_persons
download_authors_orgs >> extract_authors_orgs

[extract_authors_persons, extract_authors_orgs] >> load_authors
load_authors >> clean_rdf_files >> clean_dump_files

