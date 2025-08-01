from typing import List

from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session

from schemas.schemas import LoanApplication, LoanApplicationResponse, LoanApplicationUpdate
from crud import loan as loan_crud
from database.connection import get_db

router = APIRouter(prefix="/loans", tags=["loans"])

@router.post("/", response_model=LoanApplicationResponse)
def create_loan_endpoint(loan: LoanApplication, db: Session = Depends(get_db)):
    return loan_crud.create_request(db, loan)

@router.get("/", response_model=List[LoanApplicationResponse])
def get_loans_endpoint(db: Session = Depends(get_db)):
    return loan_crud.get_all_requests(db)

@router.delete("/{loan_id}", status_code=204)
def delete_loan_endpoint(loan_id: int, db: Session = Depends(get_db)):
    success = loan_crud.delete_request(db, loan_id)
    if not success:
        raise HTTPException(status_code=404, detail="Loan not found")
    return Response(status_code=204)

@router.patch("/{loan_id}", response_model=LoanApplicationResponse)
def update_loan_endpoint(loan_id: int, loan_data: LoanApplicationUpdate, db: Session = Depends(get_db)):
    return loan_crud.update_request(db, loan_id, loan_data)
