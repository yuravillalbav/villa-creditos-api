"""
Rutas básicas para Villa Créditos API.
CRUD: crear, leer, actualizar, eliminar.
"""
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from schemas.schemas import LoanApplication, LoanApplicationResponse, LoanApplicationUpdate
from crud import loan as loan_crud
from database.connection import get_db

router = APIRouter(prefix="/loans", tags=["Loans"])

# ============================================================================
# OPERACIONES CRUD BÁSICAS
# ============================================================================


@router.post("/", response_model=LoanApplicationResponse, status_code=status.HTTP_201_CREATED)
def create_loan(loan: LoanApplication, db: Session = Depends(get_db)):
    """Crear una nueva solicitud de préstamo."""
    try:
        return loan_crud.create_request(db, loan)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al crear el préstamo: {str(e)}"
        )


@router.get("/", response_model=List[LoanApplicationResponse])
def get_all_loans(db: Session = Depends(get_db)):
    """Obtener todos los préstamos."""
    try:
        return loan_crud.get_all_requests(db)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener préstamos: {str(e)}"
        )


@router.get("/{loan_id}", response_model=LoanApplicationResponse)
def get_loan(loan_id: int, db: Session = Depends(get_db)):
    """Obtener un préstamo por ID."""
    loan = loan_crud.get_request_by_id(db, loan_id)
    if not loan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Préstamo no encontrado"
        )
    return loan


@router.patch("/{loan_id}", response_model=LoanApplicationResponse)
def update_loan(loan_id: int, loan_update: LoanApplicationUpdate, db: Session = Depends(get_db)):
    """Actualizar parcialmente un préstamo."""
    try:
        updated_loan = loan_crud.update_request(db, loan_id, loan_update)
        if not updated_loan:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Préstamo no encontrado"
            )
        return updated_loan
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al actualizar el préstamo: {str(e)}"
        )


@router.delete("/{loan_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_loan(loan_id: int, db: Session = Depends(get_db)):
    """Eliminar un préstamo."""
    success = loan_crud.delete_request(db, loan_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Préstamo no encontrado"
        )
