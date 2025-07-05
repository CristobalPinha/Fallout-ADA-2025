# 🎮 Escape del Refugio Fallout
## Análisis de Algoritmos 2025 - Programación Dinámica

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-Academic-green.svg)]()
[![Status](https://img.shields.io/badge/Status-Complete-success.svg)]()

### 👥 **Información del Proyecto**
- **Estudiantes**: Victor Salazar, Cristobal Piña
- **Profesor**: Luis Corral
- **Curso**: Análisis de Algoritmos 2025
- **Fecha**: Julio 2025

---

## 📋 **Índice**
- [🎯 Síntesis del Problema](#-síntesis-del-problema)
- [🔄 Relación de Recurrencia](#-relación-de-recurrencia)
- [📊 Tabla de Memoización](#-tabla-de-memoización)
- [🏁 Base del Problema](#-base-del-problema)
- [⚡ Orden del Algoritmo](#-orden-del-algoritmo)
- [🧠 Tipo de Algoritmo](#-tipo-de-algoritmo)
- [🚀 Cómo Ejecutar](#-cómo-ejecutar)
- [📈 Interpretación de Resultados](#-interpretación-de-resultados)
- [📦 Instalación](#-instalación)
- [🔬 Resultados Experimentales](#-resultados-experimentales)

---

## 🎯 **S - Síntesis del Problema**

### **Descripción General**
El problema "Escape del Refugio Fallout" consiste en navegar por una cuadrícula de tamaño `n×n` que representa un refugio post-apocalíptico. El jugador debe moverse desde la posición inicial `(0,0)` hasta la posición final `(n-1,n-1)` en **máximo 2n-1 movimientos**, maximizando la recolección de cápsulas RadAway mientras evita las bombas.

### **Elementos de la Cuadrícula**
| Símbolo | Descripción | Efecto |
|---------|-------------|--------|
| `'B'` | 💣 **Bomba** | Celda prohibida (no transitable) |
| `'R'` | 💊 **RadAway** | Cápsula recolectable (una vez) |
| `'.'` | ⬜ **Sala vacía** | Celda transitable sin efecto |

### **Restricciones del Movimiento**
- **Direcciones permitidas**: 4 direcciones cardinales (arriba, derecha, abajo, izquierda)
- **Límite de pasos**: Máximo `2n-1` movimientos
- **Posición inicial**: Siempre `(0,0)`
- **Posición objetivo**: Siempre `(n-1,n-1)`

### **Objetivo de Optimización**
**Maximizar** el número total de cápsulas RadAway recolectadas siguiendo un camino válido desde el origen hasta el destino dentro del límite de movimientos.

---

## 🔄 **R - Relación de Recurrencia**

### **Función Principal**
```
f(x, y, t) = máximo número de cápsulas recolectables al estar en posición (x,y) después de t pasos
```

### **Formulación Matemática**
La relación de recurrencia se define como:

```
f(x, y, t) = {
    -∞                           si (x,y) está fuera de límites
    -∞                           si grid[x][y] == 'B' (bomba)
    -∞                           si t > 2n-1 (límite de pasos excedido)
    -∞                           si no es posible llegar a (n-1,n-1) en pasos restantes
    current_value                si x == n-1 AND y == n-1 (destino alcanzado)
    current_value + max{f(nx,ny,t+1) | (nx,ny) ∈ neighbors(x,y)}  en otro caso
}
```

Donde:
- `current_value = 1` si `grid[x][y] == 'R'`, `0` en otro caso
- `neighbors(x,y)` = {(x-1,y), (x+1,y), (x,y-1), (x,y+1)} (4 direcciones cardinales)

### **Poda por Alcanzabilidad**
Se implementa una optimización crucial:
```python
def is_reachable(x, y, t):
    remaining_steps = (2*n-1) - t
    min_distance = |n-1-x| + |n-1-y|  # Distancia Manhattan
    return remaining_steps >= min_distance
```

Esta poda elimina estados desde los cuales es **imposible** llegar al destino en el tiempo restante.

---

## 📊 **T - Tabla de Memoización**

Se implementan **dos estrategias diferentes** de memoización para comparar su eficiencia:

### **1. Array Tridimensional**
```python
dp = [[[None for _ in range(2*n)] for _ in range(n)] for _ in range(n)]
# Acceso: dp[x][y][t]
```

**Características:**
- ✅ **Acceso directo O(1)**
- ✅ **Memoria predecible**
- ❌ **Uso de memoria fijo O(n³)**
- ❌ **Desperdicia memoria en estados no visitados**

### **2. Diccionario Hash**
```python
dp = {}  # Diccionario vacío
# Acceso: dp[(x, y, t)]
```

**Características:**
- ✅ **Memoria proporcional a estados visitados**
- ✅ **Eficiente para problemas dispersos**
- ❌ **Overhead de hash**
- ❌ **Acceso ligeramente más lento**

### **Comparación Teórica**

| Aspecto | Array 3D | Dictionary Hash |
|---------|----------|-----------------|
| **Complejidad Espacial** | O(n³) | O(estados visitados) ≤ O(n³) |
| **Acceso** | O(1) | O(1) promedio |
| **Inicialización** | O(n³) | O(1) |
| **Memoria Real** | Siempre n³ | Variable |

---

## 🏁 **B - Base del Problema**

### **Casos Base Implementados**

1. **🚫 Posición Inválida**
   ```python
   if not (0 <= x < n and 0 <= y < n):
       return -∞
   ```

2. **💣 Bomba Encontrada**
   ```python
   if grid[x][y] == 'B':
       return -∞
   ```

3. **⏰ Límite de Tiempo Excedido**
   ```python
   if t > 2*n-1:
       return -∞
   ```

4. **🎯 Destino Alcanzado**
   ```python
   if x == n-1 and y == n-1:
       return 1 if grid[x][y] == 'R' else 0
   ```

5. **✂️ Poda por Inalcanzabilidad**
   ```python
   if not is_reachable(x, y, t):
       return -∞
   ```

### **Manejo de Estados**
- **Estados válidos**: Se memorizan para evitar recálculos
- **Estados inválidos**: Retornan `-∞` inmediatamente
- **Estados base**: Terminan la recursión con valores concretos

---

## ⚡ **O - Orden del Algoritmo**

### **Complejidad Temporal**
```
T(n) = O(n² × (2n-1) × 4) = O(n³)
```

**Justificación:**
- **n²** posiciones posibles en la cuadrícula
- **(2n-1)** pasos temporales máximos
- **4** direcciones por posición
- **Memoización** evita recálculos: cada estado se calcula **una sola vez**

### **Complejidad Espacial**

| Método | Complejidad | Descripción |
|--------|-------------|-------------|
| **Array 3D** | O(n³) | Espacio fijo para dp[n][n][2n-1] |
| **Dictionary Hash** | O(k) donde k ≤ n³ | Espacio proporcional a estados visitados |
| **Stack de Recursión** | O(n²) | Profundidad máxima de recursión |

### **Análisis de Eficiencia**
- **Sin memoización**: O(4^(2n-1)) - Exponencial
- **Con memoización**: O(n³) - Polinomial
- **Mejora**: Reducción exponencial a polinomial

---

## 🧠 **T - Tipo de Algoritmo**

### **Clasificación: Programación Dinámica Top-Down**

**Características del Enfoque:**
1. **🔄 Recursión con Memoización**: Enfoque descendente (top-down)
2. **📝 Subproblemas Superpuestos**: Estados (x,y,t) se repiten
3. **🎯 Subestructura Óptima**: Solución óptima depende de subsubluciones óptimas
4. **💾 Memoización**: Evita recálculos de subproblemas

### **¿Por qué Programación Dinámica?**

1. **📊 Subproblemas Superpuestos**:
   - Múltiples caminos pueden llevar al mismo estado (x,y,t)
   - Sin memoización se recalcularían repetidamente

2. **🎯 Subestructura Óptima**:
   - El máximo de cápsulas desde (x,y,t) depende del máximo desde estados vecinos
   - `f(x,y,t) = current_value + max{f(vecino, t+1)}`

3. **⚡ Eficiencia**:
   - Reduce complejidad de O(4^(2n-1)) a O(n³)
   - Factible para valores grandes de n

### **Alternativas Consideradas**
- **❌ Fuerza Bruta**: O(4^(2n-1)) - Inviable para n > 10
- **❌ Backtracking**: Sin memoización sigue siendo exponencial
- **✅ Programación Dinámica**: Equilibrio perfecto entre optimalidad y eficiencia

---

## 🚀 **Cómo Ejecutar**

### **Ejecución Básica**
```bash
python Fallout-ada.py
```

### **Menú Interactivo**
Al ejecutar el programa, aparecerá el siguiente menú:

```
======================================================================
       ESCAPE DEL REFUGIO FALLOUT - PROGRAMACIÓN DINÁMICA
======================================================================
Seleccione una opción:
1. Ejecutar experimento para n = 10
2. Ejecutar experimento para n = 20
3. Ejecutar experimento para n = 30
4. Ejecutar experimento para n = 40
5. Ejecutar TODOS los experimentos (n = 10, 20, 30, 40)
6. Salir del programa
----------------------------------------------------------------------
```

### **Opciones de Ejecución**

| Opción | Descripción | Recomendado para |
|--------|-------------|------------------|
| **1-4** | Experimento individual | Análisis específico de un tamaño |
| **5** | Batería completa | **Evaluación académica completa** |
| **6** | Salir | Finalización limpia |

### **Proceso por Experimento**
Para cada tamaño seleccionado:
1. 🎲 **Generación**: 3 cuadrículas aleatorias independientes
2. ⚙️ **Ejecución**: Ambos métodos (Array 3D + Dictionary Hash)
3. 📊 **Medición**: Tiempo, memoria y llamadas recursivas
4. 📈 **Análisis**: Comparación y estadísticas promedio

---

## 📈 **Interpretación de Resultados**

### **Salida por Prueba Individual**
```
📊 RESULTADOS DE LA PRUEBA 1:
🏆 Máximo de cápsulas recolectadas: 12

📈 Comparación de métodos:
Método               Tiempo (s)   Memoria (KB)    Llamadas
-----------------------------------------------------------------
Array 3D             0.001234     1.84            237
Dictionary Hash      0.000987     5.60            237
```

### **Métricas Explicadas**

| Métrica | Descripción | Interpretación |
|---------|-------------|----------------|
| **🏆 Cápsulas** | Resultado óptimo encontrado | Ambos métodos deben dar el mismo valor |
| **⏱️ Tiempo (s)** | Tiempo de ejecución | Menor es mejor |
| **💾 Memoria (KB)** | Pico de uso de memoria | Menor es mejor |
| **📞 Llamadas** | Llamadas recursivas totales | Indica complejidad del problema |

### **Análisis de Eficiencia Final**
```
🔍 ANÁLISIS DE EFICIENCIA:
⚡ Speedup (Array/Dict): 1.25x
💾 Ratio de memoria (Array/Dict): 0.33x
✅ El método con Dictionary Hash es más rápido
✅ El método con Array 3D usa menos memoria
```

### **Interpretación de Speedup y Ratios**
- **Speedup > 1**: Array 3D es más lento que Dictionary Hash
- **Speedup < 1**: Array 3D es más rápido que Dictionary Hash
- **Ratio de memoria < 1**: Array 3D usa menos memoria
- **Ratio de memoria > 1**: Dictionary Hash usa menos memoria

---

## 📦 **Instalación**

### **Requisitos del Sistema**
- **Python**: Versión 3.7 o superior
- **Librerías**: Solo librerías estándar de Python

### **Librerías Utilizadas (Todas Estándar)**
```python
import random      # Generación de cuadrículas aleatorias
import time        # Medición de tiempo de ejecución
import tracemalloc # Medición de uso de memoria
import typing      # Anotaciones de tipos
import sys         # Funcionalidades del sistema
```

### **Verificación de Python**
```bash
# Verificar versión de Python
python --version

# Debe mostrar Python 3.7+ para compatibilidad completa
```

### **No se Requiere Instalación Adicional**
🎉 **El proyecto está listo para ejecutar** inmediatamente después de descargar, sin necesidad de instalar dependencias externas.

---

## 🔬 **Resultados Experimentales**

### **Resumen de Hallazgos**

Basándose en experimentos con cuadrículas aleatorias (20% bombas, 30% RadAway, 50% vacías):

#### **📊 Eficiencia de Memoria**
- **Array 3D**: Consistentemente usa **75-85% menos memoria** que Dictionary Hash
- **Dictionary Hash**: Memoria proporcional a estados visitados
- **Tendencia**: Diferencia se amplifica con n más grandes

#### **⚡ Velocidad de Ejecución**
| Tamaño (n) | Método Más Rápido | Diferencia Promedio |
|------------|-------------------|---------------------|
| **n = 10** | Dictionary Hash | ~1.5x más rápido |
| **n = 20** | Variable | Diferencias mínimas |
| **n = 30** | Array 3D | ~1.2x más rápido |
| **n = 40** | Array 3D | ~1.3x más rápido |

#### **🎯 Recolección de Cápsulas**
- **Promedio recolectado**: ~n/2 cápsulas por experimento
- **Máximo observado**: Hasta 75% de cápsulas disponibles
- **Consistencia**: Ambos métodos siempre producen resultados idénticos

### **📈 Tendencias Observadas**

1. **Escalabilidad**: Ambos métodos escalan O(n³) como se esperaba
2. **Memory Trade-off**: Array 3D sacrifica memoria por velocidad en problemas grandes
3. **Hash Overhead**: Dictionary Hash tiene overhead notable para accesos frecuentes
4. **Poda Efectiva**: La verificación de alcanzabilidad reduce significativamente el espacio de búsqueda

### **🏆 Recomendaciones**

| Escenario | Método Recomendado | Justificación |
|-----------|-------------------|---------------|
| **n ≤ 20** | Dictionary Hash | Menor uso de memoria, velocidad comparable |
| **n > 20** | Array 3D | Mejor velocidad, uso de memoria predecible |
| **Memoria limitada** | Dictionary Hash | Uso proporcional a estados visitados |
| **Velocidad crítica** | Array 3D | Acceso directo O(1) sin overhead |

### **📝 Conclusiones Técnicas**

1. **✅ Programación Dinámica Efectiva**: Reducción de O(4^n) a O(n³)
2. **⚖️ Trade-offs Claros**: Memoria vs. Velocidad según implementación
3. **🎯 Ambos Métodos Viables**: Elección depende de restricciones específicas
4. **📊 Resultados Reproducibles**: Comportamiento consistente across múltiples ejecuciones

---

## 📚 **Referencias y Documentación Adicional**

- **📖 Documentación Técnica**: Ver `MANUAL_USUARIO.md`
- **🔧 Guía de Instalación**: Ver `INSTRUCCIONES.md`
- **📊 Resumen Ejecutivo**: Ver `RESUMEN_EJECUTIVO.md`
