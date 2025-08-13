"""
Operaciones CRUD para préstamos con validaciones básicas y manejo de errores.
"""
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from models.models import LoanRequest
from schemas.schemas import LoanApplication, LoanApplicationUpdate


def get_all_requests(db: Session):
    """Obtener todos los préstamos"""
    try:
        return db.query(LoanRequest).order_by(LoanRequest.created_at.desc()).all()
    except SQLAlchemyError as e:
        print(f"Error obteniendo préstamos: {e}")
        raise


def get_request_by_id(db: Session, request_id: int):
    """Obtener un préstamo por ID"""
    try:
        return db.query(LoanRequest).filter(LoanRequest.id == request_id).first()
    except SQLAlchemyError as e:
        print(f"Error obteniendo préstamo {request_id}: {e}")
        raise


def create_request(db: Session, data: LoanApplication):
    """Crear un nuevo préstamo con validaciones básicas"""
    try:
        # Crear nuevo préstamo
        new_request = LoanRequest(**data.model_dump())
        db.add(new_request)
        db.commit()
        db.refresh(new_request)
        print(f"✅ Préstamo creado: ID {new_request.id}")
        return new_request

    except SQLAlchemyError as e:
        db.rollback()
        print(f"Error creando préstamo: {e}")
        raise


def get_total_requests(db: Session):
    """Obtener total de préstamos"""
    try:
        return db.query(LoanRequest).count()
    except SQLAlchemyError as e:
        print(f"Error contando préstamos: {e}")
        raise


def delete_request(db: Session, request_id: int):
    """Eliminar un préstamo por ID"""
    try:
        request = db.get(LoanRequest, request_id)
        if request:
            db.delete(request)
            db.commit()
            print(f"✅ Préstamo eliminado: ID {request_id}")
            return True
        else:
            print(f"⚠️  Préstamo no encontrado: ID {request_id}")
            return False

    except SQLAlchemyError as e:
        db.rollback()
        print(f"Error eliminando préstamo {request_id}: {e}")
        raise


def update_request(db: Session, request_id: int, data: LoanApplicationUpdate):
    """Actualizar un préstamo existente"""
    try:
        request = db.query(LoanRequest).filter(
            LoanRequest.id == request_id).first()
        if not request:
            print(
                f"⚠️  Préstamo no encontrado para actualizar: ID {request_id}")
            return None

        # Actualizar solo los campos que se enviaron
        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(request, key, value)

        db.commit()
        db.refresh(request)
        print(f"✅ Préstamo actualizado: ID {request_id}")
        return request

    except SQLAlchemyError as e:
        db.rollback()
        print(f"Error actualizando préstamo {request_id}: {e}")
        raise
