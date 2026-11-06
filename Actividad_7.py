import pandas as pd

df = pd.read_csv("df_ventas.csv")
df.shape

print("Primeras filas del archivo:")
print(df.head())

print("Información general:")
print(df.info())

print(df.describe(include="all"))

print(df.isnull().sum())

df.dropna(subset=["ciudad"])

df["precio_unitario"].fillna("Desconocido")

df[df["fecha"].isnull()].head(26)

df.duplicated().sum()

df["precio_unitario"] = (
    df["precio_unitario"]
    .astype("string")
    .str.replace("$", "", regex=False)
    .str.replace(".", "", regex=False)
)

df.to_csv("datos.csv", index=False)
