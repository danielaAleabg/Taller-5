import pandas as pd
import numpy as np
import sqlite3
from datetime import datetime
import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt

class Animal:
    def __init__(self, nombre, edad, habitat, fecha_ingreso):
        self.nombre = nombre
        self.edad = edad
        self.habitat = habitat
        self.fecha_ingreso = fecha_ingreso

    def mostrar_info(self):
        return f"Nombre: {self.nombre}, Edad: {self.edad}, Hábitat: {self.habitat}, Fecha de Ingreso: {self.fecha_ingreso}"

class Terrestre(Animal):
    def __init__(self, nombre, edad, habitat, fecha_ingreso, tipo_piel, dieta):
        super().__init__(nombre, edad, habitat, fecha_ingreso)
        self.tipo_piel = tipo_piel
        self.dieta = dieta

    def mostrar_info(self):
        base_info = super().mostrar_info()
        return f"{base_info}, Tipo de Piel: {self.tipo_piel}, Dieta: {self.dieta}"

class Aereo(Animal):
    def __init__(self, nombre, edad, habitat, fecha_ingreso, tipo_alas, habilidad_vuelo):
        super().__init__(nombre, edad, habitat, fecha_ingreso)
        self.tipo_alas = tipo_alas
        self.habilidad_vuelo = habilidad_vuelo

    def mostrar_info(self):
        base_info = super().mostrar_info()
        return f"{base_info}, Tipo de Alas: {self.tipo_alas}, Habilidad de Vuelo: {self.habilidad_vuelo}"

class Acuatico(Animal):
    def __init__(self, nombre, edad, habitat, fecha_ingreso, tipo_agua, habilidad_natacion):
        super().__init__(nombre, edad, habitat, fecha_ingreso)
        self.tipo_agua = tipo_agua
        self.habilidad_natacion = habilidad_natacion

    def mostrar_info(self):
        base_info = super().mostrar_info()
        return f"{base_info}, Tipo de Agua: {self.tipo_agua}, Habilidad de Natación: {self.habilidad_natacion}"

class BaseDeDatos:
    def __init__(self):
        self.conn = sqlite3.connect('zoologico.db')
        self.cursor = self.conn.cursor()
        self.crear_tablas()

    def crear_tablas(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS animales (
            id INTEGER PRIMARY KEY,
            nombre TEXT,
            edad INTEGER,
            habitat TEXT,
            especie TEXT,
            tipo_piel TEXT,
            dieta TEXT,
            tipo_alas TEXT,
            habilidad_vuelo TEXT,
            tipo_agua TEXT,
            habilidad_natacion TEXT,
            fecha_ingreso TEXT
        )''')
        self.conn.commit()

    def insertar_animal(self, animal, especie):
        fecha_ingreso = animal.fecha_ingreso
        if isinstance(animal, Terrestre):
            self.cursor.execute('''INSERT INTO animales (nombre, edad, habitat, especie, tipo_piel, dieta, fecha_ingreso)
                                   VALUES (?, ?, ?, ?, ?, ?, ?)''', (animal.nombre, animal.edad, animal.habitat, especie, animal.tipo_piel, animal.dieta, fecha_ingreso))
        elif isinstance(animal, Aereo):
            self.cursor.execute('''INSERT INTO animales (nombre, edad, habitat, especie, tipo_alas, habilidad_vuelo, fecha_ingreso)
                                   VALUES (?, ?, ?, ?, ?, ?, ?)''', (animal.nombre, animal.edad, animal.habitat, especie, animal.tipo_alas, animal.habilidad_vuelo, fecha_ingreso))
        elif isinstance(animal, Acuatico):
            self.cursor.execute('''INSERT INTO animales (nombre, edad, habitat, especie, tipo_agua, habilidad_natacion, fecha_ingreso)
                                   VALUES (?, ?, ?, ?, ?, ?, ?)''', (animal.nombre, animal.edad, animal.habitat, especie, animal.tipo_agua, animal.habilidad_natacion, fecha_ingreso))
        self.conn.commit()

    def mostrar_animales(self):
        self.cursor.execute("SELECT * FROM animales")
        rows = self.cursor.fetchall()
        for row in rows:
            print(row)

def mostrar_grafico():
    df = pd.read_sql_query("SELECT especie, COUNT(*) FROM animales GROUP BY especie", conn)
    df.plot(kind='bar', x='especie', y='COUNT(*)', title='Número de Animales por Especie', legend=False)
    plt.ylabel('Cantidad')
    plt.show()

class ZoologicoGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Zoológico")
        self.db = BaseDeDatos()

        self.nombre_label = tk.Label(root, text="Nombre del Animal")
        self.nombre_label.grid(row=0, column=0)
        self.nombre_entry = tk.Entry(root)
        self.nombre_entry.grid(row=0, column=1)

        self.edad_label = tk.Label(root, text="Edad del Animal")
        self.edad_label.grid(row=1, column=0)
        self.edad_entry = tk.Entry(root)
        self.edad_entry.grid(row=1, column=1)

        self.habitat_label = tk.Label(root, text="Hábitat del Animal")
        self.habitat_label.grid(row=2, column=0)
        self.habitat_entry = tk.Entry(root)
        self.habitat_entry.grid(row=2, column=1)

        self.especie_label = tk.Label(root, text="Especie del Animal")
        self.especie_label.grid(row=3, column=0)
        self.especie_var = tk.StringVar(value="Terrestre")
        self.especie_menu = tk.OptionMenu(root, self.especie_var, "Terrestre", "Aéreo", "Acuático")
        self.especie_menu.grid(row=3, column=1)

        self.ingresar_button = tk.Button(root, text="Ingresar Animal", command=self.ingresar_animal)
        self.ingresar_button.grid(row=4, column=0, columnspan=2)

        self.grafico_button = tk.Button(root, text="Mostrar Gráfico", command=mostrar_grafico)
        self.grafico_button.grid(row=5, column=0, columnspan=2)

    def ingresar_animal(self):
        nombre = self.nombre_entry.get()
        edad = int(self.edad_entry.get())
        habitat = self.habitat_entry.get()
        especie = self.especie_var.get()
        fecha_ingreso = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        if especie == "Terrestre":
            tipo_piel = input("Ingrese tipo de piel: ")
            dieta = input("Ingrese dieta: ")
            animal = Terrestre(nombre, edad, habitat, fecha_ingreso, tipo_piel, dieta)
            self.db.insertar_animal(animal, especie)
        elif especie == "Aéreo":
            tipo_alas = input("Ingrese tipo de alas: ")
            habilidad_vuelo = input("Ingrese habilidad de vuelo: ")
            animal = Aereo(nombre, edad, habitat, fecha_ingreso, tipo_alas, habilidad_vuelo)
            self.db.insertar_animal(animal, especie)
        elif especie == "Acuático":
            tipo_agua = input("Ingrese tipo de agua: ")
            habilidad_natacion = input("Ingrese habilidad de natación: ")
            animal = Acuatico(nombre, edad, habitat, fecha_ingreso, tipo_agua, habilidad_natacion)
            self.db.insertar_animal(animal, especie)

        messagebox.showinfo("Éxito", f"El animal {nombre} ha sido ingresado exitosamente.")

root = tk.Tk()
app = ZoologicoGUI(root)
root.mainloop()
