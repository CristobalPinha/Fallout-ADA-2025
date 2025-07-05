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
- Librería adicional: matplotlib (para visualización de resultados)

Uso:
    python Fallout-ada.py

El programa iniciará un menú interactivo donde podrás elegir qué experimentos ejecutar.
"""

import random
import time
import tracemalloc
from typing import List, Tuple, Dict, Optional, Any
import sys
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle


class alg_optimizado:
    """
    Clase que implementa el algoritmo de optimización para el problema refugio Fallout.
    
    Utiliza programación dinámica con memoización para encontrar el camino óptimo
    desde (0,0) hasta (n-1,n-1) maximizando la recolección de cápsulas RadAway.
    """
    
    def __init__(self, grid: List[List[str]]):
        """
        Inicializa el optimizador con la cuadrícula del refugio.
        self hace referencia a la instancia actual de la clase.
        Argumentos:
            grid: Matriz n × n donde cada celda contiene:
                'B' - Bomba (celda no transitable)
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
    
    def posicion_valida(self, x: int, y: int) -> bool:
        """
        Verifica si una posición es válida dentro de la cuadrícula.
        
        Args:
            x: Coordenada fila
            y: Coordenada columna
            
        Returns:
            True si la posición está dentro de los límites, False en caso contrario
        """
        return 0 <= x < self.n and 0 <= y < self.n

    def es_alcanzable(self, x: int, y: int, t: int) -> bool:
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

    def resuelve_con_array(self) -> Tuple[int, Dict, list]:
        """
        Resuelve el problema usando un array tridimensional para memoización.
        """
        dp = [[[-1 for _ in range(self.max_steps + 1)] 
                for _ in range(self.n)] 
                for _ in range(self.n)]
        parent: list[list[list[Any]]] = [[[None for _ in range(self.max_steps + 1)] 
                for _ in range(self.n)] 
                for _ in range(self.n)]
        self.calls_count = 0
        # Iniciar medición de memoria
        tracemalloc.start()
        start_time = time.time()
        
        def funcion_capsulas(x: int, y: int, t: int) -> int:
            """
            Función recursiva que calcula el máximo número de cápsulas
            recolectadas al estar en posición (x,y) después de t pasos.
            
            Argumentos:
                x: Coordenada fila
                y: Coordenada columna
                t: Número de pasos 
                
            Retorna el máximo número de cápsulas recolectables desde esta posición
            """
            self.calls_count += 1
            
            # Caso base: fuera de límites o celda con bomba
            if not self.posicion_valida(x, y) or self.grid[x][y] == 'B':
                return -999999
            
            # Caso base: se acabó el tiempo
            if t > self.max_steps:
                return -999999
            
            # Caso base: llegamos al destino
            if x == self.n - 1 and y == self.n - 1:
                return 1 if self.grid[x][y] == 'R' else 0
            
            # Poda: verificar si es posible llegar al destino
            if not self.es_alcanzable(x, y, t):
                return -999999
            
            # Verificar si ya está calculado
            if dp[x][y][t] != -1:
                return dp[x][y][t]
            
            # Calcular valor de la celda actual
            celda_actual = 1 if self.grid[x][y] == 'R' else 0
            
            # Explorar todas las direcciones posibles
            max_capsulas = -999999
            mejor_movimiento = None
            for dx, dy in self.directions:
                nx, ny = x + dx, y + dy
                next_capsulas = funcion_capsulas(nx, ny, t + 1)
                if next_capsulas > max_capsulas:
                    max_capsulas = next_capsulas
                    mejor_movimiento = (nx, ny)
            
            # Memoizar resultado
            dp[x][y][t] = celda_actual + max_capsulas if max_capsulas != -999999 else -999999
            parent[x][y][t] = mejor_movimiento if max_capsulas != -999999 else None
            return dp[x][y][t]

        resultado = funcion_capsulas(0, 0, 0)

        end_time = time.time()
        current_memory, peak_memory = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        
        # Reconstruir camino óptimo
        camino_opt = []
        x, y, t = 0, 0, 0
        if dp[x][y][t] != -999999:
            camino_opt.append((x, y))
            while (x, y) != (self.n-1, self.n-1):
                sgt_pos = parent[x][y][t]
                if sgt_pos is None:
                    break
                x, y = sgt_pos
                camino_opt.append((x, y))
                t += 1
        
        stats = {
            'execution_time': end_time - start_time,
            'memory_peak': peak_memory,
            'function_calls': self.calls_count,
            'method': 'Array 3D'
        }
        
        return max(0, resultado), stats, camino_opt
    
    def resuelve_hash(self) -> Tuple[int, Dict, list]:
        """
        Resuelve el problema usando un diccionario hash para memoización.
        
        Retorna máximo_cápsulas y estadísticas_rendimiento
        """
        dp = {}  # Diccionario para memoización
        parent = {}
        self.calls_count = 0
        
        # Iniciar medición de memoria
        tracemalloc.start()
        start_time = time.time()

        def funcion_hash(x: int, y: int, t: int) -> int:
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
            if not self.posicion_valida(x, y) or self.grid[x][y] == 'B':
                return -999999
            
            # Caso base: se acabó el tiempo
            if t > self.max_steps:
                return -999999
            
            # Caso base: llegamos al destino
            if x == self.n - 1 and y == self.n - 1:
                return 1 if self.grid[x][y] == 'R' else 0
            
            # Poda: verificar si es posible llegar al destino
            if not self.es_alcanzable(x, y, t):
                return -999999

            estado = (x, y, t)
            # Verificar si ya está calculado
            if estado in dp:
                return dp[estado]

            # Calcular valor de la celda actual
            celda_actual = 1 if self.grid[x][y] == 'R' else 0
            
            # Explorar todas las direcciones posibles
            max_capsulas = -999999
            mejor_movimiento = None
            for dx, dy in self.directions:
                nx, ny = x + dx, y + dy
                next_capsulas = funcion_hash(nx, ny, t + 1)
                if next_capsulas > max_capsulas:
                    max_capsulas = next_capsulas
                    mejor_movimiento = (nx, ny)

            # Memoizar resultado
            dp[estado] = celda_actual + max_capsulas if max_capsulas != -999999 else -999999
            parent[estado] = mejor_movimiento if max_capsulas != -999999 else None
            return dp[estado]

        resultado = funcion_hash(0, 0, 0)

        end_time = time.time()
        current_memory, peak_memory = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        
        # Reconstruir camino óptimo
        camino_opt = []
        x, y, t = 0, 0, 0
        if (0, 0, 0) in dp and dp[(0, 0, 0)] != -999999:
            camino_opt.append((x, y))
            while (x, y) != (self.n-1, self.n-1):
                pos_sgt = parent.get((x, y, t))
                if pos_sgt is None:
                    break
                x, y = pos_sgt
                camino_opt.append((x, y))
                t += 1
        
        stats = {
            'execution_time': end_time - start_time,
            'memory_peak': peak_memory,
            'function_calls': self.calls_count,
            'method': 'Dictionary Hash'
        }
        
        return max(0, resultado), stats, camino_opt


