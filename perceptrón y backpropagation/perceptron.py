# SISTEMA SIMPLE DE ACEPTACIÓN DE BECAS

# Entradas del estudiante
# 1 = Sí cumple
# 0 = No cumple

x1 = 1   # Buenas notas
x2 = 1   # Actividad deportiva
x3 = 0   # Participación social


# Importancia de cada característica
w1 = 0.6   # Las notas tienen alta importancia
w2 = 0.8   # El deporte tiene importancia media
w3 = 0.1   # Lo social tiene importancia baja


# Requisito mínimo 
b = -0.4



# SUMA PONDERADA
net = (x1 * w1) + (x2 * w2) + (x3 * w3) + b

print("Resultado net:", round(net, 5))

# FUNCIÓN DE ACTIVACIÓN

if net >= 0:
    salida = 1
    decision = "Probable aceptación a la beca"
else:
    salida = 0
    decision = "Poca probabilidad de aceptación"


print("Salida:", salida)
print("Decisión:", decision)