from sqlalchemy.orm import Session
from app.models.categoria import Categoria
from app.schemas.categoria import CategoriaCreate

class CategoriaRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(Categoria).all()

    def get_by_id(self, categoria_id: int):
        return self.db.query(Categoria).filter(Categoria.id == categoria_id).first()

    def create(self, categoria: CategoriaCreate):
        db_categoria = Categoria(nombre=categoria.nombre)
        self.db.add(db_categoria)
        self.db.commit()
        self.db.refresh(db_categoria)
        return db_categoria