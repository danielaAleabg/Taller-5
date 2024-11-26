import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sqlite3
from tkinter import Tk, Label, Button
from sympy import symbols, Eq, solve

class Resistencia:
    def __init__(self, valor):
        self._valor = valor  
    @property
    def valor(self):
        return self._valor

    @valor.setter
    def valor(self, nuevo_valor):
        if nuevo_valor > 0:
            self._valor = nuevo_valor
        else:
            raise ValueError("El valor de la resistencia debe ser positivo.")

    def calcular_resistencia_total(self):
        raise NotImplementedError("Este método debe ser implementado por la clase derivada.")

class ResistenciaSerie(Resistencia):
    def __init__(self, resistencias):
        super().__init__(None)
        self.resistencias = resistencias 

    def calcular_resistencia_total(self):
        return sum([r.valor for r in self.resistencias])


class ResistenciaParalela(Resistencia):
    def __init__(self, resistencias):
        super().__init__(None)
        self.resistencias = resistencias  

    def calcular_resistencia_total(self):
        inverso = sum([1 / r.valor for r in self.resistencias])
        return 1 / inverso if inverso != 0 else float('inf')

def mostrar_resultado():
    r1 = Resistencia(10)
    r2 = Resistencia(20)
    r3 = Resistencia(30)

    circuito_serie = ResistenciaSerie([r1, r2, r3])
    resultado_serie = circuito_serie.calcular_resistencia_total()

    circuito_paralelo = ResistenciaParalela([r1, r2, r3])
    resultado_paralelo = circuito_paralelo.calcular_resistencia_total
    print(f"Resistencia total en Serie: {resultado_serie} Ohm")
    print(f"Resistencia total en Paralelo: {resultado_paralelo} Ohm")


    conn = sqlite3.connect('circuitos.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS resultados (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        tipo_circuito TEXT,
                        resistencia_total REAL)''')
    cursor.execute('''INSERT INTO resultados (tipo_circuito, resistencia_total)
                        VALUES (?, ?)''', ('Serie', resultado_serie))
    cursor.execute('''INSERT INTO resultados (tipo_circuito, resistencia_total)
                        VALUES (?, ?)''', ('Paralelo', resultado_paralelo))
    conn.commit()
    conn.close()

def graficar_resistencia():
    tipos = ['Serie', 'Paralelo']
    resistencias = [15, 7.5]  
    plt.bar(tipos, resistencias, color=['blue', 'red'])
    plt.xlabel('Tipo de Circuito')
    plt.ylabel('Resistencia Total (Ohm)')
    plt.title('Resistencia Total en Circuitos Serie y Paralelo')
    plt.show()

def mostrar_interfaz():
    window = Tk()
    window.title("Cálculo de Resistencia Total")

    label = Label(window, text="Calculadora de Resistencia Total en Circuitos", font=("Arial", 16))
    label.pack(pady=20)

    button_calcular = Button(window, text="Calcular Resistencia", command=mostrar_resultado)
    button_calcular.pack(pady=10)

    button_graficar = Button(window, text="Graficar Resultados", command=graficar_resistencia)
    button_graficar.pack(pady=10)

    window.mainloop()

mostrar_interfaz()
