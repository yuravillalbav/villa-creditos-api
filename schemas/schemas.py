from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional, List, Literal
from datetime import datetime
from enum import Enum
import re


# Enums para estados y tipos
class LoanStatus(str, Enum):
    """Estados posibles de un préstamo"""
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    DISBURSED = "disbursed"
    COMPLETED = "completed"
    DEFAULTED = "defaulted"


class LoanPurpose(str, Enum):
    """Propósitos del préstamo"""
    PERSONAL = "personal"
    BUSINESS = "business"
    EDUCATION = "education"
    MEDICAL = "medical"
    HOME_IMPROVEMENT = "home_improvement"
    DEBT_CONSOLIDATION = "debt_consolidation"
    OTHER = "other"


class LoanApplication(BaseModel):
    """Esquema para solicitud de préstamo con validaciones mejoradas"""
    user: str = Field(..., min_length=2, max_length=100, description="Nombre completo del solicitante")
    email: EmailStr = Field(..., description="Correo electrónico válido")
    phone: str = Field(..., min_length=7, max_length=15, description="Número de teléfono")
    address: str = Field(..., min_length=10, max_length=200, description="Dirección completa")
    amount: float = Field(..., gt=0, le=50000000, description="Monto solicitado en pesos colombianos")
    term_months: int = Field(..., gt=0, le=60, description="Plazo en meses (máximo 60)")
    purpose: LoanPurpose = Field(default=LoanPurpose.PERSONAL, description="Propósito del préstamo")
    monthly_income: Optional[float] = Field(None, gt=0, description="Ingresos mensuales")
    employment_type: Optional[str] = Field(None, max_length=50, description="Tipo de empleo")

    @field_validator('phone')
    @classmethod
    def validate_phone(cls, v):
        """Validar formato de teléfono colombiano"""
        phone_pattern = r'^(\+57|57)?[0-9]{10}$|^[0-9]{7,10}$'
        if not re.match(phone_pattern, v.replace(' ', '').replace('-', '')):
            raise ValueError('Formato de teléfono inválido')
        return v

    @field_validator('user')
    @classmethod
    def validate_user_name(cls, v):
        """Validar que el nombre contenga solo letras y espacios"""
        if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', v):
            raise ValueError('El nombre solo puede contener letras y espacios')
        return v.strip()

    class Config:
        json_schema_extra = {
            "example": {
                "user": "Yura Villa",
                "email": "yura@example.com",
                "phone": "3101234567",
                "address": "Carrera 22c #70-85, Bogotá",
                "amount": 500000.0,
                "term_months": 6,
                "purpose": "personal",
                "monthly_income": 2000000.0,
                "employment_type": "empleado"
            }
        }

class LoanApplicationUpdate(BaseModel):
    """Esquema para actualización parcial de solicitud de préstamo"""
    user: Optional[str] = Field(None, min_length=2, max_length=100, description="Nombre completo del solicitante")
    email: Optional[EmailStr] = Field(None, description="Correo electrónico válido")
    phone: Optional[str] = Field(None, min_length=7, max_length=15, description="Número de teléfono")
    address: Optional[str] = Field(None, min_length=10, max_length=200, description="Dirección completa")
    amount: Optional[float] = Field(None, gt=0, le=50000000, description="Monto solicitado en pesos colombianos")
    term_months: Optional[int] = Field(None, gt=0, le=60, description="Plazo en meses (máximo 60)")
    purpose: Optional[LoanPurpose] = Field(None, description="Propósito del préstamo")
    monthly_income: Optional[float] = Field(None, gt=0, description="Ingresos mensuales")
    employment_type: Optional[str] = Field(None, max_length=50, description="Tipo de empleo")

    @field_validator('phone')
    @classmethod
    def validate_phone(cls, v):
        """Validar formato de teléfono colombiano"""
        if v is None:
            return v
        phone_pattern = r'^(\+57|57)?[0-9]{10}$|^[0-9]{7,10}$'
        if not re.match(phone_pattern, v.replace(' ', '').replace('-', '')):
            raise ValueError('Formato de teléfono inválido')
        return v

    @field_validator('user')
    @classmethod
    def validate_user_name(cls, v):
        """Validar que el nombre contenga solo letras y espacios"""
        if v is None:
            return v
        if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', v):
            raise ValueError('El nombre solo puede contener letras y espacios')
        return v.strip()

class LoanApplicationResponse(LoanApplication):
    id: int
    status: Optional[LoanStatus] = None
    notes: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True




# Esquemas de respuesta y error
class ErrorResponse(BaseModel):
    """Esquema para respuestas de error"""
    error: str = Field(..., description="Tipo de error")
    message: str = Field(..., description="Mensaje descriptivo del error")
    details: Optional[dict] = Field(None, description="Detalles adicionales del error")


class SuccessResponse(BaseModel):
    """Esquema para respuestas exitosas"""
    success: bool = Field(True, description="Indica si la operación fue exitosa")
    message: str = Field(..., description="Mensaje descriptivo")
    data: Optional[dict] = Field(None, description="Datos adicionales")