def graficos_comparativos(todos_resultados: List[Dict]) -> None:
    """
    Crea gráficos comparativos de rendimiento entre Array 3D y Dictionary Hash.
    
    Args:
        todos_resultados: Lista de resultados de experimentos
    """
    if len(todos_resultados) < 2:
        print("Se necesitan al menos 2 experimentos para generar gráficos comparativos.")
        return

    sizes = [result['size'] for result in todos_resultados]
    array_times = [result['array_avg_time'] for result in todos_resultados]
    dict_times = [result['dict_avg_time'] for result in todos_resultados]
    array_memory = [result['array_avg_memory'] for result in todos_resultados]
    dict_memory = [result['dict_avg_memory'] for result in todos_resultados]
    array_calls = [result['array_avg_calls'] for result in todos_resultados]
    dict_calls = [result['dict_avg_calls'] for result in todos_resultados]

    # Crear subplots
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle('Comparación de Rendimiento: Array 3D vs Dictionary Hash', fontsize=16, fontweight='bold')
    
    # Gráfico 1: Tiempo de ejecución
    ax1.plot(sizes, array_times, 'b-o', label='Array 3D', linewidth=2, markersize=8)
    ax1.plot(sizes, dict_times, 'r-s', label='Dictionary Hash', linewidth=2, markersize=8)
    ax1.set_xlabel('Tamaño del mapa (n)', fontsize=12)
    ax1.set_ylabel('Tiempo promedio (segundos)', fontsize=12)
    ax1.set_title('Tiempo de Ejecución', fontsize=14, fontweight='bold')
    ax1.legend(fontsize=11)
    ax1.grid(True, alpha=0.3)
    ax1.set_yscale('log')
    
    # Gráfico 2: Uso de memoria
    x_pos = np.arange(len(sizes))
    width = 0.35
    ax2.bar(x_pos - width/2, array_memory, width, label='Array 3D', alpha=0.8, color='blue')
    ax2.bar(x_pos + width/2, dict_memory, width, label='Dictionary Hash', alpha=0.8, color='red')
    ax2.set_xlabel('Tamaño del mapa (n)', fontsize=12)
    ax2.set_ylabel('Memoria promedio (KB)', fontsize=12)
    ax2.set_title('Uso de Memoria', fontsize=14, fontweight='bold')
    ax2.set_xticks(x_pos)
    ax2.set_xticklabels(sizes)
    ax2.legend(fontsize=11)
    ax2.grid(True, alpha=0.3)
    
    # Gráfico 3: Factor de velocidad (speedup)
    speedup_factors = [a/d if d > 0 else 1 for a, d in zip(array_times, dict_times)]
    colors = ['green' if s < 1 else 'orange' if s < 1.5 else 'red' for s in speedup_factors]
    ax3.bar(sizes, speedup_factors, color=colors, alpha=0.7)
    ax3.axhline(y=1, color='black', linestyle='--', alpha=0.7, label='Mismo rendimiento')
    ax3.set_xlabel('Tamaño del mapa (n)', fontsize=12)
    ax3.set_ylabel('Factor de velocidad (Array/Dict)', fontsize=12)
    ax3.set_title('Factor de Velocidad Relativa', fontsize=14, fontweight='bold')
    ax3.legend(fontsize=11)
    ax3.grid(True, alpha=0.3)
    
    # Gráfico 4: Número de llamadas recursivas
    ax4.semilogy(sizes, array_calls, 'b-o', label='Array 3D', linewidth=2, markersize=8)
    ax4.semilogy(sizes, dict_calls, 'r-s', label='Dictionary Hash', linewidth=2, markersize=8)
    ax4.set_xlabel('Tamaño del mapa (n)', fontsize=12)
    ax4.set_ylabel('Llamadas promedio (escala log)', fontsize=12)
    ax4.set_title('Número de Llamadas Recursivas', fontsize=14, fontweight='bold')
    ax4.legend(fontsize=11)
    ax4.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()
    
    # Mostrar análisis textual
    print(f"\n{'='*80}")
    print("ANÁLISIS COMPARATIVO DE RENDIMIENTO")
    print(f"{'='*80}")
    
    for i, size in enumerate(sizes):
        speedup = speedup_factors[i]
        memory_ratio = array_memory[i] / dict_memory[i] if dict_memory[i] > 0 else 1
        
        print(f"\nPara n = {size}:")
        print(f"  • Factor de velocidad: {speedup:.2f}x ({'Dict más rápido' if speedup > 1 else 'Array más rápido'})")
        print(f"  • Factor de memoria: {memory_ratio:.2f}x ({'Dict más eficiente' if memory_ratio > 1 else 'Array más eficiente'})")
        print(f"  • Llamadas Array: {array_calls[i]:,.0f} vs Dict: {dict_calls[i]:,.0f}")


