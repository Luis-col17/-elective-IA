# Solución de Sudoku como CSP (Constraint Satisfaction Problem)

## ¿Qué es un CSP?

Un **Problema de Satisfacción de Restricciones** (CSP, por sus siglas en inglés) es un tipo de problema en inteligencia artificial donde se deben asignar valores a un conjunto de variables, respetando un conjunto de restricciones. El Sudoku es un ejemplo clásico:

- **Variables**: cada celda vacía del tablero (81 celdas en total).
- **Dominio**: los valores posibles para cada variable (dígitos del 1 al 9).
- **Restricciones**: ningún número puede repetirse en la misma fila, columna o subcuadro de 3×3.

---

## Estructura del código

### 1. Tablero inicial

```python
SUDOKU_EJEMPLO = [
    [5, 3, 0,  0, 7, 0,  0, 0, 0],
    ...
]
```

El puzzle se representa como una lista de listas de 9×9. Los ceros (`0`) indican las celdas vacías que el algoritmo debe completar.

---

### 2. Funciones auxiliares

#### `mostrar_tablero(tablero, titulo)`
Imprime el tablero en consola con formato legible, separando los subcuadros con líneas verticales y horizontales.

#### `copiar_tablero(tablero)`
Retorna una copia independiente del tablero (lista de listas), evitando que los dos algoritmos compartan el mismo estado.

#### `valores_usados(tablero, fila, col)`
Calcula el conjunto de valores **ya ocupados** que restringen una celda `(fila, col)`, revisando:
- Todos los valores de la **fila**.
- Todos los valores de la **columna**.
- Todos los valores del **subcuadro 3×3** al que pertenece la celda.

#### `valores_validos(tablero, fila, col)`
Retorna la lista de valores entre 1 y 9 que **no** están en `valores_usados`, es decir, los candidatos legales para esa celda.

---

### 3. Selección de celda siguiente

Aquí radica la diferencia clave entre los dos enfoques del código.

#### `celda_siguiente_simple(tablero)`
Recorre el tablero de izquierda a derecha, de arriba a abajo, y retorna la **primera celda vacía** que encuentre. Es un enfoque ingenuo: no considera cuántas opciones tiene esa celda.

#### `celda_siguiente_mrv(tablero)`
Implementa la heurística **MRV (Minimum Remaining Values)**: selecciona la celda vacía con el **menor número de valores válidos** posibles. La intuición es que empezar por la celda más restringida reduce las ramas del árbol de búsqueda que se explorarán en vano.

> Si encuentra una celda con un solo candidato (`cant == 1`), la retorna de inmediato como optimización.

---

### 4. Algoritmos de backtracking

Ambos algoritmos siguen la misma lógica general de **búsqueda con retroceso**:

1. Escoger una celda vacía.
2. Intentar cada valor válido.
3. Si el tablero sigue siendo consistente, llamar recursivamente.
4. Si no se encuentra solución en esa rama, **deshacer** la asignación y probar el siguiente valor.
5. Si no quedan celdas vacías, el tablero está resuelto.

#### `backtrack_simple(tablero)`
Usa `celda_siguiente_simple`. Explora el espacio de búsqueda sin ninguna heurística de ordenamiento. Puede hacer un número grande de llamadas recursivas.

```python
def backtrack_simple(tablero):
    global llamadas_sin_mrv
    llamadas_sin_mrv += 1

    celda = celda_siguiente_simple(tablero)
    if celda is None:
        return tablero  # ✅ Solución encontrada

    fila, col = celda
    for valor in range(1, 10):
        if valor not in valores_usados(tablero, fila, col):
            tablero[fila][col] = valor
            resultado = backtrack_simple(tablero)
            if resultado:
                return resultado
            tablero[fila][col] = 0  # ↩️ Retroceso

    return None  # ❌ Sin solución en esta rama
```

#### `backtrack_mrv(tablero)`
Usa `celda_siguiente_mrv` y además precalcula `valores_validos` para no recorrer del 1 al 9 innecesariamente. Si la celda más restringida ya no tiene candidatos, retorna `None` de inmediato.

```python
def backtrack_mrv(tablero):
    global llamadas_con_mrv
    llamadas_con_mrv += 1

    celda = celda_siguiente_mrv(tablero)
    if celda is None:
        return tablero  # ✅ Solución encontrada

    fila, col = celda
    candidatos = valores_validos(tablero, fila, col)

    if not candidatos:
        return None  # ❌ Poda: celda sin opciones

    for valor in candidatos:
        tablero[fila][col] = valor
        resultado = backtrack_mrv(tablero)
        if resultado:
            return resultado
        tablero[fila][col] = 0  # ↩️ Retroceso

    return None
```

---

### 5. Ejecución y comparación

El bloque principal:

1. Muestra el puzzle inicial.
2. Resuelve el puzzle con **backtracking simple** y mide tiempo y llamadas recursivas.
3. Resuelve el mismo puzzle con **backtracking + MRV** y mide las mismas métricas.
4. Imprime una tabla comparativa con la reducción porcentual de llamadas recursivas.

```
  Métrica                                Sin MRV  Con MRV
  ──────────────────────────────────────────────────────
  Llamadas recursivas                      X,XXX      XXX
  Tiempo (ms)                              X.XXX    X.XXX
```

---

## Comparación de enfoques

| Aspecto             | Sin MRV      | Con MRV |
|---------------------|--------------|--------------------|
| Selección de celda | Primera vacía | La más restringida |
| Exploración        | Exhaustiva    | Guiada por heurística |
| Llamadas recursivas | Muchas más   | Significativamente menos |
| Velocidad           | Más lento    | Más rápido |
| Complejidad del código | Simple    | Moderada |

---

## Conclusión

La heurística **MRV** mejora drásticamente el rendimiento del backtracking en puzzles de Sudoku porque reduce la profundidad y el ancho del árbol de búsqueda. Al asignar primero las variables más restringidas, se detectan los conflictos más temprano y se evita explorar ramas condenadas al fracaso. Este principio es aplicable a cualquier CSP, no solo al Sudoku.