from sqlalchemy.orm import Session
from models.models import LoanRequest
from schemas.schemas import LoanApplication, LoanApplicationUpdate

def get_all_requests(db: Session):
    return db.query(LoanRequest).all()

def create_request(db: Session, data: LoanApplication):
    new_request = LoanRequest(**data.dict())
    db.add(new_request)
    db.commit()
    db.refresh(new_request)
    return new_request

def get_total_requests(db: Session):
    return db.query(LoanRequest).count()

def delete_request(db: Session, request_id: int):
    request = db.get(LoanRequest, request_id)
    if request:
        db.delete(request)
        db.commit()
        return True
    return False

def update_request(db: Session, request_id: int, data: LoanApplicationUpdate):
    request = db.query(LoanRequest).filter(LoanRequest.id == request_id).first()
    if not request:
        return None
    for key, value in data.dict(exclude_unset=True).items():
        setattr(request, key, value)
    db.commit()
    db.refresh(request)
    return request
