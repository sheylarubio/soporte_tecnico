from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from io import BytesIO
from app.api.deps import get_db
from app.services.solicitud_service import SolicitudService
from app.services.report_service import ReportService
from app.schemas.solicitud import (
    SolicitudCreate, SolicitudUpdate, SolicitudResponse
)

router = APIRouter(prefix="/solicitudes", tags=["Solicitudes"])

@router.get("/", response_model=list[SolicitudResponse])
def listar_solicitudes(
    skip: int = 0, limit: int = 100,
    nombre: str = Query(None), categoria_id: int = Query(None),
    prioridad: str = Query(None), estado: str = Query(None),
    db: Session = Depends(get_db)
):
    service = SolicitudService(db)
    return service.buscar(nombre, categoria_id, prioridad, estado)

@router.post("/", response_model=SolicitudResponse, status_code=201)
def crear_solicitud(solicitud: SolicitudCreate, db: Session = Depends(get_db)):
    service = SolicitudService(db)
    return service.crear(solicitud)

@router.put("/{solicitud_id}", response_model=SolicitudResponse)
def actualizar_solicitud(solicitud_id: int, solicitud: SolicitudUpdate,
                         db: Session = Depends(get_db)):
    service = SolicitudService(db)
    actualizada = service.actualizar(solicitud_id, solicitud)
    if not actualizada:
        raise HTTPException(status_code=404, detail="Solicitud no encontrada")
    return actualizada

@router.delete("/{solicitud_id}", status_code=204)
def eliminar_solicitud(solicitud_id: int, db: Session = Depends(get_db)):
    service = SolicitudService(db)
    if not service.eliminar(solicitud_id):
        raise HTTPException(status_code=404, detail="Solicitud no encontrada")
    return None

@router.get("/reporte/excel")
def exportar_excel(db: Session = Depends(get_db)):
    service = SolicitudService(db)
    solicitudes = service.listar()
    excel_bytes = ReportService.generar_excel(solicitudes)
    return StreamingResponse(
        BytesIO(excel_bytes),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=solicitudes.xlsx"}
    )

@router.get("/reporte/pdf")
def exportar_pdf(db: Session = Depends(get_db)):
    service = SolicitudService(db)
    solicitudes = service.listar()
    pdf_bytes = ReportService.generar_pdf(solicitudes)
    return StreamingResponse(
        BytesIO(pdf_bytes),
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=solicitudes.pdf"}
    )