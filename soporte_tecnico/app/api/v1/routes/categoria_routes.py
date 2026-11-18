from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.services.categoria_service import CategoriaService
from app.schemas.categoria import CategoriaCreate, CategoriaResponse

router = APIRouter(prefix="/categorias", tags=["Categorías"])

@router.get("/", response_model=list[CategoriaResponse])
def listar_categorias(db: Session = Depends(get_db)):
    service = CategoriaService(db)
    return service.listar()

@router.post("/", response_model=CategoriaResponse, status_code=201)
def crear_categoria(categoria: CategoriaCreate, db: Session = Depends(get_db)):
    service = CategoriaService(db)
    return service.crear(categoria)