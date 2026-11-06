
from pathlib import Path

import numpy as np
import pandas as pd

try:
    from IPython.display import display
except ImportError:
    display = print

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 200)

try:
    CARPETA = Path(__file__).resolve().parent
except NameError:
    CARPETA = Path.cwd()

RUTA_CSV = CARPETA / "animal_data_dirty1-selected-columns.csv"
RUTA_SALIDA = CARPETA / "animal_data_clean.csv"

print("Pandas:", pd.__version__)
print("NumPy:", np.__version__)

df_raw = pd.read_csv(RUTA_CSV)

print(f"Filas: {df_raw.shape[0]} | Columnas: {df_raw.shape[1]}")

print("\nColumnas y tipos de dato:")
display(df_raw.dtypes.to_frame("tipo"))

print("\nValores faltantes por columna:")
faltantes = pd.DataFrame({
    "faltantes": df_raw.isna().sum(),
    "porcentaje": df_raw.isna().mean().mul(100).round(1),
})
display(faltantes)

print("\nRegistros duplicados:", df_raw.duplicated().sum())

for col in ["Animal type", "Country", "Gender"]:
    print(f"\n--- value_counts de '{col}' ---")
    display(df_raw[col].value_counts(dropna=False))

print("\n--- Nombres de animales (top 10) ---")
display(df_raw["Animal name"].value_counts(dropna=False).head(10))

es_formato_punto = df_raw["Observation date"].str.match(r"^\d{2}\.\d{2}\.\d{4}$")
print("\nFechas con formato dd.mm.aaaa:", es_formato_punto.sum())
print("Fechas con otro formato:", (~es_formato_punto).sum())
display(df_raw.loc[~es_formato_punto, "Observation date"].value_counts())

print("\nResumen numérico:")
display(df_raw[["Weight kg", "Body Length cm", "Latitude", "Longitude"]].describe().T)
print("Pesos negativos:", (df_raw["Weight kg"] < 0).sum())
print("Longitudes negativas:", (df_raw["Body Length cm"] < 0).sum())

filas_vacias = df_raw.drop(columns="Observation date").isna().all(axis=1)
print("Filas completamente vacías (salvo la fecha):", filas_vacias.sum())

print("\nCoordenadas fuera de rango razonable para Europa Central:")
display(
    df_raw.loc[
        (df_raw["Latitude"] < 40) | (df_raw["Longitude"] > 30),
        ["Animal type", "Country", "Latitude", "Longitude"],
    ]
)

print("\nPeso de lynx > 40 kg:")
display(df_raw.loc[(df_raw["Animal type"].str.contains("lynx", na=False)) & (df_raw["Weight kg"] > 40),
                   ["Animal type", "Country", "Weight kg", "Body Length cm"]])
print("Longitud de hedgehog > 40 cm:")
display(df_raw.loc[(df_raw["Animal type"].str.contains("ledgehod|hedgehog|wedgehod", na=False)) & (df_raw["Body Length cm"] > 40),
                   ["Animal type", "Country", "Weight kg", "Body Length cm"]])

df = df_raw.copy()

df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
print("Columnas:", list(df.columns))

filas_vacias = df.drop(columns="observation_date").isna().all(axis=1)
print("Filas vacías eliminadas:", filas_vacias.sum())
df = df.loc[~filas_vacias].copy()

print("Valores no nulos en animal_code:", df["animal_code"].notna().sum())
df = df.drop(columns="animal_code")

def limpiar_texto(serie):
    """Quita espacios, pasa a minúscula y elimina símbolos raros ('?' y '™')."""
    return (
        serie.astype("string")
        .str.strip()
        .str.lower()
        .str.replace(r"[?™]", "", regex=True)
        .str.strip()
    )

errores_tipo = {
    "european bisson": "european bison",
    "european buster": "european bison",
    "red squirel": "red squirrel",
    "red squirrell": "red squirrel",
    "ledgehod": "hedgehog",
    "wedgehod": "hedgehog",
}
df["animal_type"] = (
    limpiar_texto(df["animal_type"]).replace(errores_tipo).str.title()
)

df["animal_type"] = df["animal_type"].fillna("Unknown")

equivalencias_pais = {
    "pl": "poland",
    "hu": "hungary",
    "hungry": "hungary",
    "cz": "czech republic",
    "czech": "czech republic",
    "cc": "czech republic",
    "de": "germany",
    "australia": "austria",
}
df["country"] = limpiar_texto(df["country"]).replace(equivalencias_pais).str.title()

df["gender"] = (
    limpiar_texto(df["gender"]).replace({"not determined": "unknown"}).str.title()
)
df["gender"] = df["gender"].fillna("Unknown")

