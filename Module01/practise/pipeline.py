import sys
import pandas as pd

print("arguments", sys.argv)

day = int(sys.argv[1])
print(f"Coding for {day} days now!")

df = pd.DataFrame({"A": [1, 2], "B": [3, 4]})
df["month"] = [10, 20]
print(df.head())

df.to_parquet(f"output_{day}.parquet")