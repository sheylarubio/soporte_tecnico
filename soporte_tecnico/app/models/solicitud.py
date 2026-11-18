from sqlalchemy import Column, Integer, String, Text, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base

class Solicitud(Base):
    __tablename__ = "solicitudes"

    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String(20), unique=True, nullable=False, index=True)
    solicitante_nombre = Column(String(100), nullable=False)
    solicitante_email = Column(String(100), nullable=False)
    descripcion = Column(Text, nullable=False)
    categoria_id = Column(Integer, ForeignKey("categorias.id"), nullable=False)
    fecha_registro = Column(DateTime, default=datetime.utcnow)
    prioridad = Column(Enum("baja", "media", "alta", name="prioridad_enum"), nullable=False)
    estado = Column(Enum("pendiente", "en_proceso", "resuelta", name="estado_enum"),
                    default="pendiente", nullable=False)
    observaciones = Column(Text, nullable=True)

    categoria = relationship("Categoria", back_populates="solicitudes")