for col in ["animal_type", "country", "gender"]:
    print(f"\n{col}:")
    print(df[col].value_counts(dropna=False).to_string())

fecha_a = pd.to_datetime(df["observation_date"], format="%d.%m.%Y", errors="coerce")
fecha_b = pd.to_datetime(df["observation_date"], format="%d %B %Y", errors="coerce")
df["observation_date"] = fecha_a.fillna(fecha_b)

print("Fechas que no se pudieron interpretar:", df["observation_date"].isna().sum())
print("Rango de fechas:", df["observation_date"].min().date(), "->", df["observation_date"].max().date())

for col in ["weight_kg", "body_length_cm"]:
    print(f"{col}: {(df[col] < 0).sum()} valores negativos corregidos")
    df[col] = df[col].abs()
LIMITES_PAIS = {
    "Austria": (46.3, 49.1, 9.5, 17.2),
    "Czech Republic": (48.5, 51.1, 12.0, 18.9),
    "Germany": (47.2, 55.1, 5.8, 15.1),
    "Hungary": (45.7, 48.6, 16.1, 22.9),
    "Poland": (49.0, 55.0, 14.1, 24.2),
    "Slovakia": (47.7, 49.7, 16.8, 22.6),
}
coords_invalidas = 0
for pais, (lat0, lat1, lon0, lon1) in LIMITES_PAIS.items():
    es_pais = df["country"].eq(pais)
    tiene_coords = df["latitude"].notna() & df["longitude"].notna()
    dentro = df["latitude"].between(lat0, lat1) & df["longitude"].between(lon0, lon1)
    mal = es_pais & tiene_coords & ~dentro
    coords_invalidas += mal.sum()
    df.loc[mal, ["latitude", "longitude"]] = np.nan
print("Coordenadas imposibles puestas en NaN:", coords_invalidas)

print("Duplicados antes:", df.duplicated().sum())
df = df.drop_duplicates().reset_index(drop=True)
print("Duplicados después:", df.duplicated().sum())
print("Filas restantes:", len(df))

def es_outlier_iqr(datos, col, k=3.0):
    q1 = datos.groupby("animal_type")[col].transform(lambda s: s.quantile(0.25))
    q3 = datos.groupby("animal_type")[col].transform(lambda s: s.quantile(0.75))
    iqr = q3 - q1
    return (datos[col] < q1 - k * iqr) | (datos[col] > q3 + k * iqr)

for col in ["weight_kg", "body_length_cm"]:
    outliers = es_outlier_iqr(df, col)
    print(f"\n{col}: {outliers.sum()} outliers extremos")
    display(df.loc[outliers, ["animal_type", "country", "weight_kg", "body_length_cm"]])
    df.loc[outliers, col] = np.nan 

print("Faltantes antes de imputar:")
print(df.isna().sum().to_string())

for col in ["weight_kg", "body_length_cm"]:
    mediana_especie = df.groupby("animal_type")[col].transform("median")
    df[col] = df[col].fillna(mediana_especie)

df["animal_name"] = df["animal_name"].fillna("Unnamed")

df["body_length_cm"] = df["body_length_cm"].round().astype("int64")
df["weight_kg"] = df["weight_kg"].astype("float64")
for col in ["animal_type", "country", "gender"]:
    df[col] = df[col].astype("category")
df["animal_name"] = df["animal_name"].astype("string")
df = df.reset_index(drop=True)

df.info()

print("=== ANTES vs DESPUÉS ===")
comparacion = pd.DataFrame(
    {
        "antes": [
            df_raw.shape[0],
            df_raw.shape[1],
            int(df_raw.isna().sum().sum()),
            int(df_raw.duplicated().sum()),
            df_raw["Animal type"].nunique(dropna=False),
            df_raw["Country"].nunique(dropna=False),
            df_raw["Gender"].nunique(dropna=False),
            int((df_raw["Weight kg"] < 0).sum() + (df_raw["Body Length cm"] < 0).sum()),
        ],
        "después": [
            df.shape[0],
            df.shape[1],
            int(df.isna().sum().sum()),
            int(df.duplicated().sum()),
            df["animal_type"].nunique(),
            df["country"].nunique(),
            df["gender"].nunique(),
            int((df["weight_kg"] < 0).sum() + (df["body_length_cm"] < 0).sum()),
        ],
    },
    index=[
        "filas", "columnas", "celdas vacías (total)", "duplicados",
        "categorías animal_type", "categorías country", "categorías gender",
        "valores negativos",
    ],
)
display(comparacion)

print("\nFaltantes por columna (solo quedan lat/lon, a propósito):")
print(df.isna().sum().to_string())

