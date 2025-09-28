import streamlit as st
import geopandas as gpd
import os

st.title("Análisis de Temperatura Mínima en Perú")

# Ruta al shapefile de distritos
shapefile_path = os.path.join("data", "CensoDistrito_2007.shp")

# Leer el shapefile
gdf_distritos = gpd.read_file(shapefile_path)

# Mostrar los primeros registros
st.subheader("Distritos cargados")
st.dataframe(gdf_distritos.head())

import pandas as pd
from unidecode import unidecode

# Función segura que evita errores con valores nulos
def limpiar(valor):
    if pd.isnull(valor):
        return ""
    return unidecode(str(valor).upper())

# Aplicar limpieza a cada columna
gdf_distritos["NOMDEPARTA"] = gdf_distritos["NOMDEPARTA"].apply(limpiar)
gdf_distritos["NOMPROVINC"] = gdf_distritos["NOMPROVINC"].apply(limpiar)
gdf_distritos["NOMDISTRIT"] = gdf_distritos["NOMDISTRIT"].apply(limpiar)

import rasterio
from rasterstats import zonal_stats
import numpy as np

# Ruta al raster
raster_path = os.path.join("data", "tmin_raster.tif")

# Calcular estadísticas zonales por distrito
stats = zonal_stats(
    gdf_distritos,
    raster_path,
    stats=["count", "mean", "min", "max", "std", "percentile_10", "percentile_90"],
    geojson_out=True,
    nodata=-9999
)

# Convertir resultados a GeoDataFrame
gdf_stats = gpd.GeoDataFrame.from_features(stats)

# Agregar una métrica personalizada: rango térmico
gdf_stats["rango_termico"] = gdf_stats["max"] - gdf_stats["min"]

# Mostrar tabla en Streamlit
st.subheader("Estadísticas zonales por distrito")
st.dataframe(gdf_stats[["NOMDISTRIT", "mean", "min", "max", "std", "percentile_10", "percentile_90", "rango_termico"]].head())
import matplotlib.pyplot as plt

st.subheader("Distribución de la temperatura mínima promedio por distrito")

fig, ax = plt.subplots()
gdf_stats["mean"].hist(bins=30, edgecolor="black", ax=ax)
ax.set_xlabel("Temperatura mínima promedio (°C)")
ax.set_ylabel("Número de distritos")
ax.set_title("Distribución de Tmin promedio")
st.pyplot(fig)
st.subheader("Top 15 distritos con mayor riesgo de heladas (Tmin más baja)")

ranking = gdf_stats[["NOMDISTRIT", "mean"]].sort_values(by="mean").head(15)
st.dataframe(ranking)
st.subheader("Mapa de temperatura mínima promedio por distrito")

fig, ax = plt.subplots(figsize=(10, 10))
gdf_stats.plot(column="mean", cmap="coolwarm", linewidth=0.8, ax=ax, edgecolor="0.8", legend=True)
ax.set_title("Temperatura mínima promedio por distrito")
ax.axis("off")
st.pyplot(fig)
st.download_button(
    label="Descargar tabla de estadísticas zonales",
    data=gdf_stats[["NOMDISTRIT", "mean", "min", "max", "std", "percentile_10", "percentile_90", "rango_termico"]].to_csv(index=False).encode("utf-8"),
    file_name="estadisticas_zonales.csv",
    mime="text/csv"
)
st.header("Diagnóstico climático")

st.markdown("""
Las estadísticas zonales muestran que varios distritos altoandinos presentan temperaturas mínimas promedio por debajo de los 5°C, lo que indica alto riesgo de heladas.  
Distritos como HUACLLAN, LA MERCED y SUCCHA están entre los más vulnerables.  
En la Amazonía, zonas como Loreto y Ucayali también enfrentan descensos bruscos de temperatura conocidos como *friaje*, afectando salud y productividad.

Este diagnóstico permite identificar territorios prioritarios para intervención pública.
""")
st.header("Propuestas de política pública")

st.markdown("""
### 1. Viviendas térmicas rurales (ISUR)
- **Objetivo:** Reducir infecciones respiratorias agudas (IRA) en zonas altoandinas.
- **Territorio:** Distritos con Tmin ≤ p10 (ej. HUACLLAN, ACZO, CHACCHO).
- **Intervención:** Aislamiento térmico en viviendas rurales.
- **Costo estimado:** S/ 4,000 por vivienda × 500 viviendas = S/ 2,000,000
- **KPI:** −30% casos IRA en ESSALUD/MINSA en zonas intervenidas.

### 2. Kits antiheladas para agricultores
- **Objetivo:** Reducir pérdidas agrícolas por heladas.
- **Territorio:** Distritos con Tmin ≤ p10 en Cusco, Ayacucho, Huancavelica.
- **Intervención:** Entrega de cobertores, sensores y capacitación.
- **Costo estimado:** S/ 500 por kit × 1,000 kits = S/ 500,000
- **KPI:** −25% pérdida de cultivos sensibles (papa, quinua).

### 3. Calendario agroclimático escolar
- **Objetivo:** Evitar ausentismo escolar por friaje en la Amazonía.
- **Territorio:** Loreto, Ucayali, Madre de Dios.
- **Intervención:** Ajuste de calendario escolar + entrega de ropa térmica.
- **Costo estimado:** S/ 200 por estudiante × 2,000 estudiantes = S/ 400,000
- **KPI:** +15% asistencia escolar en días de friaje.
""")
