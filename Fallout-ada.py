"""
Tarea 2 - Análisis de Algoritmos 2025
Problema de Optimización con Programación Dinámica: Refugio Fallout

Estudiantes: [Victor Salazar] [Cristobal Piña]
Profesor: [Luis Corral]
Fecha: [Julio 2025]

Descripción:
Este programa resuelve un problema de optimización donde un jugador debe navegar
por una cuadrícula [n × n] representando un refugio, recolectando la mayor cantidad
posible de cápsulas RadAway mientras evita bombas, con un límite de [2n-1] movimientos.

Características Principales:
- Implementación con Programación Dinámica y dos tipos de memoización
- Menú interactivo para seleccionar experimentos específicos
- Generación aleatoria de cuadrículas en cada ejecución
- Medición de tiempo y memoria con tracemalloc
- Comparación automática entre métodos Array 3D vs Dictionary Hash
- Interfaz de usuario amigable con emojis y formateo mejorado

Opciones de Ejecución:
1. Experimentos individuales para n = 10, 20, 30, 40
2. Batería completa de todos los experimentos
3. Finalización automática después de cada experimento

Requisitos:
- Python 3.6+
- Librerías estándar: random, time, tracemalloc, typing, sys

Uso:
    python Fallout-ada.py

El programa iniciará un menú interactivo donde podrás elegir qué experimentos ejecutar.
"""

import random
import time
import tracemalloc
from typing import List, Tuple, Dict, Optional
import sys


