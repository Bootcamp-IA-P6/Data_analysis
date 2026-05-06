# Imagen base — Python 3.11 slim (ligera y estable)
FROM python:3.11-slim

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar primero el requirements para aprovechar la caché de Docker
COPY requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del proyecto
COPY . .

# Puerto que expone Streamlit
EXPOSE 8501

# Variables de entorno para que Streamlit funcione en contenedor
ENV STREAMLIT_SERVER_HEADLESS=true
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0

# Comando de arranque
CMD ["streamlit", "run", "app.py", "--server.headless=true", "--server.address=0.0.0.0", "--server.port=8501"]
