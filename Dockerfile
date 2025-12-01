FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Crear directorios para datos
RUN mkdir -p /data /output

# Crear datos de prueba
RUN python scripts/create_test_data.py

# Ejecutar pruebas
RUN python -m pytest tests/ -v

CMD ["python", "-m", "app.main"]