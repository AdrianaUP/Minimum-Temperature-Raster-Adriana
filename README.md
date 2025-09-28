# Minimum Temperature Raster Analysis – Perú

Este proyecto analiza datos de temperatura mínima en Perú usando raster GeoTIFF y propone políticas públicas basadas en evidencia. Incluye una app en Streamlit para visualizar estadísticas zonales y mapas.

## Estructura
- `/app/`: Aplicación Streamlit.
- `/data/`: Raster y shapefiles.
- `requirements.txt`: Dependencias.


## 📦 Dataset

- Raster: Tmin Perú GeoTIFF (año 2020, Band 1)
- Vector: Shapefile de distritos peruanos
- Fuente: Google Drive compartido por el curso

## 🧪 Análisis realizado

- Limpieza de nombres y UBIGEO
- Cálculo de estadísticas zonales: mean, min, max, std, p10, p90, rango térmico
- Visualizaciones: histograma, ranking de distritos más fríos, mapa choropleth
- Descarga de tabla CSV

## 🏛️ Propuestas de política pública

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

## 🚀 Cómo ejecutar la app localmente

1. Clona el repositorio:
   ```bash
   git clone https://github.com/AdrianaUP/Minimum-Temperature-Raster-Adriana.git

# Activar entorno virtual
.\.venv\Scripts\activate

# instala las dependencias
pip install -r requirements.txt

# ejecuta la app
streamlit run app/streamlit_app.py
