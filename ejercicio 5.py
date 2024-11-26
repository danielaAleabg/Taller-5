import sympy as sp
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sqlite3
from datetime import datetime
import tkinter as tk
from tkinter import messagebox


# Clase base Vehiculo
class Vehiculo:
    def __init__(self, marca, modelo, precio, tipo_pintura, unidades_disponibles):
        self.marca = marca
        self.modelo = modelo
        self.precio = precio
        self.tipo_pintura = tipo_pintura
        self.unidades_disponibles = unidades_disponibles

    def vender(self, cantidad):
        if self.unidades_disponibles >= cantidad:
            self.unidades_disponibles -= cantidad
            return True
        else:
            return False

    def mostrar_informacion(self):
        return f"Marca: {self.marca}, Modelo: {self.modelo}, Precio: ${self.precio}, Pintura: {self.tipo_pintura}, Unidades disponibles: {self.unidades_disponibles}"


# Subclases para tipos específicos de vehículos
class Automovil(Vehiculo):
    def __init__(self, marca, modelo, precio, tipo_pintura, unidades_disponibles, puertas):
        super().__init__(marca, modelo, precio, tipo_pintura, unidades_disponibles)
        self.puertas = puertas

    def mostrar_informacion(self):
        return super().mostrar_informacion() + f", Puertas: {self.puertas}"


class Camioneta(Vehiculo):
    def __init__(self, marca, modelo, precio, tipo_pintura, unidades_disponibles, traccion):
        super().__init__(marca, modelo, precio, tipo_pintura, unidades_disponibles)
        self.traccion = traccion

    def mostrar_informacion(self):
        return super().mostrar_informacion() + f", Tracción: {self.traccion}"


class Camion(Vehiculo):
    def __init__(self, marca, modelo, precio, tipo_pintura, unidades_disponibles, carga_maxima):
        super().__init__(marca, modelo, precio, tipo_pintura, unidades_disponibles)
        self.carga_maxima = carga_maxima

    def mostrar_informacion(self):
        return super().mostrar_informacion() + f", Carga máxima: {self.carga_maxima}"


class Tractocamion(Vehiculo):
    def __init__(self, marca, modelo, precio, tipo_pintura, unidades_disponibles, potencia_motor):
        super().__init__(marca, modelo, precio, tipo_pintura, unidades_disponibles)
        self.potencia_motor = potencia_motor

    def mostrar_informacion(self):
        return super().mostrar_informacion() + f", Potencia del motor: {self.potencia_motor} HP"


class Modelo:
    def __init__(self, nombre, descripcion):
        self.nombre = nombre
        self.descripcion = descripcion


class TipoPintura:
    def __init__(self, color, tipo):
        self.color = color
        self.tipo = tipo


class Inventario:
    def __init__(self):
        self.vehiculos = []

    def agregar_vehiculo(self, vehiculo):
        self.vehiculos.append(vehiculo)

    def listar_vehiculos(self):
        return [vehiculo.mostrar_informacion() for vehiculo in self.vehiculos]

    def buscar_vehiculo(self, modelo):
        return [vehiculo for vehiculo in self.vehiculos if vehiculo.modelo == modelo]


class Ventas:
    def __init__(self):
        self.historial = []

    def registrar_venta(self, vehiculo, cantidad, comprador):
        fecha_venta = datetime.now()
        self.historial.append({"vehiculo": vehiculo, "cantidad": cantidad, "comprador": comprador, "fecha": fecha_venta})

    def mostrar_historial(self):
        return self.historial


class InterfazUsuario:
    def __init__(self, root):
        self.root = root
        self.root.title("Concesionario de Autos")
        self.inventario = Inventario()
        self.ventas = Ventas()
        self.crear_interfaz()

    def crear_interfaz(self):
        self.label = tk.Label(self.root, text="Bienvenido al Concesionario de Autos", font=("Arial", 14))
        self.label.pack()

        self.boton_mostrar_inventario = tk.Button(self.root, text="Mostrar Inventario", command=self.mostrar_inventario)
        self.boton_mostrar_inventario.pack()

        self.boton_vender_vehiculo = tk.Button(self.root, text="Vender Vehículo", command=self.vender_vehiculo)
        self.boton_vender_vehiculo.pack()

    def mostrar_inventario(self):
        inventario = self.inventario.listar_vehiculos()
        inventario_str = "\n".join(inventario)
        messagebox.showinfo("Inventario", inventario_str)

    def vender_vehiculo(self):
        pass


if __name__ == "__main__":
    root = tk.Tk()
    interfaz = InterfazUsuario(root)

    pintura_azul = TipoPintura("Azul", "Metálica")
    modelo_sedan = Modelo("Sedán", "Automóvil de 4 puertas")
    auto1 = Automovil("Toyota", modelo_sedan, 20000, pintura_azul, 10, 4)
    camioneta1 = Camioneta("Ford", modelo_sedan, 25000, pintura_azul, 5, "4x4")
    
    interfaz.inventario.agregar_vehiculo(auto1)
    interfaz.inventario.agregar_vehiculo(camioneta1)

    root.mainloop()
