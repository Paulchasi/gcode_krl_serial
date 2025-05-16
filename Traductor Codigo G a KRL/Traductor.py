import os
import re

# Ruta base del archivo
base_file_path = 'kuka'
dat_file_extension = '.dat'
src_file_extension = '.src'

# Ruta del archivo G-code de entrada
gcode_file_path = "hola.g"

# Función para leer y procesar líneas válidas de G-code
def process_gcode_lines(gcode_file_path):
    with open(gcode_file_path, 'r', encoding='utf-8') as file:
        gcode_lines = file.readlines()

    processed_lines = []
    for line in gcode_lines:
        line = line.strip()  # Eliminar espacios innecesarios
        line = re.sub(r'\(.*?\)', '', line)  # Eliminar comentarios entre paréntesis
        line = re.sub(r';.*', '', line)  # Eliminar comentarios después de ";"
        if line:  # Si la línea no está vacía después de limpiar
            processed_lines.append(line)
    return processed_lines

# Función para convertir líneas de G-code a KRL para el archivo .dat
def convert_gcode_to_dat(gcode_lines):
    output_lines = []

    # Añadir encabezado al archivo DAT
    output_lines.append("&ACCESS RVP")
    output_lines.append("&REL 2")
    output_lines.append("&PARAM TEMPLATE = C:\\KRC\\Roboter\\Template\\vorgabe")
    output_lines.append("&PARAM EDITMASK = *")
    output_lines.append(f"DEFDAT {base_file_path}")
    output_lines.append("EXT BAS (BAS_COMMAND :IN,REAL :IN )")
    output_lines.append("")  # Separación para mayor claridad

    # Declaraciones iniciales
    output_lines.append("DECL E6AXIS XP1={A1 -50.70,A2 -111.56,A3 119.99,A4 -7.55,A5 8.10,A6 186.79}")
    output_lines.append('DECL FDAT FP1={TOOL_NO 1,BASE_NO 2,IPO_FRAME #BASE,POINT2[] " ",TQ_STATE FALSE}')
    output_lines.append('DECL PDAT PPDAT1={VEL 100.000,ACC 100.000,APO_DIST 1.000,APO_MODE #CPTP}')
    output_lines.append("")  # Separación para mayor claridad

    # Inicializamos las variables de posición
    x, y, z = None, None, 0  # Inicializamos z con valor 0 por defecto
    position_index = 2  # Iniciar desde XP2, FP2, LCPDAT2

    # Procesar líneas de G-code
    for line in gcode_lines:
        parts = line.split()
        new_x, new_y, new_z = None, None, None

        for part in parts:
            if 'X' in part:
                new_x = float(part[1:])
            if 'Y' in part:
                new_y = float(part[1:])
            if 'Z' in part:
                new_z = float(part[1:])

        if new_x is not None:
            x = new_x
        if new_y is not None:
            y = new_y
        if new_z is not None:
            z = new_z  # Si encontramos una coordenada Z, actualizamos

        if x is not None and y is not None:
            e6pos = f"DECL E6POS XP{position_index}={{X {x:.3f},Y {y:.3f},Z {z:.3f},A 180.000,B 0.000,C 180.000}}"
            fdat = f"DECL FDAT FP{position_index}={{TOOL_NO 1,BASE_NO 2,IPO_FRAME #BASE,POINT2[] \" \",TQ_STATE FALSE}}"
            ldat = f"DECL LDAT LCPDAT{position_index}={{VEL 1.00000,ACC 100.000,APO_DIST 1.000,APO_FAC 50.0000,ORI_TYP #VAR,CIRC_TYP #BASE,JERK_FAC 50.0000}}"
            output_lines.extend([e6pos, fdat, ldat, ""])
            position_index += 1

    output_lines.append("ENDDAT")
    return output_lines

# Función para generar el archivo .src
def generate_src_file(num_movements):
    krl_code = f'''&ACCESS RVP
&REL 2
&PARAM TEMPLATE = C:\\KRC\\Roboter\\Template\\vorgabe
&PARAM EDITMASK = *
DEF {base_file_path} ( )

;FOLD INI
BAS (#INITMOV,0 )
;ENDFOLD (INI)

;FOLD STARTPOS
$BWDSTART = FALSE
PDAT_ACT = PDEFAULT
BAS(#PTP_DAT)
FDAT_ACT = {{TOOL_NO 0, BASE_NO 0, IPO_FRAME #BASE}}
BAS(#FRAMES)
;ENDFOLD

;FOLD SET DEFAULT SPEED
$VEL.CP = 0.2
BAS(#VEL_PTP,100)
BAS(#TOOL,0)
BAS(#BASE,0)
;ENDFOLD

$ADVANCE = 5

PTP $AXIS_ACT ; skip BCO quickly

; Using nominal kinematics.
$APO.CPTP = 1.000
$APO.CDIS = 1.000
$VEL.CP = 1.00000
BASE_DATA[2] = {{FRAME: X 649.89, Y -450, Z 317.17, A 0.000, B 0.000, C 0.000}}
TOOL_DATA[1] = {{FRAME: X 278.600, Y 0, Z 88.00, A 45, B 35, C 0.000}}

;FOLD PTP P1 CONT Vel=100 %% PDAT1 Tool[1] Base[2]
$BWDSTART = FALSE
PDAT_ACT = PPDAT1
FDAT_ACT = FP1
BAS(#PTP_PARAMS,100)
PTP XP1 C_PTP
;ENDFOLD
'''

    for i in range(2, num_movements + 2):
        krl_code += f'''
;FOLD LIN P{i} CONT Vel=100 %% CPDAT{i} Tool[1] Base[2]
$BWDSTART = FALSE
LDAT_ACT = LCPDAT{i}
FDAT_ACT = FP{i}
BAS(#CP_PARAMS,1)
LIN XP{i} C_DIS
;ENDFOLD
'''

    krl_code += 'END'
    return krl_code

# Procesar G-code y generar ambos archivos
gcode_lines = process_gcode_lines(gcode_file_path)
dat_lines = convert_gcode_to_dat(gcode_lines)
src_code = generate_src_file(len(gcode_lines))

# Guardar el archivo .dat
dat_file_path = f"{base_file_path}{dat_file_extension}"
with open(dat_file_path, 'w', encoding='utf-8') as file:
    file.write("\n".join(dat_lines))

# Guardar el archivo .src
src_file_path = f"{base_file_path}{src_file_extension}"
with open(src_file_path, 'w', encoding='utf-8') as file:
    file.write(src_code)

print(f"Archivos generados correctamente:\n- {dat_file_path}\n- {src_file_path}")
