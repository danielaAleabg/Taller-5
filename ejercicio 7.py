import datetime
import sqlite3
import tkinter as tk
from tkinter import messagebox
import pandas as pd

class Persona:
    def __init__(self, nombre, apellido, edad, genero):
        self.nombre = nombre
        self.apellido = apellido
        self.edad = edad
        self.genero = genero
        self.generacion = None

    def asignar_generacion(self):
        """Asigna la generación según la edad de la persona"""
        if self.edad >= 80:
            self.generacion = "Bisabuelos"
        elif self.edad >= 60:
            self.generacion = "Abuelos"
        elif self.edad >= 30:
            self.generacion = "Padres"
        elif self.edad >= 18:
            self.generacion = "Yo"
        else:
            self.generacion = "Hijos"

    def mostrar_datos(self):
        """Muestra los datos de la persona"""
        return f"Nombre: {self.nombre} {self.apellido}, Edad: {self.edad}, Género: {self.genero}, Generación: {self.generacion}"

class Generacion:
    def __init__(self, nombre_generacion):
        self.nombre_generacion = nombre_generacion
        self.miembros = []

    def agregar_miembro(self, persona):
        """Agrega a una persona a la generación"""
        self.miembros.append(persona)

    def mostrar_miembros(self):
        """Muestra los miembros de la generación"""
        return [persona.mostrar_datos() for persona in self.miembros]

def crear_arbol_genealogico():
    bisabuelos = Generacion("Bisabuelos")
    abuelos = Generacion("Abuelos")
    padres = Generacion("Padres")
    yo = Generacion("Yo")
    hijos = Generacion("Hijos")

    persona1 = Persona("Juan", "Pérez", 85, "Masculino")
    persona2 = Persona("Maria", "Gonzalez", 62, "Femenino")
    persona3 = Persona("Carlos", "Pérez", 40, "Masculino")
    persona4 = Persona("Ana", "Pérez", 25, "Femenino")
    persona5 = Persona("Lucía", "Pérez", 10, "Femenino")

    persona1.asignar_generacion()
    persona2.asignar_generacion()
    persona3.asignar_generacion()
    persona4.asignar_generacion()
    persona5.asignar_generacion()

    if persona1.generacion == "Bisabuelos":
        bisabuelos.agregar_miembro(persona1)
    elif persona2.generacion == "Abuelos":
        abuelos.agregar_miembro(persona2)
    elif persona3.generacion == "Padres":
        padres.agregar_miembro(persona3)
    elif persona4.generacion == "Yo":
        yo.agregar_miembro(persona4)
    elif persona5.generacion == "Hijos":
        hijos.agregar_miembro(persona5)

    print("Árbol Genealógico Ascendente:")
    print("Bisabuelos:", bisabuelos.mostrar_miembros())
    print("Abuelos:", abuelos.mostrar_miembros())
    print("Padres:", padres.mostrar_miembros())
    print("Yo:", yo.mostrar_miembros())
    print("Hijos:", hijos.mostrar_miembros())

    conn = sqlite3.connect('arbol_genealogico.db')
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS personas (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nombre TEXT,
                        apellido TEXT,
                        edad INTEGER,
                        genero TEXT,
                        generacion TEXT)''')

    for persona in [persona1, persona2, persona3, persona4, persona5]:
        cursor.execute('''INSERT INTO personas (nombre, apellido, edad, genero, generacion)
                        VALUES (?, ?, ?, ?, ?)''', 
                        (persona.nombre, persona.apellido, persona.edad, persona.genero, persona.generacion))
    
    conn.commit()
    conn.close()

def mostrar_interfaz():
    window = tk.Tk()
    window.title("Árbol Genealógico")

    label = tk.Label(window, text="Bienvenido al sistema de Árbol Genealógico", font=("Arial", 16))
    label.pack(pady=20)

    button = tk.Button(window, text="Mostrar Árbol Genealógico", command=crear_arbol_genealogico)
    button.pack(pady=10)

    window.mainloop()

mostrar_interfaz()
