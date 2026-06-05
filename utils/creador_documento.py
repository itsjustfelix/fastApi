import io
from datetime import datetime
from fpdf import FPDF
from models.consultas import Consultas_show

class HistoricoConsultasPDF(FPDF):
    def __init__(self,):
        
        super().__init__(orientation="P", unit="mm", format="letter")
        self.ruta_logo = "assets/logo.png"
        self.set_margins(15, 15, 15)
        self.set_auto_page_break(auto=True, margin=15)
    
    def header(self):
        
        self.set_font("Helvetica", "B", 16)
        
        
        ancho_disponible = self.epw 
        ancho_imagen = 25  
        ancho_texto = ancho_disponible - ancho_imagen

        start_y = self.get_y()
        start_x = self.get_x()

        self.cell(ancho_texto, 7, "Veterinaria MY VET", new_x="LMARGIN", new_y="NEXT", align="C")
        self.set_font("Helvetica", "", 12)
        self.set_text_color(128, 128, 128) # Gris medio
        self.cell(ancho_texto, 6, "Historial Clínico", new_x="LMARGIN", new_y="NEXT", align="C")
        self.set_text_color(0, 0, 0) # Resetear a negro

        
        if self.ruta_logo:
            try:
                self.set_xy(start_x + ancho_texto, start_y)
        
                self.image(self.ruta_logo, w=ancho_imagen)
            except FileNotFoundError:
                pass
    
        self.set_xy(15, start_y + 18)

    def footer(self):
        
        self.set_y(-15)
        self.set_font("Helvetica", "", 10)
        
        texto_pagina = f"Página {self.page_no()} de {{nb}}"
        self.cell(0, 10, texto_pagina, align="C")

def crear_documento_pdf(consulta: Consultas_show) -> bytes:
    pdf = HistoricoConsultasPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", "", 11)

    y_datos = pdf.get_y()
    ancho_columna = pdf.epw / 2

    pdf.set_x(15)
    pdf.cell(ancho_columna, 6, f"Código consulta: {consulta.codigo}", new_x="LEFT", new_y="NEXT")
    pdf.cell(ancho_columna, 6, f"Fecha documento: {datetime.now().strftime('%d/%m/%Y')}", new_x="LEFT", new_y="NEXT")
    pdf.cell(ancho_columna, 6, f"Fecha consulta: {consulta.fecha}", new_x="LEFT", new_y="NEXT")
    
    pdf.set_xy(15 + ancho_columna, y_datos)
    pdf.cell(ancho_columna, 6, f"Nombre mascota: {consulta.nombre_mascota}", new_x="LEFT", new_y="NEXT")
    pdf.set_x(15 + ancho_columna)
    pdf.cell(ancho_columna, 6, f"Nombre Veterinario: {consulta.nombre_veterinario}", new_x="LEFT", new_y="NEXT")

    pdf.ln(8)
    pdf.set_draw_color(180, 180, 180) 
    pdf.set_line_width(0.3)
    pdf.line(15, pdf.get_y(), 15 + pdf.epw, pdf.get_y())
    pdf.ln(5)

    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 8, "Descripción del propietario:", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 12)
    pdf.multi_cell(0, 6, f"{consulta.descripcion}", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)

    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 8, "Motivo de la consulta:", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 12)
    pdf.multi_cell(0, 6, f"{consulta.diagnostico}", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)

    
    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 8, "Observaciones del veterinario:", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 12)
    pdf.multi_cell(0, 6, f"{consulta.tratamiento}", new_x="LMARGIN", new_y="NEXT")

    return bytes(pdf.output())