def random_map(n: int, bomb_probability: float = 0.2, radaway_probability: float = 0.3) -> List[List[str]]:
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
        
    Retorna:
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
            aleatorio = random.random()
            if aleatorio < bomb_probability:
                grid[i][j] = 'B'  # Bomba - celda no transitable
            elif aleatorio < bomb_probability + radaway_probability:
                grid[i][j] = 'R'  # RadAway - cápsula recolectable
            else:
                grid[i][j] = '.'  # Celda vacía transitable
    
    return grid


def mostrar_map(grid: List[List[str]]) -> None:
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


def experimentos_comp(n: int, num_trials: int = 3) -> None:
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
        grid = random_map(n)
        
        if n <= 10:  # Solo mostrar cuadrículas pequeñas
            mostrar_map(grid)
        
        optimizer = alg_optimizado(grid)
        
        # Probar método con Array 3D
        print("Se ejecutará método Array 3D")
        result_array, stats_array, _ = optimizer.resuelve_con_array()
        
        # Probar método Hash
        print("Se ejecutará método Hash")
        result_dict, stats_dict, _ = optimizer.resuelve_hash()
        
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


def mostrar_menu() -> int:
    print("\n" + "="*70)
    print("=== Refugio Fallout ===")
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


def unico_exp(n: int) -> Dict:
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
    
    stats_totales = {'execution_time': 0, 'memory_peak': 0, 'function_calls': 0}
    stats_totales_dict = {'execution_time': 0, 'memory_peak': 0, 'function_calls': 0}
    
    for j in range(3):
        print(f"\nPRUEBA {j + 1}/3")
        print("-" * 40)
        
        # Generar cuadrícula aleatoria
        grid = random_map(n)
        
        if n <= 10:  # Solo mostrar cuadrículas pequeñas
            mostrar_map(grid)
        else:
            print(f"Cuadrícula {n}×{n} generada (demasiado grande para mostrar)")
        
        optimizado = alg_optimizado(grid)
        
        print("Ejecutar método Array 3D")
        resultado_array, stats_array, camino_opt_array = optimizado.resuelve_con_array()
        print("Ejecutar método Dictionary Hash")
        result_dict, stats_dict, path_dict = optimizado.resuelve_hash()
        # Verificar consistencia de resultados
        if resultado_array != result_dict:
            print(f"ADVERTENCIA: Resultados inconsistentes! Array: {resultado_array}, Dict: {result_dict}")
        
        # Mostrar resultados de la prueba
        print(f"\nRESULTADOS DE LA PRUEBA {j + 1}:")
        print(f"Máximo de cápsulas recolectadas: {resultado_array}")
        print(f"\nComparación de métodos:")
        print(f"{'Método':<20} {'Tiempo (s)':<12} {'Memoria (KB)':<15} {'Llamadas':<12}")
        print("-" * 65)
        print(f"{'Array 3D':<20} {stats_array['execution_time']:<12.6f} "
              f"{stats_array['memory_peak']/1024:<15.2f} {stats_array['function_calls']:<12}")
        print(f"{'Dictionary Hash':<20} {stats_dict['execution_time']:<12.6f} "
              f"{stats_dict['memory_peak']/1024:<15.2f} {stats_dict['function_calls']:<12}")
        
        # Mostrar camino óptimo como texto
        if n <= 20:
            print(f"\nCAMINO ÓPTIMO - Array 3D:")
            if camino_opt_array:
                print(f"Longitud del camino: {len(camino_opt_array)} pasos")
                print("Ruta: " + " -> ".join([f"({x},{y})" for x, y in camino_opt_array]))
                # Mostrar RadAway recolectado en el camino
                radaway_collected = sum(1 for x, y in camino_opt_array if grid[x][y] == 'R')
                print(f"RadAway recolectado en el camino: {radaway_collected}")
            else:
                print("No se encontró camino válido")
            
            print(f"\nCAMINO ÓPTIMO - Dictionary Hash:")
            if path_dict:
                print(f"Longitud del camino: {len(path_dict)} pasos")
                print("Ruta: " + " -> ".join([f"({x},{y})" for x, y in path_dict]))
                # Mostrar RadAway recolectado en el camino
                radaway_collected = sum(1 for x, y in path_dict if grid[x][y] == 'R')
                print(f"RadAway recolectado en el camino: {radaway_collected}")
            else:
                print("No se encontró camino válido")
        
        # Acumular estadísticas
        for key in stats_totales:
            stats_totales[key] += stats_array[key]
            stats_totales_dict[key] += stats_dict[key]
    
    # Calcular y mostrar promedios
    print(f"\n{'='*60}")
    print(f"RESUMEN FINAL PARA n = {n} (promedio de 3 pruebas)")
    print(f"{'='*60}")
    print(f"{'Método':<20} {'Tiempo (s)':<12} {'Memoria (KB)':<15} {'Llamadas':<12}")
    print("-" * 65)
    print(f"{'Array 3D':<20} {stats_totales['execution_time']/3:<12.6f} "
          f"{stats_totales['memory_peak']/1024/3:<15.2f} "
          f"{stats_totales['function_calls']/3:<12.0f}")
    print(f"{'Dictionary Hash':<20} {stats_totales_dict['execution_time']/3:<12.6f} "
          f"{stats_totales_dict['memory_peak']/1024/3:<15.2f} "
          f"{stats_totales_dict['function_calls']/3:<12.0f}")
    
    # Análisis de eficiencia
    speedup = stats_totales['execution_time'] / stats_totales_dict['execution_time']
    memory_ratio = stats_totales['memory_peak'] / stats_totales_dict['memory_peak']
    
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
    
    # Retornar datos para gráficos comparativos
    return {
        'size': n,
        'array_avg_time': stats_totales['execution_time'] / 3,
        'dict_avg_time': stats_totales_dict['execution_time'] / 3,
        'array_avg_memory': stats_totales['memory_peak'] / 1024 / 3,
        'dict_avg_memory': stats_totales_dict['memory_peak'] / 1024 / 3,
        'array_avg_calls': stats_totales['function_calls'] / 3,
        'dict_avg_calls': stats_totales_dict['function_calls'] / 3
    }