class FalloutOptimizer:
    """
    Clase que implementa el algoritmo de optimización para el problema del refugio Fallout.
    
    Utiliza programación dinámica con memoización para encontrar el camino óptimo
    desde (0,0) hasta (n-1,n-1) maximizando la recolección de cápsulas RadAway.
    """
    
    def __init__(self, grid: List[List[str]]):
        """
        Inicializa el optimizador con la cuadrícula del refugio.
        
        Args:
            grid: Cuadrícula n × n donde cada celda contiene:
                'B' - Bomba (celda prohibida)
                'R' - RadAway (cápsula recolectable)
                '.' - Celda vacía transitable
        """
        self.grid = grid
        self.n = len(grid)
        self.max_steps = 2 * self.n - 1
        
        # Direcciones cardinales: arriba, derecha, abajo, izquierda
        self.directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        
        # Estadísticas de rendimiento
        self.calls_count = 0
        self.memory_usage = 0
    
    def is_valid_position(self, x: int, y: int) -> bool:
        """
        Verifica si una posición es válida dentro de la cuadrícula.
        
        Args:
            x: Coordenada fila
            y: Coordenada columna
            
        Returns:
            True si la posición está dentro de los límites, False en caso contrario
        """
        return 0 <= x < self.n and 0 <= y < self.n
    
    def is_reachable(self, x: int, y: int, t: int) -> bool:
        """
        Verifica si es posible llegar desde (x,y) hasta (n-1,n-1) en el tiempo restante.
        
        Args:
            x: Coordenada fila actual
            y: Coordenada columna actual
            t: Pasos transcurridos
            
        Returns:
            True si es posible llegar al destino, False en caso contrario
        """
        remaining_steps = self.max_steps - t
        min_distance = abs(self.n - 1 - x) + abs(self.n - 1 - y)
        return remaining_steps >= min_distance
    
    def solve_with_array(self) -> Tuple[int, Dict]:
        """
        Resuelve el problema usando un array tridimensional para memoización.
        
        Returns:
            Tupla con (máximo_cápsulas, estadísticas_rendimiento)
        """
        # Inicializar array tridimensional con valores -1 (no calculado)
        dp = [[[-1 for _ in range(self.max_steps + 1)] 
                for _ in range(self.n)] 
                for _ in range(self.n)]
        
        self.calls_count = 0
        
        # Iniciar medición de memoria
        tracemalloc.start()
        start_time = time.time()
        
        def f(x: int, y: int, t: int) -> int:
            """
            Función recursiva que calcula el máximo número de cápsulas
            recolectadas al estar en posición (x,y) después de t pasos.
            
            Args:
                x: Coordenada fila
                y: Coordenada columna
                t: Número de pasos transcurridos
                
            Returns:
                Máximo número de cápsulas recolectables desde esta posición
            """
            self.calls_count += 1
            
            # Caso base: fuera de límites o celda con bomba
            if not self.is_valid_position(x, y) or self.grid[x][y] == 'B':
                return -float('inf')
            
            # Caso base: se acabó el tiempo
            if t > self.max_steps:
                return -float('inf')
            
            # Caso base: llegamos al destino
            if x == self.n - 1 and y == self.n - 1:
                capsule_value = 1 if self.grid[x][y] == 'R' else 0
                return capsule_value
            
            # Poda: verificar si es posible llegar al destino
            if not self.is_reachable(x, y, t):
                return -float('inf')
            
            # Verificar si ya está calculado
            if dp[x][y][t] != -1:
                return dp[x][y][t]
            
            # Calcular valor de la celda actual
            current_value = 1 if self.grid[x][y] == 'R' else 0
            
            # Explorar todas las direcciones posibles
            max_capsules = -float('inf')
            for dx, dy in self.directions:
                nx, ny = x + dx, y + dy
                next_capsules = f(nx, ny, t + 1)
                max_capsules = max(max_capsules, next_capsules)
            
            # Memoizar resultado
            dp[x][y][t] = current_value + max_capsules if max_capsules != -float('inf') else -float('inf')
            return dp[x][y][t]
        
        result = f(0, 0, 0)
        
        end_time = time.time()
        current_memory, peak_memory = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        
        stats = {
            'execution_time': end_time - start_time,
            'memory_peak': peak_memory,
            'function_calls': self.calls_count,
            'method': 'Array 3D'
        }
        
        return max(0, result), stats
    
    def solve_with_dict(self) -> Tuple[int, Dict]:
        """
        Resuelve el problema usando un diccionario hash para memoización.
        
        Returns:
            Tupla con (máximo_cápsulas, estadísticas_rendimiento)
        """
        dp = {}  # Diccionario para memoización
        self.calls_count = 0
        
        # Iniciar medición de memoria
        tracemalloc.start()
        start_time = time.time()
        
        def f(x: int, y: int, t: int) -> int:
            """
            Función recursiva que calcula el máximo número de cápsulas
            recolectadas al estar en posición (x,y) después de t pasos.
            
            Args:
                x: Coordenada fila
                y: Coordenada columna
                t: Número de pasos transcurridos
                
            Returns:
                Máximo número de cápsulas recolectables desde esta posición
            """
            self.calls_count += 1
            
            # Caso base: fuera de límites o celda con bomba
            if not self.is_valid_position(x, y) or self.grid[x][y] == 'B':
                return -float('inf')
            
            # Caso base: se acabó el tiempo
            if t > self.max_steps:
                return -float('inf')
            
            # Caso base: llegamos al destino
            if x == self.n - 1 and y == self.n - 1:
                capsule_value = 1 if self.grid[x][y] == 'R' else 0
                return capsule_value
            
            # Poda: verificar si es posible llegar al destino
            if not self.is_reachable(x, y, t):
                return -float('inf')
            
            # Verificar si ya está calculado
            state = (x, y, t)
            if state in dp:
                return dp[state]
            
            # Calcular valor de la celda actual
            current_value = 1 if self.grid[x][y] == 'R' else 0
            
            # Explorar todas las direcciones posibles
            max_capsules = -float('inf')
            for dx, dy in self.directions:
                nx, ny = x + dx, y + dy
                next_capsules = f(nx, ny, t + 1)
                max_capsules = max(max_capsules, next_capsules)
            
            # Memoizar resultado
            dp[state] = current_value + max_capsules if max_capsules != -float('inf') else -float('inf')
            return dp[state]
        
        result = f(0, 0, 0)
        
        end_time = time.time()
        current_memory, peak_memory = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        
        stats = {
            'execution_time': end_time - start_time,
            'memory_peak': peak_memory,
            'function_calls': self.calls_count,
            'method': 'Dictionary Hash'
        }
        
        return max(0, result), stats


