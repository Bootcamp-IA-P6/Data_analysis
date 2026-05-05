# 🏠 Airbnb Data Analysis (Madrid & Milán)

Proyecto de análisis de datos de Airbnb enfocado en las ciudades de **Madrid** y **Milán**.  
El objetivo es extraer insights de negocio y visualizarlos mediante un dashboard interactivo con Streamlit.

---

## ⚙️ Setup del entorno (usando `uv`)

### 1. Crear entorno virtual

```bash
uv venv
```

### 2. Activar entorno

**Windows:**

```bash
.venv\Scripts\activate
```

**Mac/Linux:**

```bash
source .venv/bin/activate
```

---

### 3. Instalar dependencias

```bash
uv sync
```

> Las dependencias están definidas en `pyproject.toml` e incluyen: `pandas`, `numpy`, `plotly`, `streamlit`, `scikit-learn`, `statsmodels`, entre otras.

---

### 4. Ejecutar el dashboard

```bash
uv run streamlit run app.py
```

---

### 5. Ejecutar notebooks (EDA / limpieza)

```bash
uv run jupyter notebook
```

---

## 📁 Estructura del proyecto

```
app.py             # Dashboard principal (Streamlit)

data/
  ├── raw/         # datos originales (csv)
  └── processed/   # datos limpios (csv)

notebooks/         # análisis y limpieza de datos
  ├── cleaning_data.ipynb
  └── eda1.ipynb

src/               # funciones auxiliares
dashboard/         # assets adicionales del dashboard

pyproject.toml     # dependencias del proyecto
```

---

## 📊 Dataset

- **Madrid Airbnb** — listados de alojamientos en Madrid
- **Milán Airbnb** — listados de alojamientos en Milán

---

## 🎯 Objetivos

- ✅ Limpieza y preprocesamiento de datos
- ✅ Análisis exploratorio de datos (EDA)
- ✅ Visualización interactiva (Plotly + Streamlit)
- ✅ Segmentación con KMeans clustering
- ✅ Comparativa entre ciudades (Madrid vs. Milán)
- ✅ Dashboard con tema oscuro

---

## 🚀 Estado del proyecto

**Dashboard completado** — listo para revisión y despliegue.