def run_all_experiments() -> None:
    """
    Ejecuta experimentos para todos los tamaños de cuadrícula.
    """
    print(f"\nINICIANDO BATERÍA COMPLETA DE EXPERIMENTOS")
    print("="*60)
    
    len_test = [10, 20, 30, 40]
    tiempo_total = time.time()
    todos_resultados = []
    
    print(f"Se ejecutarán experimentos para: {len_test}")
    print(f" Tiempo estimado: 2-5 minutos (dependiendo del hardware)")
    print("="*60)
    
    for i, n in enumerate(len_test, 1):
        print(f"\nEXPERIMENTO {i}/4: n = {n}")
        try:
            result = unico_exp(n)
            todos_resultados.append(result)
        except KeyboardInterrupt:
            print(f"\nExperimentos interrumpidos por el usuario en n = {n}")
            break
        except Exception as e:
            print(f"\nError en experimento para n = {n}: {e}")
            continue
    
    total_time = time.time() - tiempo_total
    print(f"\n{'='*60}")
    print(f"TODOS LOS EXPERIMENTOS COMPLETADOS")
    print(f" Tiempo total de ejecución: {total_time:.2f} segundos")
    print(f"{'='*60}")
    
    # Generar gráficos comparativos si hay resultados
    if len(todos_resultados) >= 2:
        print("\nGenerando gráficos comparativos de rendimiento...")
        graficos_comparativos(todos_resultados)

