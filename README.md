# 🏠 Airbnb Data Analysis — Madrid vs. Milán

Análisis comparativo del mercado de alquiler a corto plazo en **Madrid** y **Milán** a partir de datos públicos de [Inside Airbnb](http://insideairbnb.com/). El proyecto abarca desde la limpieza de datos hasta un dashboard interactivo con clustering mediante KMeans.

---

## 📋 Índice de contenido

1. [Descripción del proyecto](#-descripción-del-proyecto)
2. [Tecnologías utilizadas](#-tecnologías-utilizadas)
3. [Estructura del proyecto](#-estructura-del-proyecto)
4. [Instalación y despliegue](#-instalación-y-despliegue)
   - [Requisitos previos](#requisitos-previos)
   - [Clonar el repositorio](#1-clonar-el-repositorio)
   - [Crear y activar el entorno virtual](#2-crear-y-activar-el-entorno-virtual)
   - [Instalar dependencias](#3-instalar-dependencias)
   - [Ejecutar el dashboard](#4-ejecutar-el-dashboard)
   - [Ejecutar los notebooks](#5-ejecutar-los-notebooks)
5. [Dataset](#-dataset)
6. [Secciones del dashboard](#-secciones-del-dashboard)
7. [Flujo de trabajo](#-flujo-de-trabajo)
8. [Estado del proyecto](#-estado-del-proyecto)
9. [Equipo](#-equipo)

---

## 📌 Descripción del proyecto

El objetivo principal es extraer **insights de negocio** comparando los mercados de Airbnb de Madrid y Milán:

- ¿Qué ciudad tiene precios más altos y por qué?
- ¿Qué barrios concentran los alojamientos más caros?
- ¿Qué tipos de alojamiento predominan en cada ciudad?
- ¿Es posible segmentar los anuncios en grupos significativos mediante clustering?

El resultado final es un **dashboard web interactivo** con tema oscuro, construido con Streamlit, que permite explorar estas preguntas de forma visual y dinámica.

---

## 🛠 Tecnologías utilizadas

### Lenguaje
| Tecnología | Versión |
|---|---|
| Python | 3.14 |

### Gestión del entorno
| Herramienta | Uso |
|---|---|
| [`uv`](https://github.com/astral-sh/uv) | Gestor de entornos y dependencias (reemplaza pip + venv) |

### Librerías principales
| Librería | Versión mínima | Uso |
|---|---|---|
| `streamlit` | 1.57.0 | Framework del dashboard web |
| `pandas` | 3.0.2 | Manipulación y análisis de datos |
| `numpy` | 2.4.4 | Operaciones numéricas |
| `plotly` | 6.7.0 | Gráficos interactivos |
| `matplotlib` | 3.10.9 | Visualizaciones estáticas (heatmaps) |
| `seaborn` | 0.13.2 | Visualizaciones estadísticas (pairplot) |
| `scikit-learn` | 1.8.0 | KMeans clustering, PCA, métricas |
| `statsmodels` | 0.14.6 | Líneas de tendencia OLS en scatter plots |
| `jupyter` | 1.1.1 | Entorno de notebooks para EDA y limpieza |

---

## 📁 Estructura del proyecto

```
Data_analysis/
│
├── app.py                    # 🚀 Dashboard principal (Streamlit)
├── main.py                   # Punto de entrada auxiliar
├── pyproject.toml            # Configuración del proyecto y dependencias
├── uv.lock                   # Lockfile de dependencias (reproducibilidad)
├── .python-version           # Versión de Python fijada (3.14)
│
├── data/
│   ├── raw/
│   │   ├── madrid_airbnb.csv     # Datos originales Madrid
│   │   └── milan_airbnb.csv      # Datos originales Milán
│   └── processed/
│       ├── airbnb_clean.csv      # Dataset combinado y limpio (entrada del dashboard)
│       ├── madrid_clean.csv      # Dataset limpio solo Madrid
│       └── milan_clean.csv       # Dataset limpio solo Milán
│
├── notebooks/
│   ├── cleaning_data.ipynb   # Limpieza y preprocesamiento de datos
│   └── eda1.ipynb            # Análisis exploratorio de datos (EDA)
│
├── src/
│   └── utils.py              # Funciones auxiliares reutilizables
│
└── dashboard/                # Assets adicionales del dashboard
```

---

## 🚀 Instalación y despliegue

### Requisitos previos

- **Python 3.14** instalado en el sistema
- **`uv`** instalado globalmente:

```bash
# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# Mac / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
```

> ⚠️ Este proyecto usa `uv` como gestor de entornos. **No uses `pip` ni `conda` directamente**, ya que las dependencias están fijadas en `uv.lock` para garantizar reproducibilidad.

---

### 1. Clonar el repositorio

```bash
git clone https://github.com/Bootcamp-IA-P6/Data_analysis.git
cd Data_analysis
```

---

### 2. Crear y activar el entorno virtual

```bash
uv venv
```

**Windows (cmd / PowerShell):**
```bash
.venv\Scripts\activate
```

**Mac / Linux:**
```bash
source .venv/bin/activate
```

---

### 3. Instalar dependencias

```bash
uv sync
```

> Este comando instala **exactamente** las versiones especificadas en `uv.lock`. No modifica ninguna dependencia.

---

### 4. Ejecutar el dashboard

Asegúrate de que el entorno virtual esté activo y ejecuta:

```bash
uv run streamlit run app.py
```

El dashboard se abrirá automáticamente en el navegador en `http://localhost:8501`.

> 💡 Si el puerto 8501 está ocupado, Streamlit usará el siguiente disponible. Comprueba la URL en la terminal.

---

### 5. Ejecutar los notebooks

```bash
uv run jupyter notebook
```

Se abrirá Jupyter en el navegador. Los notebooks están en la carpeta `notebooks/`:

- `cleaning_data.ipynb` → ejecutar primero (genera los CSV en `data/processed/`)
- `eda1.ipynb` → análisis exploratorio

> ⚠️ Es necesario haber ejecutado `cleaning_data.ipynb` antes de lanzar el dashboard, ya que este necesita el archivo `data/processed/airbnb_clean.csv`.

---

## 📊 Dataset

| Atributo | Detalle |
|---|---|
| **Fuente** | [Inside Airbnb](http://insideairbnb.com/) |
| **Ciudades** | Madrid 🇪🇸 y Milán 🇮🇹 |
| **Período** | 2025–2026 |
| **Formato** | CSV |
| **Variables clave** | `price`, `minimum_nights`, `number_of_reviews`, `reviews_per_month`, `calculated_host_listings_count`, `availability_365`, `room_type`, `neighbourhood`, `ciudad` |

Los datos crudos se almacenan en `data/raw/` y los datos procesados en `data/processed/`. El fichero `airbnb_clean.csv` combina ambas ciudades con una columna `ciudad` que permite filtrar.

---

## 🖥 Secciones del dashboard

El dashboard está dividido en **5 secciones** navegables desde el panel lateral:

| Sección | Contenido |
|---|---|
| **1. Resumen general** | KPIs clave, calidad de datos, distribución de precios y tipos de alojamiento |
| **2. Análisis de variables** | Correlaciones con el precio, explorador de distribuciones (histograma / boxplot / violín), scatter interactivo con línea de tendencia OLS, top barrios más caros |
| **3. Visualizaciones avanzadas** | Heatmap de correlaciones, pairplot entre variables, scatter 3D interactivo |
| **4. Clustering (KMeans)** | Selección de variables, método del codo, coeficiente Silhouette, ejecución del modelo |
| **5. Resultados del clustering** | Métricas del modelo, perfil de clusters, visualización PCA 2D/3D, distribución por ciudad, boxplots y heatmap de centroides |

---

## 🔄 Flujo de trabajo

```
Datos brutos (raw/)
      │
      ▼
cleaning_data.ipynb     ← Limpieza, normalización, merge de ciudades
      │
      ▼
data/processed/airbnb_clean.csv
      │
      ▼
eda1.ipynb              ← Análisis exploratorio, primeras visualizaciones
      │
      ▼
app.py (Streamlit)      ← Dashboard interactivo con clustering KMeans
```

---

## 📈 Estado del proyecto

| Fase | Estado |
|---|---|
| Limpieza de datos | ✅ Completado |
| Análisis exploratorio (EDA) | ✅ Completado |
| Dashboard Streamlit | ✅ Completado |
| Clustering KMeans | ✅ Completado |
| Despliegue en producción | 🔲 Pendiente |

---

## 👥 Equipo

Proyecto desarrollado en el marco del **Bootcamp IA — Promoción 6**.

| Nombre | Rol | GitHub |
|---|---|---|
| * Arianna Gabriela Hernandez* | Data Analyst / Dashboard | [@gabriela_her](https://github.com/Bootcamp-IA-P6) |
| * Paloma * | Data Cleaning / EDA | [@pal-cloud](https://github.com/Bootcamp-IA-P6) |


---

<div align="center">
  <sub>Fuente de datos: <a href="http://insideairbnb.com/">Inside Airbnb</a> · 2025–2026</sub>
</div>
