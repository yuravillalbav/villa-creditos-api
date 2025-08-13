"""
Villa Créditos API - Sistema de gestión de préstamos personales
"""
from dotenv import load_dotenv
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from models import models
from database.connection import engine
from routers import routers as loan_routers

load_dotenv()

# Configuración básica
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
API_VERSION = "1.0.0"


def init_db():
    """Inicializar base de datos"""
    try:
        models.Base.metadata.create_all(bind=engine)
        print("✅ Base de datos inicializada correctamente")
    except Exception as e:
        print(f"❌ Error inicializando base de datos: {e}")


# Inicializar base de datos
init_db()

# Configuración de la aplicación FastAPI
app = FastAPI(
    title="Villa Créditos API",
    description="""
    🏦 API para la gestión de préstamos personales.

    Esta API permite:
    * Crear solicitudes de préstamo
    * Consultar préstamos existentes
    * Actualizar información de préstamos
    * Eliminar préstamos existentes
   
    """,
    version=API_VERSION,
    contact={
        "name": "Villa Créditos",
        "email": "villacreditos@outlook.com",
    },
    license_info={
        "name": "MIT",
    },
)

# Configuración de CORS básica
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*"] if ENVIRONMENT == "development" else ["https://villacreditos.com"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PATCH", "DELETE"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(loan_routers.router)

# Endpoint básico de salud


@app.get("/", tags=["General"])
def root():
    """Endpoint raíz con información básica de la API"""
    return {
        "message": "🏦 Villa Créditos API",
        "version": API_VERSION,
        "status": "active",
        "docs": "/docs",
        "environment": ENVIRONMENT
    }
