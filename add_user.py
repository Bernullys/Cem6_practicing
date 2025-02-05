import sqlite3

# Connect to the database:
db_connection = sqlite3.connect("./cem6_display_lectures.db")
cursor_command = db_connection.cursor()

# Create the table:
cursor_command.execute(
    """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            phone TEXT NOT NULL,
            email TEXT NOT NULL,
            address TEXT NOT NULL,
            sensor_id INTEGER NOT NULL
        )
    """
)

# Insert a new user:
first_name = input("Ingrese el nombre(s) del usuario: ")
last_name = input("Ingrese el apellido(s) del usuario: ")
phone = input("Ingrese el teléfono del usuario: ")
email = input("Ingrese el email del usuario: ")
address = input("Ingrese la dirección del usuario: ")
sensor_id = input("Ingrese el ID del sensor: ")

# Insert user into the table:
cursor_command.execute(
    """
        INSERT INTO users (first_name, last_name, phone, email, address, sensor_id)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (first_name, last_name, phone, email, address, sensor_id)
)

# Commit and close:
db_connection.commit()
db_connection.close()