"""
Definición de modelos para el sistema de préstamos Villa Créditos.
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Enum as SQLEnum
from sqlalchemy.sql import func
from database.connection import Base
import enum


# Enums para la base de datos
class LoanStatusEnum(enum.Enum):
    """Estados posibles de un préstamo en la base de datos"""
    pending = "pending"
    approved = "approved"
    rejected = "rejected"
    disbursed = "disbursed"
    completed = "completed"
    defaulted = "defaulted"


class LoanPurposeEnum(enum.Enum):
    """Propósitos del préstamo en la base de datos"""
    personal = "personal"
    business = "business"
    education = "education"
    medical = "medical"
    home_improvement = "home_improvement"
    debt_consolidation = "debt_consolidation"
    other = "other"


class LoanRequest(Base):
    """
    Modelo mejorado de solicitud de préstamo.
    """
    __tablename__ = "loan_requests"

    # Campos principales
    id = Column(Integer, primary_key=True, index=True)
    user = Column(String(100), nullable=False, index=True)
    email = Column(String(100), nullable=False, index=True)
    phone = Column(String(20), nullable=False)
    address = Column(String(200), nullable=False)
    amount = Column(Float, nullable=False, index=True)
    term_months = Column(Integer, nullable=False)

    # Nuevos campos
    purpose = Column(SQLEnum(LoanPurposeEnum), nullable=False, default=LoanPurposeEnum.personal)
    monthly_income = Column(Float, nullable=True)
    employment_type = Column(String(50), nullable=True)

    # Campos de estado y seguimiento
    status = Column(SQLEnum(LoanStatusEnum), nullable=False, default=LoanStatusEnum.pending, index=True)
    notes = Column(Text, nullable=True)

    # Timestamps
    created_at = Column(DateTime, nullable=False, default=func.now(), index=True)
    updated_at = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<LoanRequest(id={self.id}, user='{self.user}', amount={self.amount}, status='{self.status.value}')>"


class LoanStatusHistory(Base):
    """
    Historial de cambios de estado de préstamos.
    """
    __tablename__ = "loan_status_history"

    id = Column(Integer, primary_key=True, index=True)
    loan_id = Column(Integer, nullable=False, index=True)  # Foreign key to LoanRequest
    previous_status = Column(SQLEnum(LoanStatusEnum), nullable=True)
    new_status = Column(SQLEnum(LoanStatusEnum), nullable=False)
    notes = Column(Text, nullable=True)
    updated_by = Column(String(100), nullable=True)
    created_at = Column(DateTime, nullable=False, default=func.now())

    def __repr__(self):
        return f"<LoanStatusHistory(loan_id={self.loan_id}, {self.previous_status} -> {self.new_status})>"


class DocumentValidation(Base):
    """
    Validación de documentos de identidad.
    """
    __tablename__ = "document_validations"

    id = Column(Integer, primary_key=True, index=True)
    loan_id = Column(Integer, nullable=False, index=True)  # Foreign key to LoanRequest
    document_type = Column(String(20), nullable=False)
    document_number = Column(String(20), nullable=False, index=True)
    is_valid = Column(Integer, nullable=False, default=0)  # 0=False, 1=True (SQLite compatible)
    validation_date = Column(DateTime, nullable=False, default=func.now())
    validation_notes = Column(Text, nullable=True)

    def __repr__(self):
        return f"<DocumentValidation(loan_id={self.loan_id}, doc={self.document_number}, valid={bool(self.is_valid)})>"


class LoanCalculation(Base):
    """
    Cálculos financieros de préstamos.
    """
    __tablename__ = "loan_calculations"

    id = Column(Integer, primary_key=True, index=True)
    loan_id = Column(Integer, nullable=False, index=True)  # Foreign key to LoanRequest
    interest_rate = Column(Float, nullable=False)
    monthly_payment = Column(Float, nullable=False)
    total_payment = Column(Float, nullable=False)
    total_interest = Column(Float, nullable=False)
    calculation_date = Column(DateTime, nullable=False, default=func.now())

    def __repr__(self):
        return f"<LoanCalculation(loan_id={self.loan_id}, monthly_payment={self.monthly_payment})>"