def generate_random_grid(n: int, bomb_probability: float = 0.2, radaway_probability: float = 0.3) -> List[List[str]]:
    """
    Genera una cuadrícula aleatoria válida para las pruebas del refugio Fallout.
    
    La función asegura que:
    - La posición inicial (0,0) nunca contenga una bomba
    - La posición final (n-1,n-1) nunca contenga una bomba
    - Las probabilidades se distribuyen de manera balanceada
    - Cada ejecución genera una cuadrícula completamente nueva
    
    Args:
        n: Tamaño de la cuadrícula (n×n)
        bomb_probability: Probabilidad de que una celda contenga una bomba (0.0-1.0)
        radaway_probability: Probabilidad de que una celda contenga RadAway (0.0-1.0)
        
    Returns:
        Cuadrícula n×n generada aleatoriamente con las restricciones aplicadas
        
    Nota:
        Las probabilidades son independientes, lo que significa que una celda puede
        ser evaluada primero para bomba y luego para RadAway si no es bomba.
    """
    # Inicializar cuadrícula con celdas vacías
    grid = [['.' for _ in range(n)] for _ in range(n)]
    
    for i in range(n):
        for j in range(n):
            # Garantizar que las posiciones críticas (inicio y fin) no tengan bombas
            if (i == 0 and j == 0) or (i == n-1 and j == n-1):
                # La posición final puede tener RadAway para aumentar el desafío
                if i == n-1 and j == n-1 and random.random() < radaway_probability:
                    grid[i][j] = 'R'
                else:
                    grid[i][j] = '.'  # Mantener inicio siempre vacío
                continue
            
            # Generar contenido aleatorio para el resto de celdas
            rand = random.random()
            if rand < bomb_probability:
                grid[i][j] = 'B'  # Bomba - celda no transitable
            elif rand < bomb_probability + radaway_probability:
                grid[i][j] = 'R'  # RadAway - cápsula recolectable
            else:
                grid[i][j] = '.'  # Celda vacía transitable
    
    return grid


def print_grid(grid: List[List[str]]) -> None:
    """
    Imprime la cuadrícula de forma legible.
    
    Args:
        grid: Cuadrícula a imprimir
    """
    n = len(grid)
    print("Cuadrícula del refugio:")
    print("  " + " ".join(f"{j:2}" for j in range(n)))
    for i in range(n):
        print(f"{i:2} " + " ".join(f"{cell:2}" for cell in grid[i]))
    print()


