import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from abc import ABC, abstractmethod


class FiguraGeometrica():
    def __init__(self, nombre):
        self.nombre = nombre
    
    @abstractmethod
    def calcular_area(self):
        pass
    
    @abstractmethod
    def calcular_perimetro(self):
        pass
    
    def mostrar_info(self):
        area = self.calcular_area()
        perimetro = self.calcular_perimetro()
        return f"Figura: {self.nombre}, Área: {area:.2f}, Perímetro: {perimetro:.2f}"



class Triangulo():
    def __init__(self, base, altura, lado1, lado2, lado3):
        super().__init__("Triángulo")
        self.base = base
        self.altura = altura
        self.lado1 = lado1
        self.lado2 = lado2
        self.lado3 = lado3
    
    def calcular_area(self):
        return 0.5 * self.base * self.altura
    
    def calcular_perimetro(self):
        return self.lado1 + self.lado2 + self.lado3

class Circunferencia():
    def __init__(self, radio):
        super().__init__("Circunferencia")
        self.radio = radio
    
    def calcular_area(self):
        return math.pi * (self.radio ** 2)
    
    def calcular_perimetro(self):
        return 2 * math.pi * self.radio

class Cuadrado(FiguraGeometrica):
    def __init__(self, lado):
        super().__init__("Cuadrado")
        self.lado = lado
    
    def calcular_area(self):
        return self.lado ** 2
    
    def calcular_perimetro(self):
        return 4 * self.lado

class Rectangulo():
    def __init__(self, largo, ancho):
        super().__init__("Rectángulo")
        self.largo = largo
        self.ancho = ancho
    
    def calcular_area(self):
        return self.largo * self.ancho
    
    def calcular_perimetro(self):
        return 2 * (self.largo + self.ancho)

class Paralelogramo():
    def __init__(self, base, altura, lado1, lado2):
        super().__init__("Paralelogramo")
        self.base = base
        self.altura = altura
        self.lado1 = lado1
        self.lado2 = lado2
    
    def calcular_area(self):
        return self.base * self.altura
    
    def calcular_perimetro(self):
        return 2 * (self.lado1 + self.lado2)

class Trapecio():
    def __init__(self, base_mayor, base_menor, altura, lado1, lado2):
        super().__init__("Trapecio")
        self.base_mayor = base_mayor
        self.base_menor = base_menor
        self.altura = altura
        self.lado1 = lado1
        self.lado2 = lado2
    
    def calcular_area(self):
        return 0.5 * (self.base_mayor + self.base_menor) * self.altura
    
    def calcular_perimetro(self):
        return self.base_mayor + self.base_menor + self.lado1 + self.lado2

class Rombo():
    def __init__(self, diagonal_mayor, diagonal_menor, lado):
        super().__init__("Rombo")
        self.diagonal_mayor = diagonal_mayor
        self.diagonal_menor = diagonal_menor
        self.lado = lado
    
    def calcular_area(self):
        return 0.5 * self.diagonal_mayor * self.diagonal_menor
    
    def calcular_perimetro(self):
        return 4 * self.lado

def ingresar_figura():
    print("Seleccione el tipo de figura:")
    print("1. Triángulo")
    print("2. Circunferencia")
    print("3. Cuadrado")
    print("4. Rectángulo")
    print("5. Paralelogramo")
    print("6. Trapecio")
    print("7. Rombo")
    
    opcion = input("Ingrese el número de la figura: ")
    
    if opcion == '1':
        base = float(input("Ingrese la base del triángulo: "))
        altura = float(input("Ingrese la altura del triángulo: "))
        lado1 = float(input("Ingrese el primer lado: "))
        lado2 = float(input("Ingrese el segundo lado: "))
        lado3 = float(input("Ingrese el tercer lado: "))
        figura = Triangulo(base, altura, lado1, lado2, lado3)

    elif opcion == '2':
        radio = float(input("Ingrese el radio de la circunferencia: "))
        figura = Circunferencia()

    elif opcion == '3':
        lado = float(input("Ingrese el lado del cuadrado: "))
        figura = Cuadrado()

    elif opcion == '4':
        largo = float(input("Ingrese el largo del rectángulo: "))
        ancho = float(input("Ingrese el ancho del rectángulo: "))
        figura = Rectangulo()

    elif opcion == '5':
        base = float(input("Ingrese la base del paralelogramo: "))
        altura = float(input("Ingrese la altura del paralelogramo: "))
        lado1 = float(input("Ingrese el primer lado: "))
        lado2 = float(input("Ingrese el segundo lado: "))
        figura = Paralelogramo()

    elif opcion == '6':
        base_mayor = float(input("Ingrese la base mayor del trapecio: "))
        base_menor = float(input("Ingrese la base menor del trapecio: "))
        altura = float(input("Ingrese la altura del trapecio: "))
        lado1 = float(input("Ingrese el primer lado: "))
        lado2 = float(input("Ingrese el segundo lado: "))
        figura = Trapecio()

    elif opcion == '7':
        diagonal_mayor = float(input("Ingrese la diagonal mayor del rombo: "))
        diagonal_menor = float(input("Ingrese la diagonal menor del rombo: "))
        lado = float(input("Ingrese el lado del rombo: "))
        figura = Rombo(diagonal_mayor, diagonal_menor, lado)
    
    return figura

figura = ingresar_figura()
print(figura.mostrar_info())
