import cv2
import numpy as np
import matplotlib.pyplot as plt

# Cargar la imagen
imagen = cv2.imread('imagen_original.jpg')
gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)

# Suavizado para reducir ruido
gris = cv2.GaussianBlur(gris, (9, 9), 0)

# Detectar bordes
bordes = cv2.Canny(gris, 20, 50, apertureSize=3)

# Invertir colores (blanco -> negro, negro -> blanco)
bordes_invertidos = cv2.bitwise_not(bordes)

# Guardar la imagen con bordes invertidos
cv2.imwrite('imagen_borders.jpg', bordes_invertidos)