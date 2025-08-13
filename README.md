# 🏦 Villa Créditos API

Una API REST moderna para la gestión de préstamos personales, construida con FastAPI, SQLAlchemy y SQLite.

## 📋 Tabla de Contenidos

- [Características](#-características)
- [Tecnologías](#-tecnologías)
- [Instalación](#-instalación)
- [Uso](#-uso)
- [Endpoints](#-endpoints)
- [Modelos de Datos](#-modelos-de-datos)
- [Validaciones](#-validaciones)
- [Contribuir](#-contribuir)
- [Licencia](#-licencia)
- [Autores](#-autores)
- [Roadmap](#-roadmap)
- [Agradecimientos](#-agradecimientos)

## ✨ Características

- 🚀 **API REST completa** con FastAPI
- 📊 **Gestión de préstamos** con estados y seguimiento
- 🔍 **Validaciones robustas** para datos colombianos
- 📈 **Esquemas extensibles** para futuras funcionalidades
- 🗄️ **Base de datos SQLite** con migraciones automáticas
- 📚 **Documentación automática** con Swagger/OpenAPI
- 🐳 **Soporte Docker** para despliegue fácil
- 🔒 **Validación de datos** con Pydantic
- 📝 **Auditoría** y historial de cambios

## 🛠 Tecnologías

- **FastAPI** - Framework web moderno y rápido
- **SQLAlchemy** - ORM para Python
- **Pydantic** - Validación de datos
- **SQLite** - Base de datos ligera
- **Uvicorn** - Servidor ASGI
- **Python 3.12+** - Lenguaje de programación

## 🚀 Instalación

### Prerrequisitos

- Docker
- Git

### 🐳 Instalación con Docker (Recomendado)

1. **Clonar el repositorio**
   ```bash
   git clone git@github.com:yuravillalbav/villa-creditos-api.git
   cd api_villacreditos
   ```

2. **Construir la imagen Docker**
   ```bash
   docker build -t villa-creditos-api .
   ```

3. **Ejecutar el contenedor (básico)**
   ```bash
   docker run -p 8000:8000 villa-creditos-api
   ```

4. **Acceder a la API**
   - API: http://127.0.0.1:8000
   - Documentación: http://127.0.0.1:8000/docs
   - Redoc: http://127.0.0.1:8000/redoc


## 📖 Uso

### Crear un préstamo

```bash
curl -X POST "http://127.0.0.1:8000/loans/" \
     -H "Content-Type: application/json" \
     -d '{
       "user": "Juan Pérez",
       "email": "juan@example.com",
       "phone": "3001234567",
       "address": "Calle 123 #45-67, Bogotá",
       "amount": 1000000.0,
       "term_months": 12,
       "purpose": "personal",
       "monthly_income": 2500000.0,
       "employment_type": "empleado"
     }'
```

### Obtener todos los préstamos

```bash
curl -X GET "http://127.0.0.1:8000/loans/"
```

### Obtener un préstamo por ID

```bash
curl -X GET "http://127.0.0.1:8000/loans/1"
```

### Actualizar un préstamo

```bash
curl -X PATCH "http://127.0.0.1:8000/loans/1" \
     -H "Content-Type: application/json" \
     -d '{
       "status": "approved",
       "notes": "Préstamo aprobado"
     }'
```

### Eliminar un préstamo

```bash
curl -X DELETE "http://127.0.0.1:8000/loans/1"
```

## 🔗 Endpoints

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `GET` | `/loans/` | Obtener todos los préstamos | 
| `GET` | `/loans/{id}` | Obtener un préstamo por ID |
| `POST` | `/loans/` | Crear un nuevo préstamo |
| `PATCH` | `/loans/{id}` | Actualizar un préstamo |
| `DELETE` | `/loans/{id}` | Eliminar un préstamo |
| `GET` | `/docs` | Documentación Swagger |
| `GET` | `/redoc` | Documentación ReDoc |

## 📊 Modelos de Datos

### LoanRequest (Préstamo)

```python
{
  "id": 1,
  "user": "Juan Pérez",
  "email": "juan@example.com",
  "phone": "3001234567",
  "address": "Calle 123 #45-67, Bogotá",
  "amount": 1000000.0,
  "term_months": 12,
  "purpose": "personal",
  "monthly_income": 2500000.0,
  "employment_type": "empleado",
  "status": "pending",
  "notes": null,
  "created_at": "2025-08-04T12:00:00",
  "updated_at": "2025-08-04T12:00:00"
}
```

### Estados de Préstamo

- `pending` - Pendiente de revisión
- `approved` - Aprobado
- `rejected` - Rechazado
- `disbursed` - Desembolsado
- `completed` - Completado
- `defaulted` - En mora

### Propósitos de Préstamo

- `personal` - Personal
- `business` - Negocio
- `education` - Educación
- `medical` - Médico
- `other` - Otro

## ✅ Validaciones

### Teléfono
- Formato colombiano: `3001234567` o `+573001234567`
- Longitud: 7-15 caracteres

### Nombre
- Solo letras y espacios
- Incluye caracteres especiales (á, é, í, ó, ú, ñ)
- Longitud: 2-100 caracteres

### Monto
- Valor positivo
- Minimo: $100.000 COP
- Máximo: $500.000 COP

### Plazo
- Valor positivo
- Máximo: 12 meses

### Email
- Formato de email válido
- Validación con Pydantic EmailStr


### Estructura del proyecto

```
api_villacreditos/
├── crud/
│   └── loan.py             # Operaciones CRUD
├── database/
│   └── connection.py       # Configuración de BD
├── models/
│   └── models.py           # Modelos SQLAlchemy
├── routers/
│   └── routers.py          # Endpoints de la API
├── schemas/
│   └── schemas.py          # Esquemas Pydantic
├── main.py                 # Aplicación principal
├── requirements.txt        # Dependencias
├── Dockerfile              # Configuración Docker
├── .dockerignore           # Archivos ignorados por Docker
├── .gitignore              # Archivos ignorados por Git
└── README.md               # Este archivo
```

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📝 Licencia

Este proyecto está bajo la Licencia MIT.

## 👥 Autores

- **Yuranis Villalba Villa** - *Desarrollo inicial*


## 📈 Roadmap

### Versión 2.0 (Próximamente)

- [ ] Autenticación JWT
- [ ] Roles de usuario (admin, cliente, analista)
- [ ] Cálculos de interés automáticos
- [ ] Notificaciones por email/SMS
- [ ] Reportes en PDF/Excel
- [ ] Integración con sistemas de pago


### Versión 1.1 (En desarrollo)

- [ ] Paginación en endpoints
- [ ] Filtros avanzados de búsqueda
- [ ] Validación de documentos
- [ ] Historial de cambios de estado
- [ ] Métricas y estadísticas

### Versión 1.0 (Completada)

- [x] Crear préstamo
- [x] Obtener préstamos
- [x] Actualizar préstamo
- [x] Eliminar préstamo
- [x] Documentación Swagger
- [x] Validaciones de datos
- [x] Base de datos SQLite


## 🙏 Agradecimientos

- FastAPI por el excelente framework
- SQLAlchemy por el ORM robusto
- Pydantic por la validación de datos
- La comunidad de Python por las herramientas


⭐ ¡No olvides dar una estrella al proyecto si te fue útil!

**Villa Créditos API** - Simplificando el acceso al crédito 🏦✨

**Creado con amor y dedicación** 💕👨‍💻