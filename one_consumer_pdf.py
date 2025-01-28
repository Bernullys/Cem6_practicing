from fpdf import FPDF

def invoice(tip_amount, taxes):

    class PDF(FPDF):    # header and footer methos are called automatically, but we have to extend the class and override them.
        
        def header(self):
            self.image("./logo.jpg", 10, 10, 20)                      # Rendering logo (path, position_x, position_y, width):
            self.set_font("helvetica", "B", 15)                             # Setting font: helvetica bold 15
            self.cell(50)                                                   # Moving cursor to the right:
            self.cell(100, 10, "__BADR__BAR__RESTAURANT__", border=0, align="C")         # Printing title:
            self.ln(20)                                                     # Performing a line break:
            self.set_font("helvetica", "B", 12)                             # Setting font: helvetica bold 15
            self.cell(20, 20, f"This is your invoice", border=0, align="L")
            self.ln(20)

        def footer(self):
            self.set_y(-15)                                                 # Position cursor at 1.5 cm from bottom:
            self.set_font("helvetica", "I", 8)                              # Setting font: helvetica italic 8
            self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", align="C")    # Printing page number:

    
    taxes = 22
    tip_amount = 24
    
    invoice_pdf = PDF()
    invoice_pdf.set_font("helvetica", size=10)
    invoice_pdf.add_page()

    invoice_pdf.ln(20)
    invoice_pdf.set_font("helvetica", size=12)
    invoice_pdf.cell(0, 0, f"Subtotal: ${tip_amount:,.2f}", align="R")
    invoice_pdf.ln(7)
    invoice_pdf.cell(0, 0, f"Tip: ${tip_amount:,.2f}", align="R")
    invoice_pdf.ln(7)
    invoice_pdf.cell(0, 0, f"Taxes: ${taxes:,.2f}", align="R")
    invoice_pdf.ln(7)
    invoice_pdf.set_font("helvetica","B", size=12)
    invoice_pdf.cell(0, 0, f"Total: ${taxes+tip_amount:,.2f}", align="R")

    invoice_pdf.output(f"_bill.pdf")
          
invoice(24, 22)