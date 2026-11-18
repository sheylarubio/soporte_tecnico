from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from app.repositories.categoria_repository import CategoriaRepository
from app.schemas.categoria import CategoriaCreate

class CategoriaService:
    def __init__(self, db: Session):
        self.repo = CategoriaRepository(db)

    def listar(self):
        return self.repo.get_all()

    def obtener(self, categoria_id: int):
        return self.repo.get_by_id(categoria_id)

    def crear(self, categoria: CategoriaCreate):
        try:
            return self.repo.create(categoria)
        except IntegrityError:
            # Si MySQL rechaza por duplicado, hacemos rollback y avisamos
            self.repo.db.rollback()
            raise HTTPException(
                status_code=400,
                detail=f"La categoría '{categoria.nombre}' ya existe."
            )