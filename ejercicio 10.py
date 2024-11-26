import sqlite3
import tkinter as tk
from tkinter import messagebox, simpledialog

conn = sqlite3.connect('vehiculos.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS vehiculos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tipo TEXT,
    marca TEXT,
    modelo TEXT,
    año INTEGER,
    color TEXT,
    placa TEXT
)
''')
conn.commit()

class Vehiculo:
    def __init__(self, tipo, marca, modelo, año, color, placa):
        self.tipo = tipo
        self.marca = marca
        self.modelo = modelo
        self.año = año
        self.color = color
        self.placa = placa

    def mostrar_info(self):
        return f"Tipo: {self.tipo}, Marca: {self.marca}, Modelo: {self.modelo}, Año: {self.año}, Color: {self.color}, Placa: {self.placa}"

    def agregar_vehiculo(self):
        cursor.execute('''
        INSERT INTO vehiculos (tipo, marca, modelo, año, color, placa)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (self.tipo, self.marca, self.modelo, self.año, self.color, self.placa))
        conn.commit()

    def editar_vehiculo(self, id_vehiculo):
        cursor.execute('''
        UPDATE vehiculos
        SET tipo = ?, marca = ?, modelo = ?, año = ?, color = ?, placa = ?
        WHERE id = ?
        ''', (self.tipo, self.marca, self.modelo, self.año, self.color, self.placa, id_vehiculo))
        conn.commit()

    def borrar_vehiculo(self, id_vehiculo):
        cursor.execute('DELETE FROM vehiculos WHERE id = ?', (id_vehiculo,))
        conn.commit()

class Coche(Vehiculo):
    def __init__(self, marca, modelo, año, color, placa, puertas):
        super().__init__("Coche", marca, modelo, año, color, placa)
        self.puertas = puertas

    def mostrar_info(self):
        return super().mostrar_info() + f", Puertas: {self.puertas}"

class Moto(Vehiculo):
    def __init__(self, marca, modelo, año, color, placa, cilindrada):
        super().__init__("Moto", marca, modelo, año, color, placa)
        self.cilindrada = cilindrada

    def mostrar_info(self):
        return super().mostrar_info() + f", Cilindrada: {self.cilindrada}"

def agregar_vehiculo():
    tipo = simpledialog.askstring("Tipo de Vehículo", "Ingrese el tipo de vehículo (Coche/Moto):")
    marca = simpledialog.askstring("Marca", "Ingrese la marca del vehículo:")
    modelo = simpledialog.askstring("Modelo", "Ingrese el modelo del vehículo:")
    año = simpledialog.askinteger("Año", "Ingrese el año del vehículo:")
    color = simpledialog.askstring("Color", "Ingrese el color del vehículo:")
    placa = simpledialog.askstring("Placa", "Ingrese la placa del vehículo:")

    if tipo.lower() == "coche":
        puertas = simpledialog.askinteger("Puertas", "Ingrese el número de puertas del coche:")
        vehiculo = Coche(marca, modelo, año, color, placa, puertas)
    elif tipo.lower() == "moto":
        cilindrada = simpledialog.askinteger("Cilindrada", "Ingrese la cilindrada de la moto:")
        vehiculo = Moto(marca, modelo, año, color, placa, cilindrada)
    else:
        messagebox.showerror("Error", "Tipo de vehículo no reconocido.")
        return

    vehiculo.agregar_vehiculo()
    messagebox.showinfo("Éxito", "Vehículo agregado correctamente.")

def editar_vehiculo():
    id_vehiculo = simpledialog.askinteger("ID de Vehículo", "Ingrese el ID del vehículo a editar:")
    cursor.execute('SELECT * FROM vehiculos WHERE id = ?', (id_vehiculo,))
    vehiculo_data = cursor.fetchone()

    if vehiculo_data:
        tipo = simpledialog.askstring("Tipo de Vehículo", f"Tipo actual: {vehiculo_data[1]}. Ingrese el nuevo tipo:")
        marca = simpledialog.askstring("Marca", f"Marca actual: {vehiculo_data[2]}. Ingrese la nueva marca:")
        modelo = simpledialog.askstring("Modelo", f"Modelo actual: {vehiculo_data[3]}. Ingrese el nuevo modelo:")
        año = simpledialog.askinteger("Año", f"Año actual: {vehiculo_data[4]}. Ingrese el nuevo año:")
        color = simpledialog.askstring("Color", f"Color actual: {vehiculo_data[5]}. Ingrese el nuevo color:")
        placa = simpledialog.askstring("Placa", f"Placa actual: {vehiculo_data[6]}. Ingrese la nueva placa:")

        vehiculo = Vehiculo(tipo, marca, modelo, año, color, placa)
        vehiculo.editar_vehiculo(id_vehiculo)
        messagebox.showinfo("Éxito", "Vehículo editado correctamente.")
    else:
        messagebox.showerror("Error", "Vehículo no encontrado.")

def borrar_vehiculo():
    id_vehiculo = simpledialog.askinteger("ID de Vehículo", "Ingrese el ID del vehículo a borrar:")
    cursor.execute('SELECT * FROM vehiculos WHERE id = ?', (id_vehiculo,))
    vehiculo_data = cursor.fetchone()

    if vehiculo_data:
        vehiculo = Vehiculo("", "", "", 0, "", "")
        vehiculo.borrar_vehiculo(id_vehiculo)
        messagebox.showinfo("Éxito", "Vehículo borrado correctamente.")
    else:
        messagebox.showerror("Error", "Vehículo no encontrado.")

def mostrar_vehiculos():
    cursor.execute('SELECT * FROM vehiculos')
    vehiculos = cursor.fetchall()
    info_vehiculos = "\n".join([f"ID: {v[0]} - {v[1]} {v[2]} {v[3]} - Año: {v[4]} - Color: {v[5]} - Placa: {v[6]}" for v in vehiculos])
    messagebox.showinfo("Vehículos Registrados", info_vehiculos)

def crear_interfaz():
    window = tk.Tk()
    window.title("Gestión de Vehículos")

    tk.Button(window, text="Agregar Vehículo", command=agregar_vehiculo).pack(pady=10)
    tk.Button(window, text="Editar Vehículo", command=editar_vehiculo).pack(pady=10)
    tk.Button(window, text="Borrar Vehículo", command=borrar_vehiculo).pack(pady=10)
    tk.Button(window, text="Mostrar Vehículos", command=mostrar_vehiculos).pack(pady=10)

    window.mainloop()

crear_interfaz()

conn.close()
