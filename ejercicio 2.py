class ConvertirARomano:
    def __init__(self, numero_entero):
        self.numero_entero = numero_entero
        self.romanos = [
            ('M', 1000),
            ('CM', 900),
            ('D', 500),
            ('CD', 400),
            ('C', 100),
            ('XC', 90),
            ('L', 50),
            ('XL', 40),
            ('X', 10),
            ('IX', 9),
            ('V', 5),
            ('IV', 4),
            ('I', 1)
        ]
    
    def convertir(self):
        numero = self.numero_entero
        romano = ''
        for simbolo, valor in self.romanos:
            while numero >= valor:
                romano += simbolo
                numero -= valor
        return romano


class ConvertirAEntero:
    def __init__(self, numero_romano):
        self.numero_romano = numero_romano
        self.romanos = {
            'M': 1000,
            'CM': 900,
            'D': 500,
            'CD': 400,
            'C': 100,
            'XC': 90,
            'L': 50,
            'XL': 40,
            'X': 10,
            'IX': 9,
            'V': 5,
            'IV': 4,
            'I': 1
        }
    
    def convertir(self):
        romano = self.numero_romano
        numero = 0
        i = 0
        while i < len(romano):
            if i + 1 < len(romano) and romano[i:i+2] in self.romanos:
                numero += self.romanos[romano[i:i+2]]
                i += 2
            else:
                numero += self.romanos[romano[i]]
                i += 1
        return numero


def menu():
    while True:
        print("Seleccione una opción:")
        print("1. Convertir número entero a número romano")
        print("2. Convertir número romano a número entero")
        print("3. Salir")
        
        opcion = input("Ingrese la opción deseada: ")
        
        if opcion == '1':
            numero = int(input("Ingrese un número entero: "))
            convertidor = ConvertirARomano(numero)
            print(f"El número romano es: {convertidor.convertir()}")
        
        elif opcion == '2':
            numero_romano = input("Ingrese un número romano: ").upper()
            convertidor = ConvertirAEntero(numero_romano)
            print(f"El número entero es: {convertidor.convertir()}")
        
        elif opcion == '3':
            print("Saliendo del programa.")
            break
        else:
            print("Opción no válida, por favor intente de nuevo.")

menu()
