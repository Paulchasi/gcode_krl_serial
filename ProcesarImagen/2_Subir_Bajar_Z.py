import re

def modificar_codigo_g(codigo_g, escala_x, escala_y):
    """
    Modifica el código G:
    1. Si las primeras dos líneas son 'G21' y 'G90;svg > path', las elimina.
    2. Agrega G0 Z5 antes de cada G0 original.
    3. Agrega G0 con Z0 después de cada G0 original.
    4. Reescala las coordenadas X y Y según las escalas proporcionadas.
    5. Elimina cualquier valor de velocidad 'F' en las líneas (como F300).
    6. Si no existe 'G0 X0 Y0 Z30', lo añade **al inicio y al final** del archivo.
    """
    lineas = codigo_g.strip().split("\n")

    # 1. Eliminar las primeras dos líneas si son 'G21' y 'G90;svg > path'
    if len(lineas) >= 2 and lineas[0].strip() == "G21" and "G90;svg > path" in lineas[1]:
        lineas = lineas[2:]

    nuevo_codigo = []
    primera_linea = "G0 X0 Y0 Z30"
    ultima_linea = "G0 Z30"
    primera_linea_presente = False
    ultima_linea_presente = False

    for linea in lineas:
        # 5. Eliminar valores de velocidad 'F' en cualquier parte de la línea
        linea = re.sub(r"\s*F\d+(\.\d+)?", "", linea).strip()

        if linea.startswith("G0") or linea.startswith("G1"):  
            partes = linea.split()
            nueva_linea = []
            
            for parte in partes:
                if parte.startswith("X"):
                    valor_x = float(parte[1:])
                    nueva_x = valor_x * escala_x
                    nueva_linea.append(f"X{nueva_x:.6f}")
                elif parte.startswith("Y"):
                    valor_y = float(parte[1:])
                    nueva_y = valor_y * escala_y
                    nueva_linea.append(f"Y{nueva_y:.6f}")
                elif parte.startswith("Z"):
                    nueva_linea.append(parte)  
                else:
                    nueva_linea.append(parte)  

            nueva_linea_str = " ".join(nueva_linea)
            
            if linea.startswith("G0"):  
                coordenadas = " ".join(parte for parte in nueva_linea if parte.startswith(("X", "Y")))
                nuevo_codigo.append("G0 Z5")  
                nuevo_codigo.append(nueva_linea_str)  
                nuevo_codigo.append(f"G0 {coordenadas} Z0")  
            else:
                nuevo_codigo.append(nueva_linea_str)  
        else:
            nuevo_codigo.append(linea)  

        # Verificar si "G0 X0 Y0 Z30" ya está en el código
        if linea.strip() == primera_linea:
            primera_linea_presente = True

    # 6. Si la línea "G0 X0 Y0 Z30" no está, se agrega **al inicio y al final**
    if not primera_linea_presente:
        nuevo_codigo.insert(0, primera_linea)  # Agrega la línea al inicio

    if nuevo_codigo[-1].strip() != primera_linea:
        nuevo_codigo.append(ultima_linea)  # Agrega la línea al final
    
    return "\n".join(nuevo_codigo)


# 🔧 **Configuración de escalas**
tamano_original_x = 160.0  
tamano_nuevo_x = 550.0  
escala_x = tamano_nuevo_x / tamano_original_x

tamano_original_y = 160.0  
tamano_nuevo_y = 700.0  
escala_y = tamano_nuevo_y / tamano_original_y

# 📂 **Leer archivo G-Code**
with open("archivo.gcode", "r") as archivo:
    codigo_g_original = archivo.read()

# 🛠️ **Aplicar modificaciones**
codigo_g_modificado = modificar_codigo_g(codigo_g_original, escala_x=escala_x, escala_y=escala_y)

# 💾 **Guardar archivo modificado**
with open("modificado.gcode", "w") as archivo:
    archivo.write(codigo_g_modificado)

print(f"✅ Archivo modificado y escalado a {tamano_nuevo_x}x{tamano_nuevo_y} mm. Guardado como 'modificado.gcode'.")