# Esquemas de paginación
class PaginationParams(BaseModel):
    """Parámetros de paginación"""
    page: int = Field(1, ge=1, description="Número de página")
    size: int = Field(10, ge=1, le=100, description="Tamaño de página")


class PaginatedResponse(BaseModel):
    """Respuesta paginada genérica"""
    items: List[LoanApplicationResponse] = Field(..., description="Lista de elementos")
    total: int = Field(..., ge=0, description="Total de elementos")
    page: int = Field(..., ge=1, description="Página actual")
    size: int = Field(..., ge=1, description="Tamaño de página")
    pages: int = Field(..., ge=0, description="Total de páginas")


# Esquemas de filtrado y búsqueda
class LoanFilters(BaseModel):
    """Filtros para búsqueda de préstamos"""
    status: Optional[LoanStatus] = Field(None, description="Filtrar por estado")
    purpose: Optional[LoanPurpose] = Field(None, description="Filtrar por propósito")
    min_amount: Optional[float] = Field(None, ge=0, description="Monto mínimo")
    max_amount: Optional[float] = Field(None, ge=0, description="Monto máximo")
    min_term: Optional[int] = Field(None, ge=1, description="Plazo mínimo en meses")
    max_term: Optional[int] = Field(None, ge=1, description="Plazo máximo en meses")
    user_search: Optional[str] = Field(None, min_length=1, description="Buscar por nombre de usuario")
    email_search: Optional[str] = Field(None, min_length=1, description="Buscar por email")


# Esquemas de estadísticas
class LoanStatistics(BaseModel):
    """Estadísticas de préstamos"""
    total_loans: int = Field(..., ge=0, description="Total de préstamos")
    total_amount: float = Field(..., ge=0, description="Monto total prestado")
    average_amount: float = Field(..., ge=0, description="Monto promedio")
    loans_by_status: dict = Field(..., description="Préstamos agrupados por estado")
    loans_by_purpose: dict = Field(..., description="Préstamos agrupados por propósito")


class MonthlyStatistics(BaseModel):
    """Estadísticas mensuales"""
    month: str = Field(..., description="Mes en formato YYYY-MM")
    total_loans: int = Field(..., ge=0, description="Total de préstamos del mes")
    total_amount: float = Field(..., ge=0, description="Monto total del mes")
    approved_loans: int = Field(..., ge=0, description="Préstamos aprobados")
    rejected_loans: int = Field(..., ge=0, description="Préstamos rechazados")


# Esquemas para actualización de estado
class LoanStatusUpdate(BaseModel):
    """Esquema para actualizar el estado de un préstamo"""
    status: LoanStatus = Field(..., description="Nuevo estado del préstamo")
    notes: Optional[str] = Field(None, max_length=500, description="Notas adicionales")
    updated_by: Optional[str] = Field(None, max_length=100, description="Usuario que realiza la actualización")


# Esquemas de validación de documentos
class DocumentType(str, Enum):
    """Tipos de documentos"""
    CEDULA = "cedula"
    PASSPORT = "passport"
    CEDULA_EXTRANJERIA = "cedula_extranjeria"


class DocumentValidation(BaseModel):
    """Esquema para validación de documentos"""
    document_type: DocumentType = Field(..., description="Tipo de documento")
    document_number: str = Field(..., min_length=5, max_length=20, description="Número de documento")
    is_valid: bool = Field(..., description="Si el documento es válido")
    validation_date: datetime = Field(..., description="Fecha de validación")


# Esquemas para cálculos financieros
class LoanCalculation(BaseModel):
    """Esquema para cálculos de préstamo"""
    amount: float = Field(..., gt=0, description="Monto del préstamo")
    term_months: int = Field(..., gt=0, le=60, description="Plazo en meses")
    interest_rate: float = Field(..., gt=0, le=100, description="Tasa de interés anual")


class LoanCalculationResponse(BaseModel):
    """Respuesta de cálculos de préstamo"""
    monthly_payment: float = Field(..., description="Cuota mensual")
    total_payment: float = Field(..., description="Total a pagar")
    total_interest: float = Field(..., description="Total de intereses")
    payment_schedule: List[dict] = Field(..., description="Cronograma de pagos")


# Esquema para notificaciones
class NotificationType(str, Enum):
    """Tipos de notificación"""
    EMAIL = "email"
    SMS = "sms"
    PUSH = "push"


class NotificationRequest(BaseModel):
    """Esquema para solicitud de notificación"""
    loan_id: int = Field(..., description="ID del préstamo")
    notification_type: NotificationType = Field(..., description="Tipo de notificación")
    recipient: str = Field(..., description="Destinatario (email o teléfono)")
    message: str = Field(..., max_length=500, description="Mensaje a enviar")


# Esquema para reportes
class ReportType(str, Enum):
    """Tipos de reporte"""
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    YEARLY = "yearly"


class ReportRequest(BaseModel):
    """Esquema para solicitud de reporte"""
    report_type: ReportType = Field(..., description="Tipo de reporte")
    start_date: datetime = Field(..., description="Fecha de inicio")
    end_date: datetime = Field(..., description="Fecha de fin")
    include_details: bool = Field(False, description="Incluir detalles en el reporte")
    format: Literal["json", "csv", "pdf"] = Field("json", description="Formato del reporte")
