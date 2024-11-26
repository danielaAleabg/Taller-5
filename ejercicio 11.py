import sqlite3
import pandas as pd
import numpy as np
import sympy as sp
import matplotlib.pyplot as plt
from tkinter import *
from tkinter import simpledialog, messagebox
from datetime import datetime

conn = sqlite3.connect('cinema.db')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS empleados (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    usuario TEXT,
                    contrasena TEXT)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    tipo TEXT, 
                    usuario TEXT,
                    contrasena TEXT)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS peliculas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT,
                    horario TEXT,
                    sala INTEGER)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS tiquetes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    id_pelicula INTEGER,
                    id_usuario INTEGER,
                    fecha_compra TEXT)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS comidas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    producto TEXT,
                    precio REAL)''')

class Usuario:
    def __init__(self, tipo, usuario, contrasena):
        self.tipo = tipo
        self.usuario = usuario
        self.contrasena = contrasena

    def es_valido(self, usuario, contrasena):
        return self.usuario == usuario and self.contrasena == contrasena

class Empleado(Usuario):
    def __init__(self, usuario, contrasena):
        super().__init__("Empleado", usuario, contrasena)

class UsuarioFrecuente(Usuario):
    def __init__(self, usuario, contrasena):
        super().__init__("Frecuente", usuario, contrasena)

class UsuarioVisitante(Usuario):
    def __init__(self):
        super().__init__("Visitante", "", "")

class Cinema:
    def __init__(self):
        self.peliculas = []
        self.comidas = []
        self.usuarios = []
        self.empleados = []

    def agregar_pelicula(self, nombre, horario, sala):
        cursor.execute('INSERT INTO peliculas (nombre, horario, sala) VALUES (?, ?, ?)', 
                       (nombre, horario, sala))
        conn.commit()

    def mostrar_cartelera(self):
        cursor.execute('SELECT * FROM peliculas')
        peliculas = cursor.fetchall()
        cartelera = "\n".join([f"{p[1]} - {p[2]} - Sala {p[3]}" for p in peliculas])
        messagebox.showinfo("Cartelera", cartelera)

    def agregar_comida(self, producto, precio):
        cursor.execute('INSERT INTO comidas (producto, precio) VALUES (?, ?)', (producto, precio))
        conn.commit()

    def mostrar_comidas(self):
        cursor.execute('SELECT * FROM comidas')
        comidas = cursor.fetchall()
        menu_comidas = "\n".join([f"{c[1]} - ${c[2]}" for c in comidas])
        messagebox.showinfo("Menú de Comidas", menu_comidas)

    def comprar_tiquete(self, id_usuario, id_pelicula):
        cursor.execute('SELECT * FROM tiquetes WHERE id_pelicula = ? AND id_usuario = ?', (id_pelicula, id_usuario))
        tiquete_existente = cursor.fetchone()
        if tiquete_existente:
            messagebox.showerror("Error", "Ya has comprado un tiquete para esta película.")
            return
        
        cursor.execute('INSERT INTO tiquetes (id_usuario, id_pelicula, fecha_compra) VALUES (?, ?, ?)',
                       (id_usuario, id_pelicula, str(datetime.now())))
        conn.commit()
        messagebox.showinfo("Éxito", "Tiquete comprado correctamente.")

    def generar_informe(self):
        cursor.execute('SELECT p.nombre, COUNT(t.id) AS tiquetes_vendidos, SUM(c.precio) AS total_ventas '
                       'FROM peliculas p LEFT JOIN tiquetes t ON p.id = t.id_pelicula '
                       'LEFT JOIN comidas c ON c.id = t.id_pelicula '
                       'GROUP BY p.id')
        informe = cursor.fetchall()
        df = pd.DataFrame(informe, columns=["Película", "Tiquetes Vendidos", "Dinero Ganado"])
        df.to_csv('informe.csv', index=False)
        messagebox.showinfo("Informe Generado", "El informe ha sido generado exitosamente.")

class Interfaz:
    def __init__(self, root, cinema):
        self.root = root
        self.cinema = cinema

    def login(self):
        tipo_usuario = simpledialog.askstring("Tipo de Usuario", "Ingrese tipo de usuario (Empleado, Frecuente, Visitante):")
        usuario = simpledialog.askstring("Usuario", "Ingrese su nombre de usuario:")
        contrasena = simpledialog.askstring("Contraseña", "Ingrese su contraseña:", show="*")

        if tipo_usuario.lower() == "empleado":
            for emp in self.cinema.empleados:
                if emp.es_valido(usuario, contrasena):
                    messagebox.showinfo("Login", "Bienvenido, Empleado.")
                    return
            messagebox.showerror("Error", "Empleado no encontrado.")
        elif tipo_usuario.lower() == "frecuente":
            for user in self.cinema.usuarios:
                if isinstance(user, UsuarioFrecuente) and user.es_valido(usuario, contrasena):
                    messagebox.showinfo("Login", "Bienvenido, Usuario Frecuente.")
                    return
            messagebox.showerror("Error", "Usuario Frecuente no encontrado.")
        else:
            messagebox.showinfo("Login", "Bienvenido, Usuario Visitante.")

    def mostrar_menu(self):
        self.root = Tk()
        self.root.title("Sistema Cinema")

        Button(self.root, text="Mostrar Cartelera", command=self.cinema.mostrar_cartelera).pack(pady=10)
        Button(self.root, text="Comprar Tiquetes", command=self.comprar_tiquetes).pack(pady=10)
        Button(self.root, text="Venta de Comidas", command=self.cinema.mostrar_comidas).pack(pady=10)
        Button(self.root, text="Generar Informe", command=self.cinema.generar_informe).pack(pady=10)

        self.root.mainloop()

    def comprar_tiquetes(self):
        pelicula_id = simpledialog.askinteger("Seleccionar Película", "Ingrese ID de la película:")
        usuario_id = simpledialog.askinteger("ID de Usuario", "Ingrese su ID de usuario:")
        self.cinema.comprar_tiquete(usuario_id, pelicula_id)

def main():
    cinema = Cinema()

    empleado1 = Empleado("admin", "admin123")
    cinema.empleados.append(empleado1)

    usuario1 = UsuarioFrecuente("usuario1", "pass1")
    cinema.usuarios.append(usuario1)

    cinema.agregar_pelicula("Película 1", "11:30 AM", 1)
    cinema.agregar_pelicula("Película 2", "2:00 PM", 2)
    cinema.agregar_comida("Palomitas", 5.0)
    cinema.agregar_comida("Refresco", 3.0)

    interfaz = Interfaz(Tk(), cinema)
    interfaz.login()
    interfaz.mostrar_menu()

if __name__ == "__main__":
    main()
