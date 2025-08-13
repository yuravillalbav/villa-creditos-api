import enum


class LoanStatus(str, enum.Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"
    disbursed = "disbursed"
    completed = "completed"
    defaulted = "defaulted"


class LoanPurpose(str, enum.Enum):
    personal = "personal"
    business = "business"
    education = "education"
    medical = "medical"
    other = "other"
