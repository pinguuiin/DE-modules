import pandas as pd
from sqlalchemy import create_engine

engine = create_engine("postgresql://root:root@localhost:5432/ny_taxi")

df_zones = pd.read_csv("taxi_zone_lookup.csv")
df_zones.to_sql(name="zones", con=engine, if_exists="replace")