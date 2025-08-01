"""
Definición del modelo LoanRequest para la tabla 'loan_requests'.
"""
from sqlalchemy import Column, Integer, String, Float
from database.connection import Base

class LoanRequest(Base):
    """
    Modelo de solicitud de préstamo.
    """
    __tablename__ = "loan_requests"

    id = Column(Integer, primary_key=True, index=True)
    user = Column(String(100), nullable=False)
    email = Column(String(50), nullable=False)
    phone = Column(String(20), nullable=False)
    address = Column(String(20), nullable=False)
    amount = Column(Float, nullable=False)
    term_months = Column(Integer, nullable=False)
