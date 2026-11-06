import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.DataFrame({
    "Mes": ["Ene", "Feb", "Mar", "Abr", "May", "Jun"],
    "Ventas": [120, 150, 135, 180, 210, 195],
    "Categoria": ["A", "B", "A", "C", "B", "C"],
    "Unidades": [20, 35, 25, 40, 30, 45]
})

# 2. Dimensiones de la figura
plt.figure(figsize=(9, 5))

# 3. Trazo del gráfico de líneas y personalización
plt.plot(
    df["Mes"],
    df["Ventas"],
    color="#2b5c8f",  # Color de la línea
    linestyle="--",  # Estilo discontinuo
    linewidth=2.5,  # Grosor de la línea
    marker="o",  # Forma del marcador (círculo)
    markersize=8,  # Tamaño del marcador
    markerfacecolor="#0a093b",  # Relleno del marcador
    markeredgecolor="#3e91ea",  # Borde del marcador
    markeredgewidth=1.5,
    label="Ventas mensuales",
)

# 4. Título y nombres de ejes
plt.title("Evolución de Ventas por Mes", fontsize=14, fontweight="bold", pad=15)
plt.xlabel("Mes", fontsize=11, labelpad=10)
plt.ylabel("Ventas", fontsize=11, labelpad=10)

# 5. Cuadrícula y leyenda
plt.grid(True, linestyle=":", alpha=0.6)
plt.legend(loc="upper left")

# Visualización
plt.tight_layout()
plt.show()

# 2. Cambio de estilo visual general
sns.set_theme(style="ticks", font_scale=1.05)

plt.figure(figsize=(8, 5))

# 3. Gráfico de barras con paleta personalizada y agregación por suma
ax = sns.barplot(
    data=df,
    x="Categoria",
    y="Unidades",
    estimator=sum,  # Calcula la suma total acumulada por categoría
    errorbar=None,  # Omite barras de dispersión para un gráfico categóric
    palette="crest",  # Paleta continua/secuencial accesible y de fácil lectura
)

# 4. Inclusión de valores sobre las barras para facilitar la lectura inmediata
ax.bar_label(ax.containers[0], padding=3, fontsize=11, fontweight="bold")

# 5. Eliminación de bordes sobrantes (reduce ruido visual)
sns.despine(top=True, right=True)

# 6. Personalización de título y etiquetas de ejes
plt.title(
    "Total de Unidades Vendidas por Categoría",
    fontsize=14,
    fontweight="bold",
    pad=15,
)
plt.xlabel("Categoría de Producto", fontsize=11, labelpad=10)
plt.ylabel("Unidades Totales", fontsize=11, labelpad=10)

plt.tight_layout()
plt.show()

variables_numericas = df[["Ventas", "Unidades"]]

# Calcular la matriz de correlación
matriz_correlacion = variables_numericas.corr()

fig, ax = plt.subplots(figsize=(7, 5.5))

sns.heatmap(
    matriz_correlacion,
    annot=True,                  # Mostrar los valores
    fmt=".2f",                   # Dos decimales
    cmap="vlag",                 # Paleta divergente
    vmin=-1,
    vmax=1,
    center=0,
    square=True,
    linewidths=1,
    linecolor="white",
    cbar_kws={"label": "Coeficiente de correlación"},
    ax=ax
)

ax.set_title(
    "Mapa de calor: correlación entre variables",
    fontsize=15,
    fontweight="bold",
    pad=15
)
ax.set_xlabel("Variables")
ax.set_ylabel("Variables")

plt.tight_layout()
plt.show()

print("Unidades totales por categoría:")
print(unidades_categoria)

print("\nMatriz de correlación:")
print(matriz_correlacion.round(2))