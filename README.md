# Análisis Exploratorio de Datos 📊

Esta librería permite realizar un Análisis Exploratorio de Datos (EDA) de forma rápida y automática.
Incluye funciones para identificar missing values, separar variables por tipo, visualizar categorías, y generar un reporte PDF con gráficos y tablas estadísticas.
---

### ⚙️ ¿Cómo se instala?
#### 📌📁 Ruta de la carpeta:```C:\Users\xyz\Downloads\edaf``` (cambiar por la ruda donde se descargó y descomprimió el archivo)

- 1° Descargar el .zip
- 2° Descomprimir el archivo
- 3° Instalar con pip desde la terminal (VSCode, PowerShell o CMD):

   ```python
   pip install C:\Users\xyz\Downloads\edaf-main
   ```
   Opción 2:
  
   ```python
   pip install C:\Users\xyz\Downloads\edaf-main\edaf-main
   ```
---
## 🚀 ¿Cómo se utiliza?

   ```python
   import edaf
from edaf import contador_de_missing, variables_categoricas, variables_numericas, mostrar_value_counts, edafreport
   ```

 ## Funciones:

##❓ contador_de_missing:
Muestra solo las variables que contienen missing values en un Data Frame.

```python
contador_de_missing(df)
```

## ⚠️ variables_categoricas:

Muestra las variables tipo object y bool de un Data Frame

```python
df_cat = variables_categoricas(df)
```

## 📈 Variables_numericas:
  
Muestra las variables tipo object y bool de un Data Frame

```python
EDA = variables_numericas(df)
```

## 🧩 mostrar_value_counts:

Muestra la cantidad de categorías en número y % en df_cat

```python
mostrar_value_counts(df_cat)
```

## 📚 edafreport:

Genera un reporte en PDF con un Boxplot, un Histograma o un KDE, una tabla descriptiva, una tabla de resumen de variables y un gráfico QQplot

```python
edafreport(df, 'c:/usuario/xyz/Proyecto1/ReporteEDA.pdf')
```