def run_experiment_legacy(n: int, num_trials: int = 3) -> None:
    """
    Ejecuta experimentos comparativos entre ambos métodos de memoización.
    
    Args:
        n: Tamaño de la cuadrícula
        num_trials: Número de pruebas a realizar
    """
    print(f"\n{'='*60}")
    print(f"EXPERIMENTO PARA n = {n}")
    print(f"{'='*60}")
    
    total_stats_array = {'execution_time': 0, 'memory_peak': 0, 'function_calls': 0}
    total_stats_dict = {'execution_time': 0, 'memory_peak': 0, 'function_calls': 0}
    
    for trial in range(num_trials):
        print(f"\nPrueba {trial + 1}/{num_trials}")
        print("-" * 40)
        
        # Generar cuadrícula aleatoria
        grid = generate_random_grid(n)
        
        if n <= 10:  # Solo mostrar cuadrículas pequeñas
            print_grid(grid)
        
        optimizer = FalloutOptimizer(grid)
        
        # Probar método con array
        print("Ejecutando método con Array 3D...")
        result_array, stats_array = optimizer.solve_with_array()
        
        # Probar método con diccionario
        print("Ejecutando método con Dictionary Hash...")
        result_dict, stats_dict = optimizer.solve_with_dict()
        
        # Verificar consistencia de resultados
        if result_array != result_dict:
            print(f"ADVERTENCIA: Resultados inconsistentes! Array: {result_array}, Dict: {result_dict}")
        
        # Mostrar resultados de la prueba
        print(f"\nResultados de la prueba {trial + 1}:")
        print(f"Máximo de cápsulas recolectadas: {result_array}")
        print(f"\nComparación de métodos:")
        print(f"{'Método':<20} {'Tiempo (s)':<12} {'Memoria (KB)':<15} {'Llamadas':<12}")
        print("-" * 65)
        print(f"{'Array 3D':<20} {stats_array['execution_time']:<12.6f} "
              f"{stats_array['memory_peak']/1024:<15.2f} {stats_array['function_calls']:<12}")
        print(f"{'Dictionary Hash':<20} {stats_dict['execution_time']:<12.6f} "
              f"{stats_dict['memory_peak']/1024:<15.2f} {stats_dict['function_calls']:<12}")
        
        # Acumular estadísticas
        for key in total_stats_array:
            total_stats_array[key] += stats_array[key]
            total_stats_dict[key] += stats_dict[key]
    
    # Calcular promedios
    print(f"\n{'='*60}")
    print(f"PROMEDIOS PARA n = {n} (basado en {num_trials} pruebas)")
    print(f"{'='*60}")
    print(f"{'Método':<20} {'Tiempo (s)':<12} {'Memoria (KB)':<15} {'Llamadas':<12}")
    print("-" * 65)
    print(f"{'Array 3D':<20} {total_stats_array['execution_time']/num_trials:<12.6f} "
          f"{total_stats_array['memory_peak']/1024/num_trials:<15.2f} "
          f"{total_stats_array['function_calls']/num_trials:<12.0f}")
    print(f"{'Dictionary Hash':<20} {total_stats_dict['execution_time']/num_trials:<12.6f} "
          f"{total_stats_dict['memory_peak']/1024/num_trials:<15.2f} "
          f"{total_stats_dict['function_calls']/num_trials:<12.0f}")
    
    # Análisis de eficiencia
    speedup = total_stats_array['execution_time'] / total_stats_dict['execution_time']
    memory_ratio = total_stats_array['memory_peak'] / total_stats_dict['memory_peak']
    
    print(f"\nAnálisis de eficiencia:")
    print(f"Speedup (Array/Dict): {speedup:.2f}x")
    print(f"Ratio de memoria (Array/Dict): {memory_ratio:.2f}x")
    
    if speedup > 1:
        print("El método con Dictionary Hash es más rápido")
    else:
        print("El método con Array 3D es más rápido")
    
    if memory_ratio > 1:
        print("El método con Dictionary Hash usa menos memoria")
    else:
        print("El método con Array 3D usa menos memoria")


def show_menu() -> int:
    """
    Muestra el menú de opciones al usuario y retorna la opción seleccionada.
    
    Returns:
        Número de la opción seleccionada (1-6)
    """
    print("\n" + "="*70)
    print("       ESCAPE DEL REFUGIO FALLOUT - PROGRAMACIÓN DINÁMICA")
    print("="*70)
    print("Seleccione una opción:")
    print("1. Ejecutar experimento para n = 10")
    print("2. Ejecutar experimento para n = 20") 
    print("3. Ejecutar experimento para n = 30")
    print("4. Ejecutar experimento para n = 40")
    print("5. Ejecutar TODOS los experimentos (n = 10, 20, 30, 40)")
    print("6. Salir del programa")
    print("-"*70)
    
    while True:
        try:
            choice = int(input("Ingrese su opción (1-6): "))
            if 1 <= choice <= 6:
                return choice
            else:
                print("Opción inválida. Por favor ingrese un número entre 1 y 6.")
        except ValueError:
            print("Por favor ingrese un número válido.")


