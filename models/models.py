"""
Modelos de base de datos para Villa Créditos API.
Define las tablas y relaciones para el sistema de gestión de préstamos.
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Enum as SQLEnum
from sqlalchemy.sql import func
from database.connection import Base
from enums.enums import LoanPurpose, LoanStatus

# ============================================================================
# MODELO PRINCIPAL
# ============================================================================


class LoanRequest(Base):
    """
    Modelo principal para solicitudes de préstamo.

    Contiene toda la información necesaria para gestionar un préstamo:
    - Datos del solicitante (nombre, email, teléfono, dirección)
    - Detalles del préstamo (monto, plazo, propósito)
    - Información adicional (ingresos, tipo de empleo)
    - Estado y seguimiento (status, notas, timestamps)
    """
    __tablename__ = "loan_requests"

    # Campos principales - Información del solicitante
    id = Column(Integer, primary_key=True, index=True,
                comment="ID único del préstamo")
    user = Column(String(100), nullable=False, index=True,
                  comment="Nombre completo del solicitante")
    email = Column(String(100), nullable=False, index=True,
                   comment="Correo electrónico")
    phone = Column(String(20), nullable=False, comment="Número de teléfono")
    address = Column(String(200), nullable=False, comment="Dirección completa")

    # Campos del préstamo
    amount = Column(Float, nullable=False, index=True,
                    comment="Monto solicitado en COP")
    term_months = Column(Integer, nullable=False, comment="Plazo en meses")
    purpose = Column(SQLEnum(LoanPurpose), nullable=False,
                     default=LoanPurpose.personal, comment="Propósito del préstamo")

    # Información adicional (opcional)
    monthly_income = Column(Float, nullable=True,
                            comment="Ingresos mensuales en COP")
    employment_type = Column(String(50), nullable=True,
                             comment="Tipo de empleo")

    # Estado y seguimiento
    status = Column(SQLEnum(LoanStatus), nullable=False, default=LoanStatus.pending,
                    index=True, comment="Estado actual del préstamo")
    notes = Column(Text, nullable=True,
                   comment="Notas adicionales del préstamo")

    # Timestamps automáticos
    created_at = Column(DateTime, nullable=False, default=func.now(
    ), index=True, comment="Fecha de creación")
    updated_at = Column(DateTime, nullable=False, default=func.now(
    ), onupdate=func.now(), comment="Fecha de última actualización")

    def __repr__(self):
        """Representación string del objeto para debugging"""
        return f"<LoanRequest(id={self.id}, user='{self.user}', amount=${self.amount:,.0f}, status='{self.status.value}')>"

    def to_dict(self):
        """Convertir el objeto a diccionario"""
        return {
            'id': self.id,
            'user': self.user,
            'email': self.email,
            'phone': self.phone,
            'address': self.address,
            'amount': self.amount,
            'term_months': self.term_months,
            'purpose': self.purpose.value if self.purpose else None,
            'monthly_income': self.monthly_income,
            'employment_type': self.employment_type,
            'status': self.status.value if self.status else None,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
