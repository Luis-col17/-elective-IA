# Solver de Sudoku como CSP

## ¿Qué es un CSP?

Un **CSP (Constraint Satisfaction Problem)** es un problema donde hay variables, cada una con un dominio de valores posibles, y restricciones que limitan qué combinaciones son válidas.

En el Sudoku:
- **Variables** → las celdas vacías
- **Dominio** → los números del 1 al 9
- **Restricciones** → no repetir números en la misma fila, columna ni bloque 3×3

---

## Estructura general del código

```
PUZZLE INICIAL
     ↓
Herramientas (mostrar, copiar, calcular restricciones)
     ↓
Algoritmo 1: Backtracking simple
     ↓
Algoritmo 2: Backtracking + MRV
     ↓
Comparación de rendimiento
```

---

## El puzzle

```python
SUDOKU_EJEMPLO = [
    [5, 3, 0,  0, 7, 0,  0, 0, 0],
    ...
]
```

El tablero es una lista de 9 listas (filas). El `0` representa una celda vacía que hay que resolver.

---

## Herramientas base

### `mostrar_tablero`

Imprime el tablero con separadores visuales entre los bloques 3×3.

```python
if i % 3 == 0 and i != 0:
    print("  ------+-------+------")
```

`i % 3 == 0` usa el operador módulo: pregunta si `i` es múltiplo de 3. Con `i != 0` se asegura de no imprimir la línea al inicio. Esto dibuja los separadores antes de las filas 3 y 6.

---

### `copiar_tablero`

```python
def copiar_tablero(tablero):
    return [fila[:] for fila in tablero]
```

Hace una copia completamente independiente del tablero. `fila[:]` copia cada lista de números. Sin esto, los tres algoritmos modificarían el mismo objeto en memoria y los resultados se contaminarían entre sí.

---

### `valores_usados`

```python
def valores_usados(tablero, fila, col):
    usados = set()
    usados.update(tablero[fila])                              # restricción de fila
    usados.update(tablero[f][col] for f in range(9))         # restricción de columna
    bf = (fila // 3) * 3
    bc = (col // 3) * 3
    for r in range(bf, bf + 3):
        for c in range(bc, bc + 3):
            usados.add(tablero[r][c])                        # restricción de bloque
    usados.discard(0)
    return usados
```

Devuelve el conjunto de números **prohibidos** para una celda. Usa `set` para evitar duplicados automáticamente.

**Restricción de fila:** agrega todos los valores de esa fila.

**Restricción de columna:** recorre las 9 filas tomando solo el elemento en la posición `col`. Es como bajar verticalmente por esa columna.

**Restricción de bloque 3×3:** primero calcula la esquina superior izquierda del bloque:

```
bf = (fila // 3) * 3
```

El truco de `// 3 * 3` convierte cualquier número en el múltiplo de 3 más cercano hacia abajo:

```
fila 0,1,2  →  bf = 0   (bloque superior)
fila 3,4,5  →  bf = 3   (bloque del medio)
fila 6,7,8  →  bf = 6   (bloque inferior)
```

Luego el doble `for` recorre las 9 celdas de ese bloque.

Finalmente `usados.discard(0)` elimina el cero porque no es un valor real.

---

### `valores_validos`

```python
def valores_validos(tablero, fila, col):
    return [v for v in range(1, 10) if v not in valores_usados(tablero, fila, col)]
```

Del 1 al 9, devuelve solo los que **no** están prohibidos. Es una comprensión de lista, equivalente a:

```python
resultado = []
for v in range(1, 10):
    if v not in valores_usados(tablero, fila, col):
        resultado.append(v)
return resultado
```

---

## Algoritmo 1 — Backtracking simple

### Selección de celda

```python
def celda_siguiente_simple(tablero):
    for i in range(9):
        for j in range(9):
            if tablero[i][j] == 0:
                return (i, j)
    return None
```

Toma la **primera celda vacía** que encuentra, recorriendo de izquierda a derecha y de arriba a abajo.

### Resolución

```python
def backtrack_simple(tablero):
    celda = celda_siguiente_simple(tablero)
    if celda is None:
        return tablero          # todas las celdas asignadas → solución

    fila, col = celda
    for valor in range(1, 10):
        if valor not in valores_usados(tablero, fila, col):
            tablero[fila][col] = valor          # asignar
            resultado = backtrack_simple(tablero)
            if resultado:
                return resultado
            tablero[fila][col] = 0              # ← backtrack
    return None
```

