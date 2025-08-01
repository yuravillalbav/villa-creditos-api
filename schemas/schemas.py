from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class LoanApplication(BaseModel):
    user: str
    email: EmailStr
    phone: str = Field(..., min_length=7, max_length=15)
    address: str
    amount: float = Field(..., gt=0)
    term_months: int = Field(..., gt=0)

    class Config:
        json_schema_extra = {
            "example": {
                "user": "Yura Villa",
                "email": "yura@example.com",
                "phone": "3101234567",
                "address": "cra 22c #70-85",
                "amount": 500000.0,
                "term_months": 6
            }
        }

class LoanApplicationUpdate(BaseModel):
    user: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    amount: Optional[float] = None
    term_months: Optional[int] = None

class LoanApplicationResponse(LoanApplication):
    id: int

    class Config:
        from_attributes = True
