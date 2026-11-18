from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from app.core.config import settings
import logging

# Configuramos un logger para ver en consola si el correo se envía o falla
logger = logging.getLogger(__name__)

class EmailService:
    def __init__(self):
        self.conf = ConnectionConfig(
            MAIL_USERNAME=settings.MAIL_USERNAME,
            MAIL_PASSWORD=settings.MAIL_PASSWORD,
            MAIL_FROM=settings.MAIL_FROM,
            MAIL_SERVER=settings.MAIL_SERVER,
            MAIL_PORT=settings.MAIL_PORT,
            MAIL_STARTTLS=settings.MAIL_STARTTLS,
            MAIL_SSL_TLS=settings.MAIL_SSL_TLS,
            USE_CREDENTIALS=True,
        )
        self.fm = FastMail(self.conf)

    async def notificar_cambio_estado(self, solicitud, accion: str):
        try:
            html = f"""
            <h2>Solicitud {accion}</h2>
            <p><strong>Código:</strong> {solicitud.codigo}</p>
            <p><strong>Solicitante:</strong> {solicitud.solicitante_nombre}</p>
            <p><strong>Descripción:</strong> {solicitud.descripcion[:100]}...</p>
            <p><strong>Nuevo estado:</strong> {solicitud.estado}</p>
            <p><strong>Observaciones:</strong> {solicitud.observaciones or 'Sin observaciones'}</p>
            <p><strong>Fecha:</strong> {solicitud.fecha_registro}</p>
            """
            message = MessageSchema(
                subject=f"[Soporte Técnico] Solicitud {accion} - {solicitud.codigo}",
                recipients=[solicitud.solicitante_email],
                body=html,
                subtype=MessageType.html,
            )
            await self.fm.send_message(message)
            logger.info(f"✅ Correo enviado exitosamente para {solicitud.codigo}")
        except Exception as e:
            # En lugar de romper la app, solo mostramos una advertencia en consola
            logger.warning(f"⚠️ No se pudo enviar correo para {solicitud.codigo}. Error: {e}")