El funcionamiento es:

1. Busca la primera celda vacía.
2. Prueba los números del 1 al 9 en orden.
3. Para cada número válido, lo escribe en la celda y **se llama a sí mismo** (recursión) para intentar resolver el resto.
4. Si la llamada recursiva falla, borra el número (`= 0`) y prueba el siguiente. Esto es el **backtrack**.
5. Si ningún número funciona, devuelve `None` para indicar fallo.

---

## Algoritmo 2 — Backtracking con MRV

### ¿Qué es MRV?

**MRV = Minimum Remaining Values.** En vez de tomar la primera celda vacía, elige siempre la celda con **menos opciones posibles**. Esto reduce drásticamente los caminos incorrectos.

### Selección de celda con MRV

```python
def celda_siguiente_mrv(tablero):
    mejor_celda = None
    mejor_cant = 10         # más grande que el máximo posible (9)

    for i in range(9):
        for j in range(9):
            if tablero[i][j] == 0:
                cant = len(valores_validos(tablero, i, j))
                if cant < mejor_cant:
                    mejor_cant = cant
                    mejor_celda = (i, j)
                    if cant == 1:
                        return mejor_celda    # imposible encontrar algo mejor
    return mejor_celda
```

Recorre todas las celdas vacías calculando cuántas opciones tiene cada una. Se queda con la que tenga menos. El `10` inicial es un truco para que cualquier celda gane la primera comparación.

Si encuentra una celda con solo 1 opción, retorna inmediatamente sin seguir buscando.

### Resolución con MRV

```python
def backtrack_mrv(tablero):
    celda = celda_siguiente_mrv(tablero)
    if celda is None:
        return tablero

    fila, col = celda
    candidatos = valores_validos(tablero, fila, col)

    if not candidatos:
        return None             # poda anticipada: ya no hay opciones

    for valor in candidatos:
        tablero[fila][col] = valor
        resultado = backtrack_mrv(tablero)
        if resultado:
            return resultado
        tablero[fila][col] = 0  # ← backtrack

    return None
```

Igual que el simple, pero con dos mejoras:

- Usa `celda_siguiente_mrv` en vez de `celda_siguiente_simple`.
- Si `candidatos` está vacío, falla de inmediato sin intentar nada (**poda anticipada**).

---

## ¿Por qué MRV es más eficiente?

Imagina estas dos celdas vacías:

```
Celda A → puede ser: 1, 2, 3, 4, 5   (5 opciones)
Celda B → puede ser: 7                (1 opción)
```

El algoritmo simple elegiría A y probaría hasta 5 valores antes de quizás fallar. MRV elegiría B primero — ya sabe que es el 7 — y avanza sin arriesgarse a equivocarse.

---

## El bloque principal

```python
if __name__ == "__main__":
```

Todo lo que está dentro de este bloque solo se ejecuta cuando corres el archivo directamente (no cuando lo importas desde otro script).

El bloque:

1. Muestra el puzzle inicial.
2. Crea una **copia independiente** del tablero para cada algoritmo.
3. Mide el tiempo con `time.perf_counter()` antes y después de cada ejecución.
4. Imprime los resultados y compara llamadas recursivas y tiempo.

---

## Comparación de rendimiento

```python
reduccion = (1 - llamadas_con_mrv / llamadas_sin_mrv) * 100
```

Calcula en porcentaje cuántas llamadas recursivas MRV evitó en comparación con el algoritmo simple. A mayor porcentaje, más eficiente fue MRV.

---

## Resumen visual

```
Puzzle inicial
      │
      ├── Backtracking simple
      │      Primera celda vacía
      │      Prueba 1→9 en orden
      │      Muchas llamadas recursivas
      │
      └── Backtracking + MRV
             Celda con menos opciones
             Prueba solo candidatos válidos
             Muchas menos llamadas recursivas
```

| Concepto | Descripción |
|---|---|
| `set()` | Colección sin duplicados, ideal para valores prohibidos |
| `//` | División entera, descarta decimales |
| `%` | Módulo, devuelve el residuo de la división |
| `fila[:]` | Copia una lista completa |
| Recursión | La función se llama a sí misma para resolver el subproblema |
| Backtrack | Borra un valor incorrecto y prueba el siguiente |
| MRV | Elige primero la celda con menos opciones disponibles |
