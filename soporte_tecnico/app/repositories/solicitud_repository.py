from sqlalchemy.orm import Session
from app.models.solicitud import Solicitud
from app.schemas.solicitud import SolicitudCreate, SolicitudUpdate

class SolicitudRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self, skip: int = 0, limit: int = 100):
        return self.db.query(Solicitud).offset(skip).limit(limit).all()

    def get_by_id(self, solicitud_id: int):
        return self.db.query(Solicitud).filter(Solicitud.id == solicitud_id).first()

    def get_by_codigo(self, codigo: str):
        return self.db.query(Solicitud).filter(Solicitud.codigo == codigo).first()

    def search(self, nombre: str = None, categoria_id: int = None,
               prioridad: str = None, estado: str = None):
        query = self.db.query(Solicitud)
        if nombre:
            query = query.filter(Solicitud.solicitante_nombre.ilike(f"%{nombre}%"))
        if categoria_id:
            query = query.filter(Solicitud.categoria_id == categoria_id)
        if prioridad:
            query = query.filter(Solicitud.prioridad == prioridad)
        if estado:
            query = query.filter(Solicitud.estado == estado)
        return query.all()

    def create(self, solicitud: SolicitudCreate):
        db_solicitud = Solicitud(**solicitud.model_dump())
        self.db.add(db_solicitud)
        self.db.commit()
        self.db.refresh(db_solicitud)
        return db_solicitud

    def update(self, solicitud_id: int, solicitud: SolicitudUpdate):
        db_solicitud = self.get_by_id(solicitud_id)
        if not db_solicitud:
            return None
        update_data = solicitud.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_solicitud, key, value)
        self.db.commit()
        self.db.refresh(db_solicitud)
        return db_solicitud

    def delete(self, solicitud_id: int):
        db_solicitud = self.get_by_id(solicitud_id)
        if not db_solicitud:
            return False
        self.db.delete(db_solicitud)
        self.db.commit()
        return True