print("\nCategorías finales:")
for col in ["animal_type", "country", "gender"]:
    print(f"\n{col}:")
    print(df[col].value_counts().to_string())

assert df.duplicated().sum() == 0, "Quedan duplicados"
assert df["observation_date"].notna().all(), "Hay fechas sin interpretar"
assert (df["weight_kg"] > 0).all() and (df["body_length_cm"] > 0).all(), "Hay valores <= 0"
assert df[["weight_kg", "body_length_cm", "animal_type", "country", "gender"]].notna().all().all()
assert df["animal_type"].nunique() == 5 and df["country"].nunique() == 6
assert df["latitude"].dropna().between(46, 56).all(), "Latitud fuera de Europa Central"
assert df["longitude"].dropna().between(10, 25).all(), "Longitud fuera de Europa Central"
print("\n✔ Todas las verificaciones pasaron.")

display(df.head(10))

mediana_peso_especie = df.groupby("animal_type", observed=True)["weight_kg"].transform("median")
df["weight_status"] = np.where(
    df["weight_kg"] > mediana_peso_especie, "Above species median", "At/below species median"
)

df["has_gps"] = np.where(df["latitude"].notna() & df["longitude"].notna(), 1, 0)

print(df["weight_status"].value_counts().to_string())
print("\nObservaciones con GPS:", df["has_gps"].sum(), "de", len(df))
display(df[["animal_type", "weight_kg", "weight_status", "has_gps"]].head(8))

pesos_crudos = df_raw["Weight kg"].to_numpy()
print("\nSobre los datos CRUDOS (con NaN):")
print("  np.mean    :", np.mean(pesos_crudos))
print("  np.nanmean :", round(np.nanmean(pesos_crudos), 2), "(ignora los NaN)")

pesos_ardilla = df.loc[df["animal_type"] == "Red Squirrel", "weight_kg"].to_numpy()
media = np.mean(pesos_ardilla)
mediana = np.median(pesos_ardilla)
desv = np.std(pesos_ardilla)
print("\nPeso de la ardilla roja (kg):")
print(f"  media   = {media:.3f}")
print(f"  mediana = {mediana:.3f}")
print(f"  desv.   = {desv:.3f}")

cv = (
    df.groupby("animal_type", observed=True)["weight_kg"]
    .apply(lambda s: np.std(s.to_numpy()) / np.mean(s.to_numpy()) * 100)
    .round(1)
    .sort_values(ascending=False)
    .rename("coef_variacion_%")
)
print("\nCoeficiente de variación del peso por especie (%):")
display(cv)

obs_tipo = df.groupby("animal_type", observed=True).size().sort_values(ascending=False)
print("4.1 Observaciones por tipo de animal")
display(obs_tipo.to_frame("observaciones"))

prom_tipo = (
    df.groupby("animal_type", observed=True)[["weight_kg", "body_length_cm"]]
    .mean()
    .round(2)
    .sort_values("weight_kg", ascending=False)
)
print("\n4.2 Promedio de peso y longitud por tipo de animal")
display(prom_tipo)

prom_pais = df.groupby("country", observed=True)["weight_kg"].mean().round(2).sort_values(ascending=False)
print("\n4.3 Peso promedio por país (todas las especies)")
display(prom_pais.to_frame("peso_promedio_kg"))

ardillas = df[df["animal_type"] == "Red Squirrel"]
prom_pais_ardilla = (
    ardillas.groupby("country", observed=True)["weight_kg"]
    .agg(observaciones="count", peso_promedio_kg="mean")
    .round(3)
    .sort_values("peso_promedio_kg", ascending=False)
)
print("\n4.3b Peso promedio de la ARDILLA ROJA por país")
display(prom_pais_ardilla)

obs_pais = df.groupby("country", observed=True).agg(
    observaciones=("animal_type", "size"),
    con_gps=("has_gps", "sum"),
)
obs_pais["pct_con_gps"] = (obs_pais["con_gps"] / obs_pais["observaciones"] * 100).round(1)
print("\n4.4 Observaciones por país y cobertura GPS")
display(obs_pais.sort_values("observaciones", ascending=False))

sexo_tipo = df.groupby(["animal_type", "gender"], observed=True).size().unstack(fill_value=0)
print("\n4.5 Sexo por tipo de animal")
display(sexo_tipo)

obs_mes = df.groupby(df["observation_date"].dt.to_period("M")).size()
print("\n4.6 Observaciones por mes")
display(obs_mes.to_frame("observaciones"))

df.to_csv(RUTA_SALIDA, index=False)
print("Archivo limpio guardado en:", RUTA_SALIDA)