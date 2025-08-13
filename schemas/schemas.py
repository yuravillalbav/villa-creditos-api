"""
Esquemas básicos de validación para Villa Créditos API.
Solo contiene los esquemas necesarios para operaciones CRUD básicas.
"""
from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional
from datetime import datetime
from enums.enums import LoanPurpose, LoanStatus
import re

# ============================================================================
# ESQUEMAS PRINCIPALES
# ============================================================================


class LoanApplication(BaseModel):
    """Esquema para crear una nueva solicitud de préstamo."""
    user: str = Field(..., min_length=2, max_length=100,
                      description="Nombre completo del solicitante")
    email: EmailStr = Field(..., description="Correo electrónico válido")
    phone: str = Field(..., min_length=7, max_length=15,
                       description="Número de teléfono")
    address: str = Field(..., min_length=10, max_length=200,
                         description="Dirección completa")
    amount: float = Field(..., gt=0, le=5000000,
                          description="Monto solicitado en pesos colombianos")
    term_months: int = Field(..., gt=0, le=60,
                             description="Plazo en meses (máximo 60)")
    purpose: LoanPurpose = Field(
        default=LoanPurpose.personal, description="Propósito del préstamo")
    monthly_income: Optional[float] = Field(
        None, gt=0, description="Ingresos mensuales")
    employment_type: Optional[str] = Field(
        None, max_length=50, description="Tipo de empleo")

    @field_validator('phone')
    @classmethod
    def validate_phone(cls, v):
        """Validar formato de teléfono colombiano"""
        clean_phone = v.replace(' ', '').replace('-', '')
        patterns = [
            r'^(\+57|57)?[3][0-9]{9}$',  # Celular
            r'^(\+57|57)?[1-8][0-9]{6,7}$'  # Fijo
        ]
        if not any(re.match(pattern, clean_phone) for pattern in patterns):
            raise ValueError(
                'Formato de teléfono inválido. Use formato colombiano')
        return clean_phone

    @field_validator('user')
    @classmethod
    def validate_user_name(cls, v):
        """Validar que el nombre contenga solo letras y espacios"""
        if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', v.strip()):
            raise ValueError('El nombre solo puede contener letras y espacios')
        return v.strip()

    @field_validator('amount')
    @classmethod
    def validate_amount(cls, v):
        """Validar que el monto sea realista"""
        if v < 100000:
            raise ValueError('El monto mínimo es $100.000 COP')
        if v > 500000:
            raise ValueError('El monto máximo es $500.000 COP')
        return v


class LoanApplicationUpdate(BaseModel):
    """Esquema para actualizar una solicitud de préstamo."""
    user: Optional[str] = Field(None, min_length=2, max_length=100)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, min_length=7, max_length=15)
    address: Optional[str] = Field(None, min_length=10, max_length=200)
    amount: Optional[float] = Field(None, gt=0, le=50000000)
    term_months: Optional[int] = Field(None, gt=0, le=12)
    purpose: Optional[LoanPurpose] = None
    monthly_income: Optional[float] = Field(None, gt=0)
    employment_type: Optional[str] = Field(None, max_length=50)

    @field_validator('phone')
    @classmethod
    def validate_phone(cls, v):
        """Validar formato de teléfono colombiano (si se proporciona)"""
        if v is None:
            return v
        clean_phone = v.replace(' ', '').replace('-', '')
        patterns = [
            r'^(\+57|57)?[3][0-9]{9}$',
            r'^(\+57|57)?[1-8][0-9]{6,7}$'
        ]
        if not any(re.match(pattern, clean_phone) for pattern in patterns):
            raise ValueError(
                'Formato de teléfono inválido. Use formato colombiano')
        return clean_phone

    @field_validator('user')
    @classmethod
    def validate_user_name(cls, v):
        """Validar que el nombre contenga solo letras y espacios (si se proporciona)"""
        if v is None:
            return v
        if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', v.strip()):
            raise ValueError('El nombre solo puede contener letras y espacios')
        return v.strip()

    @field_validator('amount')
    @classmethod
    def validate_amount(cls, v):
        """Validar que el monto sea realista (si se proporciona)"""
        if v is None:
            return v
        if v < 100000:
            raise ValueError('El monto mínimo es $100,000 COP')
        if v > 50000000:
            raise ValueError('El monto máximo es $50,000,000 COP')
        return v


class LoanApplicationResponse(LoanApplication):
    """Esquema de respuesta que incluye campos adicionales del sistema."""
    id: int = Field(..., description="ID único del préstamo")
    status: Optional[LoanStatus] = Field(
        default=LoanStatus.pending, description="Estado actual del préstamo")
    notes: Optional[str] = Field(
        None, description="Notas adicionales del préstamo")
    created_at: Optional[datetime] = Field(
        None, description="Fecha y hora de creación")
    updated_at: Optional[datetime] = Field(
        None, description="Fecha y hora de última actualización")

    class Config:
        from_attributes = True
