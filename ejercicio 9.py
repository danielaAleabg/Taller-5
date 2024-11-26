import tkinter as tk
from tkinter import messagebox
import pandas as pd
import sqlite3
import numpy as np
import matplotlib.pyplot as plt
import datetime
from sympy import symbols, Eq, solve

conn = sqlite3.connect('cinema.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS peliculas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT,
    horario TEXT
)
''')
cursor.execute('''
CREATE TABLE IF NOT EXISTS tiquetes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_pelicula INTEGER,
    cantidad INTEGER,
    FOREIGN KEY (id_pelicula) REFERENCES peliculas(id)
)
''')
cursor.execute('''
CREATE TABLE IF NOT EXISTS comidas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT,
    precio REAL
)
''')
conn.commit()

def agregar_pelicula():
    nombre = entry_nombre_pelicula.get()
    horario = entry_horario.get()
    cursor.execute('INSERT INTO peliculas (nombre, horario) VALUES (?, ?)', (nombre, horario))
    conn.commit()
    actualizar_cartelera()

def actualizar_cartelera():
    cursor.execute('SELECT * FROM peliculas')
    peliculas = cursor.fetchall()
    listbox_cartelera.delete(0, tk.END)
    for pelicula in peliculas:
        listbox_cartelera.insert(tk.END, f"{pelicula[1]} - {pelicula[2]}")

def comprar_tiquete():
    try:
        pelicula_seleccionada = listbox_cartelera.curselection()[0]
        id_pelicula = cursor.execute('SELECT id FROM peliculas').fetchall()[pelicula_seleccionada][0]
        cantidad = int(entry_cantidad.get())
        cursor.execute('INSERT INTO tiquetes (id_pelicula, cantidad) VALUES (?, ?)', (id_pelicula, cantidad))
        conn.commit()
        messagebox.showinfo("Compra Realizada", f"Tiquetes comprados para {listbox_cartelera.get(pelicula_seleccionada)}")
    except Exception as e:
        messagebox.showerror("Error", "Por favor seleccione una película y una cantidad válida.")

def vender_comida():
    try:
        comida = entry_comida.get()
        precio = float(entry_precio.get())
        cursor.execute('INSERT INTO comidas (nombre, precio) VALUES (?, ?)', (comida, precio))
        conn.commit()
        messagebox.showinfo("Venta Realizada", f"Comida {comida} vendida por {precio}!")
        actualizar_comidas()
    except Exception as e:
        messagebox.showerror("Error", "Hubo un problema al registrar la venta.")

def actualizar_comidas():
    cursor.execute('SELECT * FROM comidas')
    comidas = cursor.fetchall()
    listbox_comidas.delete(0, tk.END)
    for comida in comidas:
        listbox_comidas.insert(tk.END, f"{comida[1]} - {comida[2]}")

def mostrar_informe():
    cursor.execute('SELECT p.nombre, SUM(t.cantidad), SUM(t.cantidad) * c.precio FROM peliculas p JOIN tiquetes t ON p.id = t.id_pelicula JOIN comidas c ON t.id_pelicula = c.id GROUP BY p.nombre')
    resultados = cursor.fetchall()
    informe_texto = "Informe de Ventas\n\n"
    for resultado in resultados:
        informe_texto += f"Película: {resultado[0]}, Tiquetes Vendidos: {resultado[1]}, Ganancias: {resultado[2]}\n"
    messagebox.showinfo("Informe de Ventas", informe_texto)

def mostrar_interfaz():
    window = tk.Tk()
    window.title("Gestión Cinema")

    label_nombre_pelicula = tk.Label(window, text="Nombre de la Película:")
    label_nombre_pelicula.pack()
    entry_nombre_pelicula = tk.Entry(window)
    entry_nombre_pelicula.pack()

    label_horario = tk.Label(window, text="Horario:")
    label_horario.pack()
    entry_horario = tk.Entry(window)
    entry_horario.pack()

    button_agregar_pelicula = tk.Button(window, text="Agregar Película", command=agregar_pelicula)
    button_agregar_pelicula.pack()

    label_comprar_tiquete = tk.Label(window, text="Comprar Tiquetes")
    label_comprar_tiquete.pack()

    label_cantidad = tk.Label(window, text="Cantidad de Tiquetes:")
    label_cantidad.pack()
    entry_cantidad = tk.Entry(window)
    entry_cantidad.pack()

    button_comprar_tiquete = tk.Button(window, text="Comprar Tiquete", command=comprar_tiquete)
    button_comprar_tiquete.pack()

    label_comida = tk.Label(window, text="Vender Comida")
    label_comida.pack()

    label_comida_nombre = tk.Label(window, text="Nombre de la Comida:")
    label_comida_nombre.pack()
    entry_comida = tk.Entry(window)
    entry_comida.pack()

    label_precio = tk.Label(window, text="Precio de la Comida:")
    label_precio.pack()
    entry_precio = tk.Entry(window)
    entry_precio.pack()

    button_vender_comida = tk.Button(window, text="Vender Comida", command=vender_comida)
    button_vender_comida.pack()

    button_informe = tk.Button(window, text="Ver Informe de Ventas", command=mostrar_informe)
    button_informe.pack()

    listbox_cartelera = tk.Listbox(window, height=10, width=50)
    listbox_cartelera.pack()
    listbox_comidas = tk.Listbox(window, height=10, width=50)
    listbox_comidas.pack()

    actualizar_cartelera()
    actualizar_comidas()

    window.mainloop()

mostrar_interfaz()

conn.close()
