import time

SUDOKU_EJEMPLO = [
    [5, 3, 0,  0, 7, 0,  0, 0, 0],
    [6, 0, 0,  1, 9, 5,  0, 0, 0],
    [0, 9, 8,  0, 0, 0,  0, 6, 0],

    [8, 0, 0,  0, 6, 0,  0, 0, 3],
    [4, 0, 0,  8, 0, 3,  0, 0, 1],
    [7, 0, 0,  0, 2, 0,  0, 0, 6],

    [0, 6, 0,  0, 0, 0,  2, 8, 0],
    [0, 0, 0,  4, 1, 9,  0, 0, 5],
    [0, 0, 0,  0, 8, 0,  0, 7, 9],
]


def mostrar_tablero(tablero, titulo):
    print(f"\n{'─'*25}  {titulo}  {'─'*25}")
    for i, fila in enumerate(tablero):
        if i % 3 == 0 and i != 0:
            print("  ------+-------+------")
        linea = ""
        for j, val in enumerate(fila):
            if j % 3 == 0 and j != 0:
                linea += " | "
            linea += f" {'.' if val == 0 else val}"
        print(" ", linea)
    print()


def copiar_tablero(tablero):
    return [fila[:] for fila in tablero]


def valores_usados(tablero, fila, col):
    usados = set()
    usados.update(tablero[fila])
    usados.update(tablero[f][col] for f in range(9))
    bf = (fila // 3) * 3
    bc = (col // 3) * 3
    for r in range(bf, bf + 3):
        for c in range(bc, bc + 3):
            usados.add(tablero[r][c])
    usados.discard(0)
    return usados


def valores_validos(tablero, fila, col):
    return [v for v in range(1, 10) if v not in valores_usados(tablero, fila, col)]


def celda_siguiente_simple(tablero):
    for i in range(9):
        for j in range(9):
            if tablero[i][j] == 0:
                return (i, j)
    return None


def celda_siguiente_mrv(tablero):
    mejor_celda = None
    mejor_cant = 10

    for i in range(9):
        for j in range(9):
            if tablero[i][j] == 0:
                cant = len(valores_validos(tablero, i, j))
                if cant < mejor_cant:
                    mejor_cant = cant
                    mejor_celda = (i, j)
                    if cant == 1:
                        return mejor_celda

    return mejor_celda


llamadas_sin_mrv = 0

def backtrack_simple(tablero):
    global llamadas_sin_mrv
    llamadas_sin_mrv += 1

    celda = celda_siguiente_simple(tablero)
    if celda is None:
        return tablero

    fila, col = celda
    for valor in range(1, 10):
        if valor not in valores_usados(tablero, fila, col):
            tablero[fila][col] = valor
            resultado = backtrack_simple(tablero)
            if resultado:
                return resultado
            tablero[fila][col] = 0

    return None


llamadas_con_mrv = 0

def backtrack_mrv(tablero):
    global llamadas_con_mrv
    llamadas_con_mrv += 1

    celda = celda_siguiente_mrv(tablero)
    if celda is None:
        return tablero

    fila, col = celda
    candidatos = valores_validos(tablero, fila, col)

    if not candidatos:
        return None

    for valor in candidatos:
        tablero[fila][col] = valor
        resultado = backtrack_mrv(tablero)
        if resultado:
            return resultado
        tablero[fila][col] = 0

    return None


try:

    print("=" * 60)
    print("  SOLUCION DE SUDOKU COMO CSP")
    print("=" * 60)

    mostrar_tablero(SUDOKU_EJEMPLO, "Puzzle inicial")

    # Versión SIN MRV
    tablero1 = copiar_tablero(SUDOKU_EJEMPLO)
    llamadas_sin_mrv = 0
    t0 = time.perf_counter()
    sol1 = backtrack_simple(tablero1)
    t1 = time.perf_counter()

    if sol1:
        mostrar_tablero(sol1, "Solución — Backtracking simple (sin MRV)")
        print(f"  Llamadas recursivas (SIN MRV): {llamadas_sin_mrv:,}")
        print(f"  Tiempo (SIN MRV):              {(t1 - t0)*1000:.3f} ms\n")
    else:
        print("  Sin solución (backtracking simple)\n")

    # Versión CON MRV
    tablero2 = copiar_tablero(SUDOKU_EJEMPLO)
    llamadas_con_mrv = 0
    t2 = time.perf_counter()
    sol2 = backtrack_mrv(tablero2)
    t3 = time.perf_counter()

    if sol2:
        mostrar_tablero(sol2, "Solución — Backtracking + MRV")
        print(f"  Llamadas recursivas (CON MRV): {llamadas_con_mrv:,}")
        print(f"  Tiempo (CON MRV):              {(t3 - t2)*1000:.3f} ms\n")
    else:
        print("  Sin solución (MRV)\n")

    # Comparación final
    if sol1 and sol2:
        reduccion = (1 - llamadas_con_mrv / llamadas_sin_mrv) * 100
        print("=" * 60)
        print("  COMPARACIÓN FINAL")
        print("=" * 60)
        print(f"  {'Métrica':<38} {'Sin MRV':>8} {'Con MRV':>8}")
        print(f"  {'-'*54}")
        print(f"  {'Llamadas recursivas':<38} {llamadas_sin_mrv:>8,} {llamadas_con_mrv:>8,}")
        print(f"  {'Tiempo (ms)':<38} {(t1-t0)*1000:>8.3f} {(t3-t2)*1000:>8.3f}")
        print()
        
except:
    print("Ocurrió un error inesperado durante la ejecución.")