import pandas as pd
import re

class Agenda:
    def __init__(self, archivo_csv='Archivos/agenda_POO.csv'):
        self.archivo_csv = archivo_csv
        try:
            self.df = pd.read_csv(self.archivo_csv)
        except FileNotFoundError:
            self.df = pd.DataFrame(columns=['Nombre', 'Correo', 'Telefono'])
            self.df.to_csv(self.archivo_csv, index=False)

        self.menu()

    def Correo_valido(self):
        while True:
            correo = input("Ingrese su correo electrónico: ")
            if re.match(r"[^@]+@[^@]+\.[^@]+", correo):
                self.correo = correo
                break
            else:
                print("!!!CORREO NO VALIDO!!! Ingrese un username seguido de una arroba (@) y termine con un dominio (por ejemplo, .com)")

    def Telefono_valido(self):
        while True:
            try:
                telefono = int(input('Ingrese su telefono: '))
                telefono = str(telefono)
                if len(telefono) != 10:
                    print('!!!TELEFONO INVALIDO!!! Digite un telefono valido')
                else: 
                    self.telefono = telefono
                    break
            except ValueError:
                print('!!!TELEFONO INVALIDO!!! Digite un telefono valido')

    def Agregar(self):
        nombre = input("Ingresa su nombre: ")
        self.Correo_valido()
        self.Telefono_valido()

        nuevo_dato = pd.DataFrame({'Nombre': [nombre], 'Correo': [self.correo], 'Telefono': [self.telefono]})
        self.df = pd.concat([self.df, nuevo_dato], ignore_index=True)
        self.df.to_csv(self.archivo_csv, index=False)

        print(f"Datos guardados correctamente en {self.archivo_csv}")
        print(self.df)

    def Mostrar(self):
        nombre = input("Ingrese el nombre del contacto que desea mostrar: ")
        contacto = self.df[self.df['Nombre'] == nombre]
        if not contacto.empty:
            print(contacto)
        else:
            print(f"No se encontró el contacto con el nombre {nombre}.")
    
    def Lista(self):
        print(self.df)
    
    def Eliminar(self):
        nombre = input("Ingrese el nombre del contacto que desea eliminar: ")
        if nombre in self.df['Nombre'].values:
            self.df = self.df[self.df['Nombre'] != nombre]
            self.df.to_csv(self.archivo_csv, index=False)
            print(f"Contacto {nombre} eliminado.")
        else:
            print(f"No se encontró el contacto con el nombre {nombre}.")

    def Editar(self):
        nombre = input("Ingrese el nombre del contacto que desea editar: ")
        if nombre in self.df['Nombre'].values:
            nuevo_nombre = input("Ingrese el nuevo nombre: ")
            self.Correo_valido()
            self.Telefono_valido()
            self.df.loc[self.df['Nombre'] == nombre, ['Nombre', 'Correo', 'Telefono']] = [nuevo_nombre, self.correo, self.telefono]
            self.df.to_csv(self.archivo_csv, index=False)
            print(f"Contacto {nombre} editado.")
        else:
            print(f"No se encontró el contacto con el nombre {nombre}.") 

    def menu(self):
        while True:
            print("\nMenu:")
            print("\t1. Agregar contacto")
            print("\t2. Mostrar contacto")
            print("\t3. Lista de contactos")
            print("\t4. Eliminar contactos")
            print("\t5. Editar contactos")
            print("\t6. Salir")
            op = input("Seleccione una opción: ")
            if op == '1':
                self.Agregar()
            elif op == '2':
                self.Mostrar()
            elif op == '3':
                self.Lista()
            elif op == '4':
                self.Eliminar()
            elif op == '5':
                self.Editar()
            elif op == '6':
                exit()
            else:
                print("Opción no válida. Por favor, intente nuevamente.")

while True:
    agenda = Agenda()
