from sqlalchemy.orm import Session
from app.repositories.solicitud_repository import SolicitudRepository
from app.schemas.solicitud import SolicitudCreate, SolicitudUpdate
# from app.services.email_service import EmailService

class SolicitudService:
    def __init__(self, db: Session):
        self.repo = SolicitudRepository(db)
        # self.email_service = EmailService()

    def listar(self, skip: int = 0, limit: int = 100):
        return self.repo.get_all(skip, limit)

    def buscar(self, nombre: str = None, categoria_id: int = None,
               prioridad: str = None, estado: str = None):
        return self.repo.search(nombre, categoria_id, prioridad, estado)

    def obtener(self, solicitud_id: int):
        return self.repo.get_by_id(solicitud_id)

    def crear(self, solicitud: SolicitudCreate):
        nueva = self.repo.create(solicitud)
        # self.email_service.notificar_cambio_estado(nueva, "creada")
        return nueva

    def actualizar(self, solicitud_id: int, solicitud: SolicitudUpdate):
        actualizada = self.repo.update(solicitud_id, solicitud)
        # if actualizada and (solicitud.estado or solicitud.observaciones):
        #     self.email_service.notificar_cambio_estado(actualizada, "actualizada")
        return actualizada

    def eliminar(self, solicitud_id: int):
        return self.repo.delete(solicitud_id)