from fpdf import FPDF
import matplotlib.pyplot as plt
import sqlite3

# Function to create a graph of the last 12 months energy consumptions:
def graph_maker(client_num, database_name):
    # client_num == device_id or sensor_id
    # Bring data from historical_lectures table:
    connecting_database = sqlite3.connect(database_name)
    cursor = connecting_database.cursor()
    cursor.execute(
        """
            SELECT month, monthly_consumption
            FROM historical_lectures
            WHERE sensor_id = ?
            LIMIT 12
    """, (client_num,))
    anual_data = cursor.fetchall()
    
    # Store months and energy values to be graphicated:
    months = []
    consumptions = []
    for d in anual_data:
        months.append(d[0])
        consumptions.append(d[1])
    global actual_month
    actual_month = months[0]
    months.reverse()
    consumptions.reverse()

    # Create a Graph and Save it as an Image
    plt.figure(figsize=(12, 6))
    plt.plot(months, consumptions, marker='o', linestyle='-', color='b')
    plt.xlabel("Ultimos 12 meses")
    plt.ylabel("Consumo eléctrico [kWh]")
    plt.title("Consumo eléctrico de los últimos 12 meses")
    plt.grid(True)
    plt.savefig(f"./Graphs/Historico_{actual_month}_{client_num}.png")  # Save the graph as an image.
    plt.close()

# Function to create an Invoice by month for each client
def invoice(initial_energy_lecture, final_energy_lectures, monthly_comsumn_energy, monthly_cost, initial_datetime, final_datetime, actual_datetime, client_num, client_first_name, client_last_name, client_address):

    class PDF(FPDF):    
        # header and footer methos are called automatically, but we have to extend the class and override them.
        def header(self):
            self.image("./logo.jpg", 10, 10, 20)                      # Rendering enterprise logo (path, position_x, position_y, width):
            self.set_font("helvetica", "B", 15)                       # Setting font: helvetica bold 15
            self.cell(50)                                             # Moving cursor to the right:
            self.cell(100, 10, "BOLETA DEL SERVICIO ELÉCTRICO", border=0, align="C")    # Printing title:
            self.ln(20)                                                                 # Performing a line break:
            self.set_font("helvetica", "", 10)                                          # Setting font: helvetica bold 15
            self.cell(20, 20, f"Cliente N°: {client_num}", border=0, align="L")
            self.ln(5)
            self.cell(20, 20, f"Factura N° (generar numero automatico)", border=0, align="L")
            self.ln(5)
            self.cell(20, 20, f"Fecha de emisión: {actual_datetime}", border=0, align="L")
            self.ln(5)
            self.cell(20, 20, f"Cliente: {client_first_name} {client_last_name}", border=0, align="L")
            self.ln(5)
            # self.cell(20, 20, f"RUT: {client_rut}", border=0, align="L")
            # self.ln(5)
            self.cell(20, 20, f"Dirección: {client_address}", border=0, align="L")
        def footer(self):
            self.set_y(-15)                                                 # Position cursor at 1.5 cm from bottom:
            self.set_font("helvetica", "I", 8)                              # Setting font: helvetica italic 8
            self.cell(0, 10, f"Página {self.page_no()}/{{nb}}", align="C")  # Printing page number:

    # Creating the instance of pdf to print the invoice:
    invoice_pdf = PDF()
    invoice_pdf.set_font("helvetica", size=10)
    invoice_pdf.add_page()

    # Inserting all the data of the invoice:
    invoice_pdf.ln(30)
    invoice_pdf.set_font("helvetica", size=12)
    invoice_pdf.cell(0, 0, f"Detalle del consumo eléctrico:", align="L")
    invoice_pdf.ln(10)
    invoice_pdf.set_font("helvetica", size=10)
    invoice_pdf.cell(0, 0, f"Lectura inicial [kWh]: {initial_energy_lecture:,.2f}. Fecha: {initial_datetime}", align="L")
    invoice_pdf.ln(7)
    invoice_pdf.cell(0, 0, f"Lectura final [kWh]: {final_energy_lectures:,.2f}. Fecha: {final_datetime}", align="L")
    invoice_pdf.ln(7)
    invoice_pdf.cell(0, 0, f"Consumo eléctrico [kWh]: {monthly_comsumn_energy:,.2f}", align="L")
    invoice_pdf.ln(7)
    invoice_pdf.set_font("helvetica","B", size=12)
    invoice_pdf.cell(0, 0, f"Total: ${monthly_cost:,.2f}", align="L")

    # Adding the image before saved into the pdf invoice:
    invoice_pdf.ln(30)
    invoice_pdf.set_font("helvetica", size=12)
    invoice_pdf.cell(0, 0, f"Registro historico anual", align="L")
    invoice_pdf.ln(10)
    invoice_pdf.image(f"./Graphs/Historico_{actual_month}_{client_num}.png", x=30, w=150)

    # Printing the invoice pdf:
    invoice_pdf.output(f"./Invoices/Cliente_N°{client_num}_factura_eléctrica_{actual_month}.pdf")