import pandas as pd

df = pd.read_csv("한국도로공사_교통사고통계_20241231.csv", encoding="cp949")
print(df.head(10))