def run_single_experiment(n: int) -> None:
    """
    Ejecuta experimentos para un tamaño específico de cuadrícula.
    
    Args:
        n: Tamaño de la cuadrícula (n×n)
    """
    print(f"\nINICIANDO EXPERIMENTO PARA n = {n}")
    print("="*60)
    print(f"Configuración:")
    print(f"   • Tamaño de cuadrícula: {n}×{n}")
    print(f"   • Máximo de movimientos: {2*n-1}")
    print(f"   • Número de pruebas: 3")
    print(f"   • Métodos: Array 3D vs Dictionary Hash")
    print("-"*60)
    
    # Generar nueva semilla aleatoria para cada experimento
    random.seed(int(time.time()))
    
    total_stats_array = {'execution_time': 0, 'memory_peak': 0, 'function_calls': 0}
    total_stats_dict = {'execution_time': 0, 'memory_peak': 0, 'function_calls': 0}
    
    for trial in range(3):
        print(f"\nPRUEBA {trial + 1}/3")
        print("-" * 40)
        
        # Generar cuadrícula aleatoria
        grid = generate_random_grid(n)
        
        if n <= 10:  # Solo mostrar cuadrículas pequeñas
            print_grid(grid)
        else:
            print(f"Cuadrícula {n}×{n} generada (demasiado grande para mostrar)")
        
        optimizer = FalloutOptimizer(grid)
        
        # Probar método con array
        print("Ejecutando método con Array 3D...")
        result_array, stats_array = optimizer.solve_with_array()
        
        # Probar método con diccionario
        print("Ejecutando método con Dictionary Hash...")
        result_dict, stats_dict = optimizer.solve_with_dict()
        
        # Verificar consistencia de resultados
        if result_array != result_dict:
            print(f"ADVERTENCIA: Resultados inconsistentes! Array: {result_array}, Dict: {result_dict}")
        
        # Mostrar resultados de la prueba
        print(f"\nRESULTADOS DE LA PRUEBA {trial + 1}:")
        print(f"Máximo de cápsulas recolectadas: {result_array}")
        print(f"\nComparación de métodos:")
        print(f"{'Método':<20} {'Tiempo (s)':<12} {'Memoria (KB)':<15} {'Llamadas':<12}")
        print("-" * 65)
        print(f"{'Array 3D':<20} {stats_array['execution_time']:<12.6f} "
              f"{stats_array['memory_peak']/1024:<15.2f} {stats_array['function_calls']:<12}")
        print(f"{'Dictionary Hash':<20} {stats_dict['execution_time']:<12.6f} "
              f"{stats_dict['memory_peak']/1024:<15.2f} {stats_dict['function_calls']:<12}")
        
        # Acumular estadísticas
        for key in total_stats_array:
            total_stats_array[key] += stats_array[key]
            total_stats_dict[key] += stats_dict[key]
    
    # Calcular y mostrar promedios
    print(f"\n{'='*60}")
    print(f"RESUMEN FINAL PARA n = {n} (promedio de 3 pruebas)")
    print(f"{'='*60}")
    print(f"{'Método':<20} {'Tiempo (s)':<12} {'Memoria (KB)':<15} {'Llamadas':<12}")
    print("-" * 65)
    print(f"{'Array 3D':<20} {total_stats_array['execution_time']/3:<12.6f} "
          f"{total_stats_array['memory_peak']/1024/3:<15.2f} "
          f"{total_stats_array['function_calls']/3:<12.0f}")
    print(f"{'Dictionary Hash':<20} {total_stats_dict['execution_time']/3:<12.6f} "
          f"{total_stats_dict['memory_peak']/1024/3:<15.2f} "
          f"{total_stats_dict['function_calls']/3:<12.0f}")
    
    # Análisis de eficiencia
    speedup = total_stats_array['execution_time'] / total_stats_dict['execution_time']
    memory_ratio = total_stats_array['memory_peak'] / total_stats_dict['memory_peak']
    
    print(f"\nANÁLISIS DE EFICIENCIA:")
    print(f"Speedup (Array/Dict): {speedup:.2f}x")
    print(f"Ratio de memoria (Array/Dict): {memory_ratio:.2f}x")
    
    if speedup > 1:
        print("El método con Dictionary Hash es más rápido")
    else:
        print("El método con Array 3D es más rápido")
    
    if memory_ratio > 1:
        print("El método con Dictionary Hash usa menos memoria")
    else:
        print("El método con Array 3D usa menos memoria")
    
    print(f"\nEXPERIMENTO PARA n = {n} COMPLETADO")


