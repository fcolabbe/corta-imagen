# Configuración de Docker para producción

FROM python:3.9-slim

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

# Crear directorio de trabajo
WORKDIR /app

# Copiar archivos de dependencias
COPY requirements.txt .

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código de la aplicación
COPY . .

# Crear directorios necesarios
RUN mkdir -p /app/outputs /app/logs

# Crear usuario no-root
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Exponer puerto
EXPOSE 8088

# Variables de entorno
ENV HOST=0.0.0.0
ENV PORT=8088
ENV WORKERS=4

# Comando de inicio
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8088", "--workers", "4"]
