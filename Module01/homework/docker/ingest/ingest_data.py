import pandas as pd
from sqlalchemy import create_engine

def ingest_data(url: str, engine, target_table: str, chunksize: int
) -> None:
    # Read the entire parquet file
    df = pd.read_parquet(url)
    
    # Upload in chunks using to_sql
    print(f"Total rows: {len(df)}")
    df.to_sql(
        name=target_table,
        con=engine,
        if_exists="replace",
        index=False,
        chunksize=chunksize,
        method="multi"
    )

def main():
    # PostgreSQL connection parameters
    pg_user = 'root'
    pg_pass = 'root'
    pg_host = 'pgdb'
    pg_port = '5432'
    pg_db = 'ny_taxi'
    
    # Data ingestion parameters
    year = 2025
    month = 11
    chunksize = 100000
    target_table = 'green_taxi_data'
    
    engine = create_engine(f'postgresql://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}')

    url = f'/data/green_tripdata_{year:04d}-{month:02d}.parquet'

    print(f'Ingesting data to {target_table} for {year}-{month}...')
    ingest_data(
        url=url,
        engine=engine,
        target_table=target_table,
        chunksize=chunksize
    )
    print('Green taxi data ingestion completed!')

    df_zones = pd.read_csv("/data/taxi_zone_lookup.csv")
    df_zones.to_sql(name="zones", con=engine, if_exists="replace", index=False)
    print('Taxi zones data ingestion completed!')

if __name__ == '__main__':
    main()