def run_all_experiments() -> None:
    """
    Ejecuta experimentos para todos los tamaños de cuadrícula.
    """
    print(f"\nINICIANDO BATERÍA COMPLETA DE EXPERIMENTOS")
    print("="*60)
    
    test_sizes = [10, 20, 30, 40]
    start_time_total = time.time()
    
    print(f"Se ejecutarán experimentos para: {test_sizes}")
    print(f"⏱ Tiempo estimado: 2-5 minutos (dependiendo del hardware)")
    print("="*60)
    
    for i, n in enumerate(test_sizes, 1):
        print(f"\nEXPERIMENTO {i}/4: n = {n}")
        try:
            run_single_experiment(n)
        except KeyboardInterrupt:
            print(f"\nExperimentos interrumpidos por el usuario en n = {n}")
            break
        except Exception as e:
            print(f"\nError en experimento para n = {n}: {e}")
            continue
    
    total_time = time.time() - start_time_total
    print(f"\n{'='*60}")
    print(f"TODOS LOS EXPERIMENTOS COMPLETADOS")
    print(f"⏱ Tiempo total de ejecución: {total_time:.2f} segundos")
    print(f"{'='*60}")
    print(f"\nCONCLUSIONES GENERALES:")
    print(f"1. La programación dinámica reduce significativamente la complejidad")
    print(f"2. La memoización evita recálculos innecesarios")
    print(f"3. Los métodos con array y diccionario tienen trade-offs diferentes")
    print(f"4. El análisis experimental permite evaluar el rendimiento real")
    print(f"5. A mayor n, las diferencias de rendimiento se hacen más notables")


def main():
    """
    Función principal que maneja el menú interactivo y la ejecución del programa.
    """
    print("Tarea 2 - Análisis de Algoritmos 2025")
    print("Problema de Optimización: Escape del Refugio Fallout")
    print("Implementación con Programación Dinámica y Memoización")
    
    while True:
        choice = show_menu()
        
        if choice == 1:
            run_single_experiment(10)
        elif choice == 2:
            run_single_experiment(20)
        elif choice == 3:
            run_single_experiment(30)
        elif choice == 4:
            run_single_experiment(40)
        elif choice == 5:
            run_all_experiments()
        elif choice == 6:
            print("\n¡Gracias por usar el programa!")
            print("Programa desarrollado para Análisis de Algoritmos 2025")
            break
        
        # Preguntar si desea continuar
        print(f"\n{'='*60}")
        while True:
            continue_choice = input("¿Desea ejecutar otro experimento? (s/n): ").lower().strip()
            if continue_choice in ['s', 'si', 'y', 'yes']:
                break
            elif continue_choice in ['n', 'no']:
                print("\n¡Gracias por usar el programa!")
                print("Programa desarrollado para Análisis de Algoritmos 2025")
                return
            else:
                print("Por favor responda 's' para sí o 'n' para no.")
    
    print("\nLiberando memoria y cerrando programa...")
    print("Programa finalizado correctamente.")


if __name__ == "__main__":
    main()