import math

# FUNCIÓN SIGMOID


def sigmoid(x):
    return 1 / (1 + math.exp(-x))


# TEMPERATURA


temperatura = 8  # grados Celsius


# NORMALIZACIÓN


temp_min = 0
temp_max = 40

x = (temperatura - temp_min) / (temp_max - temp_min)



# CLASIFICACIÓN REAL ESPERADA

# 0   = FRIO
# 0.5 = CALIDO
# 1   = CALIENTE

if temperatura <= 15:
    y_real = 0

elif temperatura <= 25:
    y_real = 0.5

else:
    y_real = 1



# PARÁMETROS


w = 0.8
b = -0.5

alpha = 0.1
epocas = 40


print(f"Temperatura: {temperatura}°C")
print(f"Valor normalizado: {round(x,4)}")
print("-" * 60)



# ENTRENAMIENTO


for epoca in range(epocas):

    # FORWARD PASS
    net = (w * x) + b

    y_pred = sigmoid(net)


    # ERROR
    error = y_real - y_pred


    # LOSS
    L = 0.5 * (error ** 2)



    # BACKPROPAGATION


    dL_dypred = y_pred - y_real

    dypred_dnet = y_pred * (1 - y_pred)

    dnet_dw = x

    dL_dw = dL_dypred * dypred_dnet * dnet_dw

    dL_db = dL_dypred * dypred_dnet


    # ACTUALIZAR PESOS


    w = w - (alpha * dL_dw)

    b = b - (alpha * dL_db)



    # CLASIFICACIÓN


    if y_pred < 0.35:
        categoria = "FRIO"

    elif y_pred < 0.65:
        categoria = "CALIDO"

    else:
        categoria = "CALIENTE"


    print(
        f"Epoca {epoca+1} | "
        f"pred: {round(y_pred,4)} | "
        f"error: {round(error,4)} | "
        f"loss: {round(L,4)} | "
        f"{categoria}"
    )


# RESULTADO FINAL


print("-" * 60)

print(f"Resultado final: {temperatura}°C es {categoria}")

print(f"Peso final: {round(w,4)}")
print(f"Bias final: {round(b,4)}")