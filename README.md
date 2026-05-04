# 🏠 Airbnb Data Analysis (Madrid & Milan)

Proyecto de análisis de datos de Airbnb enfocado en las ciudades de Madrid y Milán.
El objetivo es extraer insights de negocio y visualizarlos mediante un dashboard.

---

## ⚙️ Setup del entorno (usando uv)

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
uv add pandas numpy matplotlib seaborn jupyter
```

---

### 4. Ejecutar notebook

```bash
uv run jupyter notebook
```

---

## 📁 Estructura del proyecto

```
data/
  ├── raw/         # datos originales (csv)
  └── processed/   # datos limpios

notebooks/         # análisis (EDA)
src/               # funciones auxiliares
dashboard/         # visualización (PowerBI / Streamlit)

pyproject.toml     # dependencias
```

---

## 📊 Dataset

* Madrid Airbnb
* Milan Airbnb

---

## 🎯 Objetivos

* Análisis exploratorio de datos (EDA)
* Limpieza y preprocesamiento
* Visualización de datos
* Generación de insights
* Creación de dashboard

---

## 🚀 Estado del proyecto

En desarrollo (EDA)
