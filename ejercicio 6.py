import sqlite3  
import tkinter as tk  
from tkinter import messagebox 

class MiembroDeFamilia:
    def __init__(self, nombre, apellido, edad, genero):
        self.nombre = nombre
        self.apellido = apellido
        self.edad = edad
        self.genero = genero
        self.generacion = self.determinar_generacion()

    def determinar_generacion(self):
        if self.edad < 18:
            return "Hijo"
        elif 18 <= self.edad < 35:
            return "Padre"
        elif 35 <= self.edad < 65:
            return "Abuelo"
        else:
            return "Bisabuelo"

    def mostrar_info(self):
        return f"{self.nombre} {self.apellido}, Edad: {self.edad}, Género: {self.genero}, Generación: {self.generacion}"

class GestionBaseDeDatos:
    def __init__(self, nombre_bd="arbol_genealogico.db"):
        self.conn = sqlite3.connect(nombre_bd)
        self.cursor = self.conn.cursor()
        self.crear_tabla()

    def crear_tabla(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS familiares (
                nombre TEXT,
                apellido TEXT,
                edad INTEGER,
                genero TEXT,
                generacion TEXT
            )
        ''')
        self.conn.commit()

    def agregar_miembro(self, miembro):
        self.cursor.execute('''
            INSERT INTO familiares (nombre, apellido, edad, genero, generacion)
            VALUES (?, ?, ?, ?, ?)
        ''', (miembro.nombre, miembro.apellido, miembro.edad, miembro.genero, miembro.generacion))
        self.conn.commit()

    def obtener_miembros(self):
        self.cursor.execute('SELECT * FROM familiares')
        return self.cursor.fetchall()

    def cerrar(self):
        self.conn.close()

class InterfazGrafica:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Árbol Genealógico de la Familia")
        self.bd = GestionBaseDeDatos() 

        self.crear_widgets()

    def crear_widgets(self):
        self.nombre_label = tk.Label(self.ventana, text="Nombre:")
        self.nombre_label.grid(row=0, column=0)
        self.nombre_entry = tk.Entry(self.ventana)
        self.nombre_entry.grid(row=0, column=1)

        self.apellido_label = tk.Label(self.ventana, text="Apellido:")
        self.apellido_label.grid(row=1, column=0)
        self.apellido_entry = tk.Entry(self.ventana)
        self.apellido_entry.grid(row=1, column=1)

        self.edad_label = tk.Label(self.ventana, text="Edad:")
        self.edad_label.grid(row=2, column=0)
        self.edad_entry = tk.Entry(self.ventana)
        self.edad_entry.grid(row=2, column=1)

        self.genero_label = tk.Label(self.ventana, text="Género:")
        self.genero_label.grid(row=3, column=0)
        self.genero_entry = tk.Entry(self.ventana)
        self.genero_entry.grid(row=3, column=1)

        self.agregar_button = tk.Button(self.ventana, text="Agregar Miembro", command=self.agregar_miembro)
        self.agregar_button.grid(row=4, column=0, columnspan=2)

        self.mostrar_button = tk.Button(self.ventana, text="Mostrar Árbol Ascendente", command=self.mostrar_ascendente)
        self.mostrar_button.grid(row=5, column=0, columnspan=2)

        self.mostrar_button_desc = tk.Button(self.ventana, text="Mostrar Árbol Descendente", command=self.mostrar_descendente)
        self.mostrar_button_desc.grid(row=6, column=0, columnspan=2)

    def agregar_miembro(self):
        try:
            nombre = self.nombre_entry.get()
            apellido = self.apellido_entry.get()
            edad = int(self.edad_entry.get())
            genero = self.genero_entry.get()

            if edad <= 0:
                raise ValueError("La edad debe ser un número positivo.")
            if genero not in ["Masculino", "Femenino"]:
                raise ValueError("Género debe ser 'Masculino' o 'Femenino'.")

            miembro = MiembroDeFamilia(nombre, apellido, edad, genero)
            self.bd.agregar_miembro(miembro)
            messagebox.showinfo("Éxito", "Miembro agregado correctamente")
        except ValueError as e:
            messagebox.showerror("Error", f"Entrada inválida: {e}")

    def mostrar_ascendente(self):
        miembros = self.bd.obtener_miembros()
        miembros_ordenados = sorted(miembros, key=lambda m: m[2]) 
        self.mostrar_en_pantalla(miembros_ordenados)

    def mostrar_descendente(self):
        miembros = self.bd.obtener_miembros()
        miembros_ordenados = sorted(miembros, key=lambda m: m[2], reverse=True)  
        self.mostrar_en_pantalla(miembros_ordenados)

    def mostrar_en_pantalla(self, miembros):
        resultado = "\n".join([f"{m[0]} {m[1]}, Edad: {m[2]}, Género: {m[3]}, Generación: {m[4]}" for m in miembros])
        messagebox.showinfo("Árbol Genealógico", resultado)

if __name__ == "__main__":
    ventana = tk.Tk()  
    interfaz = InterfazGrafica(ventana)  
    ventana.mainloop()
  
