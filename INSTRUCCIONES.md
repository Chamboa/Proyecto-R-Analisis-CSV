# 📋 Instrucciones de Uso - Proyecto EDA

## 🚀 Inicio Rápido

### 1. Instalación de Dependencias

```bash
# Instalar todas las librerías necesarias
pip install -r requirements.txt
```

### 2. Ejecutar Análisis Completo

```bash
# Ejecutar todo el análisis de forma automatizada
python run_analysis.py
```

### 3. Ver Resultados

- **Reporte ejecutivo**: Abrir `reports/EDA_Report.html` en tu navegador
- **Análisis detallado**: Abrir `notebooks/EDA_Laptops.ipynb` con Jupyter
- **Visualizaciones**: Ver archivos en `reports/images/`

## 📁 Estructura del Proyecto

```
Proyecto EDA/
├── data/                    # Datos originales y procesados
│   ├── laptop.xlsx         # Dataset original
│   ├── laptop.csv          # Dataset en CSV
│   └── laptop_limpio.csv   # Datos limpios (generado)
├── notebooks/              # Jupyter notebooks
│   └── EDA_Laptops.ipynb   # Notebook principal
├── reports/                # Reportes y visualizaciones
│   ├── images/             # Gráficos generados
│   └── EDA_Report.html     # Reporte HTML
├── scripts/                # Scripts de Python
│   ├── data_cleaning.py    # Limpieza de datos
│   ├── data_analysis.py    # Análisis estadístico
│   └── visualizations.py   # Generación de gráficos
├── requirements.txt        # Dependencias
├── run_analysis.py         # Script principal
├── README.md              # Documentación
├── INSTRUCCIONES.md       # Este archivo
└── .gitignore             # Archivos a ignorar
```

## 🔧 Uso de Scripts Individuales

### Limpieza de Datos

```bash
cd scripts
python data_cleaning.py
```

**Funciones principales:**
- Carga de datos desde Excel/CSV
- Eliminación de duplicados
- Manejo de valores faltantes
- Normalización de nombres de columnas
- Conversión de tipos de datos

### Análisis Estadístico

```bash
cd scripts
python data_analysis.py
```

**Funciones principales:**
- Resumen estadístico completo
- Análisis de distribuciones
- Detección de outliers
- Análisis de correlaciones
- Análisis de variables categóricas
- Generación de insights automáticos

### Visualizaciones

```bash
cd scripts
python visualizations.py
```

**Funciones principales:**
- Gráficos de distribución
- Matriz de correlaciones
- Análisis de variables categóricas
- Gráficos de caja para outliers
- Visualizaciones interactivas con Plotly
- Gráficos de valores faltantes

## 📊 Uso del Notebook

### Abrir Jupyter Notebook

```bash
# Desde el directorio raíz del proyecto
jupyter notebook notebooks/EDA_Laptops.ipynb
```

### Contenido del Notebook

1. **Configuración inicial** - Importación de librerías
2. **Carga de datos** - Lectura del dataset
3. **Exploración inicial** - Información básica
4. **Limpieza y transformación** - Procesamiento de datos
5. **Análisis de variables numéricas** - Estadísticas descriptivas
6. **Análisis de variables categóricas** - Frecuencias y diversidad
7. **Análisis de correlaciones** - Relaciones entre variables
8. **Visualizaciones** - Gráficos informativos
9. **Análisis de relaciones específicas** - Casos particulares
10. **Visualizaciones interactivas** - Gráficos con Plotly
11. **Conclusiones** - Hallazgos principales
12. **Recomendaciones** - Próximos pasos
13. **Guardado de datos** - Datos procesados

## 🎯 Personalización

### Modificar el Dataset

1. Reemplaza `data/laptop.xlsx` con tu propio dataset
2. Ajusta las rutas en los scripts si es necesario
3. Modifica las funciones de limpieza según tus necesidades

### Agregar Nuevas Visualizaciones

1. Edita `scripts/visualizations.py`
2. Agrega nuevas funciones de gráficos
3. Llama las funciones desde `run_analysis.py`

### Personalizar el Análisis

1. Modifica `scripts/data_analysis.py`
2. Agrega nuevas métricas o análisis
3. Actualiza el reporte HTML en `run_analysis.py`

## 🔍 Solución de Problemas

### Error: "No se encontró el archivo laptop.xlsx"

- Verifica que el archivo esté en `data/laptop.xlsx`
- Asegúrate de estar en el directorio raíz del proyecto

### Error: "ModuleNotFoundError"

- Instala las dependencias: `pip install -r requirements.txt`
- Verifica que estés usando Python 3.7+

### Error: "Permission denied"

- En Windows: Ejecuta PowerShell como administrador
- En Linux/Mac: Usa `chmod +x run_analysis.py`

### Gráficos no se muestran

- Verifica que matplotlib esté instalado correctamente
- En entornos sin GUI, los gráficos se guardan automáticamente

## 📈 Interpretación de Resultados

### Estadísticas Descriptivas

- **Media**: Valor promedio
- **Mediana**: Valor central
- **Desviación estándar**: Dispersión de los datos
- **Asimetría**: Sesgo de la distribución
- **Curtosis**: Concentración de datos

### Correlaciones

- **0.0 a 0.3**: Correlación débil
- **0.3 a 0.7**: Correlación moderada
- **0.7 a 1.0**: Correlación fuerte

### Outliers

- Detectados usando el método IQR
- Valores fuera del rango Q1-1.5*IQR a Q3+1.5*IQR

## 🚀 Próximos Pasos

1. **Análisis más profundo**: Investigar relaciones específicas
2. **Modelado**: Desarrollar modelos predictivos
3. **Segmentación**: Identificar grupos de datos
4. **Optimización**: Aplicar técnicas de optimización
5. **Automatización**: Crear pipelines de análisis

## 📞 Soporte

Si tienes problemas o preguntas:

1. Revisa este archivo de instrucciones
2. Consulta el README.md
3. Revisa los comentarios en los scripts
4. Verifica que todas las dependencias estén instaladas

---

**¡Disfruta explorando tus datos! 🎉** 