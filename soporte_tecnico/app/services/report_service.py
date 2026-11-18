import io
from openpyxl import Workbook
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle, SimpleDocTemplate

class ReportService:

    @staticmethod
    def generar_excel(solicitudes) -> bytes:
        wb = Workbook()
        ws = wb.active
        ws.title = "Solicitudes"
        headers = ["Código", "Solicitante", "Categoría", "Descripción",
                   "Fecha", "Prioridad", "Estado"]
        ws.append(headers)
        for s in solicitudes:
            ws.append([
                s.codigo, s.solicitante_nombre, s.categoria.nombre,
                s.descripcion[:50], str(s.fecha_registro), s.prioridad, s.estado
            ])
        output = io.BytesIO()
        wb.save(output)
        output.seek(0)
        return output.getvalue()

    @staticmethod
    def generar_pdf(solicitudes) -> bytes:
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        data = [["Código", "Solicitante", "Categoría", "Prioridad", "Estado"]]
        for s in solicitudes:
            data.append([s.codigo, s.solicitante_nombre, s.categoria.nombre,
                         s.prioridad, s.estado])
        table = Table(data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        doc.build([table])
        buffer.seek(0)
        return buffer.getvalue()