import re

def extract_kuka_positions_as_text(file_path):
    """
    Extrae las posiciones angulares (A) y cartesianas (X) de un archivo KRL y 
    las guarda como una lista de cadenas en formato de texto.

    Args:
        file_path (str): Ruta del archivo KRL.

    Returns:
        tuple: Lista de cadenas para las posiciones angulares (A) y lista de cadenas para las posiciones cartesianas (X).
    """
    angular_positions = []
    cartesian_positions = []

    # Expresión regular para posiciones angulares (A1, A2, A3, A4, A5, A6)
    angular_pattern = re.compile(r'XP1=\{A1\s*(-?\d+\.?\d*),A2\s*(-?\d+\.?\d*),A3\s*(-?\d+\.?\d*),A4\s*(-?\d+\.?\d*),A5\s*(-?\d+\.?\d*),A6\s*(-?\d+\.?\d*)\}')
    
    # Expresión regular para posiciones cartesianas (X, Y, Z, A, B, C)
    cartesian_pattern = re.compile(r'XP\d+=\{X\s*(-?\d+\.?\d*),Y\s*(-?\d+\.?\d*),Z\s*(-?\d+\.?\d*),A\s*(-?\d+\.?\d*),B\s*(-?\d+\.?\d*),C\s*(-?\d+\.?\d*)\}')

    try:
        with open(file_path, 'r') as file:
            for line in file:
                # Buscar y procesar posiciones angulares
                angular_match = angular_pattern.search(line)
                if angular_match:
                    angular_values = list(map(float, angular_match.groups()))
                    angular_values.append(sum(angular_values))  # Añadir la suma al final
                    angular_positions.append(" ".join(map(str, angular_values)))  # Guardar como texto
                
                # Buscar y procesar posiciones cartesianas
                cartesian_match = cartesian_pattern.search(line)
                if cartesian_match:
                    cartesian_values = list(map(float, cartesian_match.groups()))
                    cartesian_values.append(sum(cartesian_values))  # Añadir la suma al final
                    cartesian_positions.append(" ".join(map(str, cartesian_values)))  # Guardar como texto
    except FileNotFoundError:
        print(f"Error: El archivo {file_path} no existe.")
    except Exception as e:
        print(f"Error al procesar el archivo: {e}")

    return angular_positions, cartesian_positions


# Ejemplo de uso
file_path = "kuka.dat"  # Cambia esto por la ruta de tu archivo KRL
A, X = extract_kuka_positions_as_text(file_path)

# Mostrar resultados
if A:
    print("Posiciones Angulares (A):")
    print(f"A = {A}")
else:
    print("No se encontraron posiciones angulares.")

if X:
    print("Posiciones Cartesianas (X):")
    print(f"X = {X}")
else:
    print("No se encontraron posiciones cartesianas.")



import serial

# Configuración del puerto serie
ser = serial.Serial(
    port='COM3',        # Puerto COM3
    baudrate=9600,      # Velocidad en baudios
    bytesize=serial.EIGHTBITS,  # 8 bits de datos
    parity=serial.PARITY_EVEN,  # Paridad par
    stopbits=serial.STOPBITS_ONE,  # 1 bit de parada       
    timeout=0.1 
)

# Verificar si el puerto está abierto
if not ser.is_open:
    ser.open()



print("Iniciando comunicación con el robot...")

import time

try:
    for item in X:
        # Enviar el elemento al robot
        mensaje = f"{item}\n"
        ser.write(mensaje.encode('ascii'))  # Enviar el mensaje en formato ASCII
        print(f"Enviado: {mensaje.strip()}")

        # Leer la respuesta del robot
        max_espera = 15  # Tiempo máximo de espera en segundos
        inicio_espera = time.time()

        while True:
            if ser.in_waiting > 0:  # Verifica si hay datos disponibles para leer
                raw_data = ser.readline()  # Leer datos en bruto
                respuesta = raw_data.decode('ascii').strip()  # Decodificar la respuesta
                print(f"Respuesta del robot (cruda): {raw_data}")
                print(f"Respuesta del robot: {respuesta}")
                break
            
            # Verifica si el tiempo de espera ha excedido
            if time.time() - inicio_espera > max_espera:
                print("Error: Tiempo de espera agotado. El robot no respondió.")
                break

    # Finalizar la comunicación
    print("Comunicación completada.")

except Exception as e:
    print(f"Error durante la comunicación: {e}")

finally:
    # Cerrar el puerto serie
    ser.close()
    print("Puerto serie cerrado.")


