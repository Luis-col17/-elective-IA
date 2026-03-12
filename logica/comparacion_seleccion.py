from random import choice
notas = [3.0, 5.0, 8.0, 8.5, 9.0, 10.0]
estrato = [1,2,3]

for i in range(len(notas)):
    for j in range(len(estrato)):
        elegido = (notas[i] >= 9.0) or (notas[i] >= 8.0 and estrato[j] <= 2) 
        print("es elegible para beca: ", elegido)