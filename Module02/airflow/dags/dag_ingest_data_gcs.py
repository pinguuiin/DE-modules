import os
from datetime import datetime
from pathlib import Path

from airflow import DAG
from airflow.sdk import task
from airflow.providers.http.hooks.http import HttpHook
from airflow.providers.google.cloud.operators.bigquery import BigQueryCreateTableOperator


from google.cloud import storage
# import pyarrow.csv as pv
# import pyarrow.parquet as pq


# -------------------------------------------------------------------
# CONFIG
# -------------------------------------------------------------------
PROJECT_ID = os.environ.get("GCP_PROJECT_ID", "long-sonar-485113-u0")
BUCKET = os.environ.get("GCP_GCS_BUCKET", "bucket-pingu")
BIGQUERY_DATASET = os.environ.get("BIGQUERY_DATASET", "taxi_dataset")

AIRFLOW_HOME = Path(os.environ.get("AIRFLOW_HOME", "/opt/airflow"))

BASE_URL_CONN_ID = "cloudfront_nyc_taxi"
BASE_PATH = "trip-data"

GCS_PREFIX = "raw/yellow"

# -------------------------------------------------------------------
# DAG
# -------------------------------------------------------------------
with DAG(
    dag_id="yellow_taxi_parquet_ingestion",
    description="Monthly ingestion of NYC Yellow Taxi Parquet files to GCS and BigQuery",
    start_date=datetime(2021, 1, 1),
    end_date=datetime(2021, 12, 31),
    schedule="@monthly",
    catchup=True,
    max_active_runs=3,
    tags=["nyc-tlc", "parquet"],
) as dag:

    # ---------------------------------------------------------------
    # 1. Download Parquet dataset (idempotent)
    # ---------------------------------------------------------------
    @task
    def download_dataset(data_interval_start=None) -> str:
        year_month = data_interval_start.strftime("%Y-%m")
        filename = f"yellow_tripdata_{year_month}.parquet"
        local_path = AIRFLOW_HOME / filename

        if local_path.exists():
            return str(local_path)

        hook = HttpHook(method="GET", http_conn_id=BASE_URL_CONN_ID)
        response = hook.run(f"{BASE_PATH}/{filename}")
        local_path.write_bytes(response.content)
        return str(local_path)

    # ---------------------------------------------------------------
    # 2. Upload Parquet to GCS (idempotent)
    # ---------------------------------------------------------------
    @task
    def upload_to_gcs(local_parquet_path: str) -> str:
        filename = Path(local_parquet_path).name
        object_name = f"{GCS_PREFIX}/{filename}"

        client = storage.Client()
        bucket = client.bucket(BUCKET)
        blob = bucket.blob(object_name)

        if not blob.exists():
            blob.upload_from_filename(local_parquet_path)

        return f"gs://{BUCKET}/{object_name}"

    # ---------------------------------------------------------------
    # TASK DEPENDENCIES (XCom-based)
    # ---------------------------------------------------------------
    local_parquet = download_dataset()
    gcs_uri = upload_to_gcs(local_parquet)

    # ---------------------------------------------------------------
    # 3. Create / Update BigQuery External Table
    # ---------------------------------------------------------------
    create_external_table = BigQueryCreateTableOperator(
        task_id="create_bq_table",
        project_id=PROJECT_ID,
        dataset_id=BIGQUERY_DATASET,
        table_id="yellow_taxi_{{ data_interval_start.strftime('%Y_%m') }}",
        gcp_conn_id="google_cloud_default",
        table_resource={
            "type": "EXTERNAL",
            "externalDataConfiguration": {
                "sourceFormat": "PARQUET",
                "sourceUris": ["{{ task_instance.xcom_pull(task_ids='upload_to_gcs') }}"],
                "autodetect": True,
            },
        },
    )

    gcs_uri >> create_external_table
