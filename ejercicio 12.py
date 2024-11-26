import numpy as np

def obtener_codigo_estudiante():
    """
    Función que solicita al usuario su código de estudiante y lo valida.
    Debe ser un código de exactamente 8 dígitos numéricos.
    """
    codigo = input("Ingrese su código de estudiante (8 dígitos): ")
    while len(codigo) != 8 or not codigo.isdigit():
        print("El código debe tener 8 dígitos numéricos.")
        codigo = input("Ingrese su código de estudiante (8 dígitos): ")
    return codigo

def calcular_resistencias(codigo):
    """
    Función que calcula las resistencias R1, R2, R3, R4 y R5 basadas en las cifras del código de estudiante.
    Si alguna resistencia suma 0, la reemplaza por 10 ohmios.
    """
    R1 = sum(int(codigo[i]) for i in range(3))  
    R2 = sum(int(codigo[i]) for i in range(1, 4))  
    R3 = sum(int(codigo[i]) for i in range(2, 4)) 
    R4 = sum(int(codigo[i]) for i in range(4, 6))  
    R5 = sum(int(codigo[i]) for i in range(5, 8))  

    resistencias = [R1, R2, R3, R4, R5]
    resistencias = [r if r != 0 else 10 for r in resistencias]

    return resistencias

def resolver_circuito(resistencias):
    """
    Función que resuelve el sistema de ecuaciones del circuito utilizando matrices.
    Utiliza la matriz A y el vector b para resolver el sistema Ax = b.
    """
    A = np.array([
        [resistencias[0], -resistencias[1], 0, 0],
        [-resistencias[1], resistencias[1] + resistencias[2], -resistencias[3], 0],
        [0, -resistencias[2], resistencias[2] + resistencias[3], -resistencias[4]],
        [0, 0, -resistencias[3], resistencias[3] + resistencias[4]]
    ])

    Vb = 10  
    b = np.array([Vb, 0, 0, 0])

    x = np.linalg.solve(A, b)
    
    return x

def main():
    """
    Función principal que ejecuta el programa.
    Solicita el código de estudiante, calcula las resistencias y resuelve el circuito.
    """
    codigo = obtener_codigo_estudiante()  
    resistencias = calcular_resistencias(codigo) 
    print(f"Resistencias calculadas: R1 = {resistencias[0]} ohmios, R2 = {resistencias[1]} ohmios, "
          f"R3 = {resistencias[2]} ohmios, R4 = {resistencias[3]} ohmios, R5 = {resistencias[4]} ohmios")
    
    soluciones = resolver_circuito(resistencias)  
    print(f"Soluciones del circuito: {soluciones}")

if __name__ == "__main__":
    main()