def main():
    """
    Función principal que maneja el menú interactivo y la ejecución del programa.
    """
    print("Tarea 2 - Análisis de Algoritmos 2025")
    print("Problema de Optimización: Escape del Refugio Fallout")
    print("Implementación con Programación Dinámica y Memoización")
    
    while True:
        opcion = mostrar_menu()
        
        if opcion == 1:
            unico_exp(10)
        elif opcion == 2:
            unico_exp(20)
        elif opcion == 3:
            unico_exp(30)
        elif opcion == 4:
            unico_exp(40)
        elif opcion == 5:
            run_all_experiments()
        elif opcion == 6:
            print("\n¡Gracias por usar el programa!")
            print("Programa desarrollado para Análisis de Algoritmos 2025")
            break
        
        # Preguntar si desea continuar
        print(f"\n{'='*60}")
        while True:
            sgt_opcion = input("¿Desea ejecutar otro experimento? (s/n): ").lower().strip()
            if sgt_opcion in ['s', 'si', 'y', 'yes']:
                break
            elif sgt_opcion in ['n', 'no']:
                print("\n¡Gracias por usar el programa!")
                print("Programa desarrollado para Análisis de Algoritmos 2025")
                return
            else:
                print("Por favor responda 's' para sí o 'n' para no.")
    
    print("Programa finalizado correctamente.")


if __name__ == "__main__":
    main()