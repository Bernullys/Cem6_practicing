from fpdf import FPDF
import matplotlib.pyplot as plt
import pandas as pd

# Sample data:
data = {
    "Ene": 150,
    "Feb": 180,
    "Mar": 210,
    "Abr": 190,
    "May": 230,
    "Jun": 250,
    "Jul": 200,
    "Ago": 220,
    "Sep": 240,
    "Oct": 260,
    "Nov": 270,
    "Dic": 280
}

# Step 1: Create a Graph and Save it as an Image
plt.figure(figsize=(6, 4))
plt.plot(data.keys(), data.values(), marker='o', linestyle='-', color='b')
plt.xlabel("Ultimos 12 meses")
plt.ylabel("Consumo eléctrico [kWh]")
plt.title("Consumo eléctrico de los últimos 12 meses")
plt.grid(True)
plt.savefig("graph.png")  # Save the graph as an image
plt.close()

def invoice(tip_amount, taxes):

    class PDF(FPDF):    # header and footer methos are called automatically, but we have to extend the class and override them.
        
        def header(self):
            self.image("./logo.jpg", 10, 10, 20)                      # Rendering logo (path, position_x, position_y, width):
            self.set_font("helvetica", "B", 15)                             # Setting font: helvetica bold 15
            self.cell(50)                                                   # Moving cursor to the right:
            self.cell(100, 10, "BOLETA DEL SERVICIO ELÉCTRICO", border=0, align="C")         # Printing title:
            self.ln(20)                                                     # Performing a line break:
            self.set_font("helvetica", "", 10)                             # Setting font: helvetica bold 15
            self.cell(20, 20, f"Cliente N° (generar numero automatico)", border=0, align="L")
            self.ln(5)
            self.cell(20, 20, f"Factura N° (generar numero automatico)", border=0, align="L")
            self.ln(5)
            self.cell(20, 20, f"Fecha de emisión (generar numero automatico)", border=0, align="L")
            self.ln(5)
            self.cell(20, 20, f"Cliente: (asignar a db)", border=0, align="L")
            self.ln(5)
            self.cell(20, 20, f"RUT: (asignar a db)", border=0, align="L")
            self.ln(5)
            self.cell(20, 20, f"Dirección: (asignar a db)", border=0, align="L")

        def footer(self):
            self.set_y(-15)                                                 # Position cursor at 1.5 cm from bottom:
            self.set_font("helvetica", "I", 8)                              # Setting font: helvetica italic 8
            self.cell(0, 10, f"Página {self.page_no()}/{{nb}}", align="C")    # Printing page number:
    
    invoice_pdf = PDF()
    invoice_pdf.set_font("helvetica", size=10)
    invoice_pdf.add_page()

    invoice_pdf.ln(30)
    invoice_pdf.set_font("helvetica", size=12)
    invoice_pdf.cell(0, 0, f"Detalle del consumo eléctrico:", align="L")

    invoice_pdf.ln(10)
    invoice_pdf.set_font("helvetica", size=10)
    invoice_pdf.cell(0, 0, f"Lectura inicial [kWh]:                 {tip_amount:,.2f}", align="L")
    invoice_pdf.ln(7)
    invoice_pdf.cell(0, 0, f"Lectura final [kWh]:                   {tip_amount:,.2f}", align="L")
    invoice_pdf.ln(7)
    invoice_pdf.cell(0, 0, f"Consumo eléctrico [kWh]:               {taxes:,.2f}", align="L")
    invoice_pdf.ln(7)
    invoice_pdf.set_font("helvetica","B", size=12)
    invoice_pdf.cell(0, 0, f"Total:                                ${taxes+tip_amount:,.2f}", align="L")

    invoice_pdf.ln(30)
    invoice_pdf.set_font("helvetica", size=12)
    invoice_pdf.cell(0, 0, f"Registro historico anual", align="L")

    invoice_pdf.ln(10)
    invoice_pdf.image("graph.png", x=30, w=150)

    invoice_pdf.output(f"electric_bill.pdf")
          
invoice(44444, 22444444)