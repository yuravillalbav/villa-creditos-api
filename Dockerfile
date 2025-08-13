# ============================================================================
# VILLA CRÉDITOS API - DOCKERFILE
# ============================================================================

# Imagen base optimizada con Python
FROM python:3.12-slim

# Información del mantenedor
LABEL maintainer="Villa Créditos <villacreditos@outlook.com>"
LABEL description="API para gestión de préstamos personales"
LABEL version="1.0.0"

# Establecer directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements 
COPY requirements.txt .

# Instalar dependencias de Python
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copiar el código de la aplicación
COPY . .

# Exponer el puerto
EXPOSE 8000

# Comando para correr la aplicación
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]