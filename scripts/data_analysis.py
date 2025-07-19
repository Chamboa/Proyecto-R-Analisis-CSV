"""
Script de Análisis Estadístico - Dataset de Laptops
Autor: [Tu nombre]
Fecha: [Fecha]

Este script contiene funciones para realizar análisis estadístico
y exploratorio del conjunto de datos de laptops.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# Configurar estilo de gráficos
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

def resumen_estadistico(df):
    """
    Genera un resumen estadístico completo del dataset
    
    Args:
        df (pandas.DataFrame): DataFrame a analizar
        
    Returns:
        dict: Diccionario con estadísticas resumidas
    """
    print("=" * 60)
    print("RESUMEN ESTADÍSTICO COMPLETO")
    print("=" * 60)
    
    resumen = {}
    
    # Información básica
    resumen['dimensiones'] = df.shape
    resumen['columnas'] = list(df.columns)
    resumen['tipos_datos'] = df.dtypes.to_dict()
    
    # Estadísticas descriptivas
    resumen['estadisticas_descriptivas'] = df.describe()
    
    # Información de valores faltantes
    resumen['valores_faltantes'] = df.isnull().sum().to_dict()
    resumen['porcentaje_faltantes'] = (df.isnull().sum() / len(df) * 100).to_dict()
    
    # Información de columnas numéricas
    columnas_numericas = df.select_dtypes(include=[np.number]).columns
    resumen['columnas_numericas'] = list(columnas_numericas)
    
    # Información de columnas categóricas
    columnas_categoricas = df.select_dtypes(include=['object']).columns
    resumen['columnas_categoricas'] = list(columnas_categoricas)
    
    # Estadísticas por tipo de columna
    if len(columnas_numericas) > 0:
        print("\nESTADÍSTICAS DE COLUMNAS NUMÉRICAS:")
        print(df[columnas_numericas].describe())
        
        # Detectar outliers usando IQR
        outliers_info = {}
        for col in columnas_numericas:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            outliers = df[(df[col] < Q1 - 1.5*IQR) | (df[col] > Q3 + 1.5*IQR)]
            outliers_info[col] = len(outliers)
        
        resumen['outliers'] = outliers_info
        print(f"\nOUTLIERS DETECTADOS (método IQR):")
        for col, count in outliers_info.items():
            print(f"{col}: {count} outliers")
    
    if len(columnas_categoricas) > 0:
        print("\nINFORMACIÓN DE COLUMNAS CATEGÓRICAS:")
        for col in columnas_categoricas:
            print(f"\n{col}:")
            print(f"  Valores únicos: {df[col].nunique()}")
            print(f"  Top 5 valores más frecuentes:")
            print(df[col].value_counts().head())
    
    return resumen

def analizar_distribuciones(df, columnas_numericas=None):
    """
    Analiza las distribuciones de las variables numéricas
    
    Args:
        df (pandas.DataFrame): DataFrame a analizar
        columnas_numericas (list): Lista de columnas numéricas a analizar
    """
    if columnas_numericas is None:
        columnas_numericas = df.select_dtypes(include=[np.number]).columns
    
    print("=" * 60)
    print("ANÁLISIS DE DISTRIBUCIONES")
    print("=" * 60)
    
    for col in columnas_numericas:
        print(f"\nANÁLISIS DE DISTRIBUCIÓN: {col}")
        print("-" * 40)
        
        # Estadísticas básicas
        media = df[col].mean()
        mediana = df[col].median()
        moda = df[col].mode()[0] if len(df[col].mode()) > 0 else "No hay moda única"
        desv_std = df[col].std()
        varianza = df[col].var()
        skewness = df[col].skew()
        kurtosis = df[col].kurtosis()
        
        print(f"Media: {media:.2f}")
        print(f"Mediana: {mediana:.2f}")
        print(f"Moda: {moda}")
        print(f"Desviación estándar: {desv_std:.2f}")
        print(f"Varianza: {varianza:.2f}")
        print(f"Asimetría (Skewness): {skewness:.2f}")
        print(f"Curtosis: {kurtosis:.2f}")
        
        # Interpretación de asimetría
        if abs(skewness) < 0.5:
            print("Distribución aproximadamente simétrica")
        elif skewness > 0.5:
            print("Distribución asimétrica positiva (sesgada a la derecha)")
        else:
            print("Distribución asimétrica negativa (sesgada a la izquierda)")
        
        # Interpretación de curtosis
        if abs(kurtosis) < 2:
            print("Distribución mesocúrtica (normal)")
        elif kurtosis > 2:
            print("Distribución leptocúrtica (picos más agudos)")
        else:
            print("Distribución platicúrtica (picos más planos)")

def analizar_correlaciones(df, columnas_numericas=None):
    """
    Analiza las correlaciones entre variables numéricas
    
    Args:
        df (pandas.DataFrame): DataFrame a analizar
        columnas_numericas (list): Lista de columnas numéricas a analizar
        
    Returns:
        pandas.DataFrame: Matriz de correlaciones
    """
    if columnas_numericas is None:
        columnas_numericas = df.select_dtypes(include=[np.number]).columns
    
    print("=" * 60)
    print("ANÁLISIS DE CORRELACIONES")
    print("=" * 60)
    
    # Calcular matriz de correlaciones
    matriz_corr = df[columnas_numericas].corr()
    
    print("\nMatriz de correlaciones:")
    print(matriz_corr.round(3))
    
    # Encontrar correlaciones más fuertes
    print("\nCORRELACIONES MÁS FUERTES:")
    correlaciones_fuertes = []
    
    for i in range(len(matriz_corr.columns)):
        for j in range(i+1, len(matriz_corr.columns)):
            corr_valor = matriz_corr.iloc[i, j]
            if abs(corr_valor) > 0.5:  # Correlación moderada o fuerte
                correlaciones_fuertes.append({
                    'variable1': matriz_corr.columns[i],
                    'variable2': matriz_corr.columns[j],
                    'correlacion': corr_valor
                })
    
    # Ordenar por valor absoluto de correlación
    correlaciones_fuertes.sort(key=lambda x: abs(x['correlacion']), reverse=True)
    
    for corr in correlaciones_fuertes:
        print(f"{corr['variable1']} - {corr['variable2']}: {corr['correlacion']:.3f}")
    
    return matriz_corr

def analizar_categoricas(df, columnas_categoricas=None):
    """
    Analiza las variables categóricas
    
    Args:
        df (pandas.DataFrame): DataFrame a analizar
        columnas_categoricas (list): Lista de columnas categóricas a analizar
    """
    if columnas_categoricas is None:
        columnas_categoricas = df.select_dtypes(include=['object']).columns
    
    print("=" * 60)
    print("ANÁLISIS DE VARIABLES CATEGÓRICAS")
    print("=" * 60)
    
    for col in columnas_categoricas:
        print(f"\nANÁLISIS DE: {col}")
        print("-" * 40)
        
        # Frecuencias
        frecuencias = df[col].value_counts()
        frecuencias_relativas = df[col].value_counts(normalize=True) * 100
        
        print("Frecuencias absolutas:")
        print(frecuencias)
        
        print("\nFrecuencias relativas (%):")
        print(frecuencias_relativas.round(2))
        
        # Estadísticas de diversidad
        n_categorias = df[col].nunique()
        entropia = stats.entropy(frecuencias)
        
        print(f"\nNúmero de categorías: {n_categorias}")
        print(f"Entropía: {entropia:.3f}")
        
        # Interpretación de entropía
        if entropia < 1:
            print("Baja diversidad (concentración en pocas categorías)")
        elif entropia < 2:
            print("Diversidad moderada")
        else:
            print("Alta diversidad (distribución más uniforme)")

def detectar_patrones_temporales(df, columna_fecha=None):
    """
    Detecta patrones temporales si existe una columna de fecha
    
    Args:
        df (pandas.DataFrame): DataFrame a analizar
        columna_fecha (str): Nombre de la columna de fecha
    """
    if columna_fecha is None:
        # Buscar columnas que podrían ser fechas
        posibles_fechas = [col for col in df.columns if 'fecha' in col.lower() or 
                          'date' in col.lower() or 'time' in col.lower()]
        if posibles_fechas:
            columna_fecha = posibles_fechas[0]
    
    if columna_fecha and columna_fecha in df.columns:
        print("=" * 60)
        print("ANÁLISIS TEMPORAL")
        print("=" * 60)
        
        try:
            # Convertir a datetime
            df[columna_fecha] = pd.to_datetime(df[columna_fecha])
            
            # Extraer componentes temporales
            df['año'] = df[columna_fecha].dt.year
            df['mes'] = df[columna_fecha].dt.month
            df['dia_semana'] = df[columna_fecha].dt.dayofweek
            
            print(f"Rango temporal: {df[columna_fecha].min()} a {df[columna_fecha].max()}")
            print(f"Total de días: {(df[columna_fecha].max() - df[columna_fecha].min()).days}")
            
            # Análisis por año
            print("\nDistribución por año:")
            print(df['año'].value_counts().sort_index())
            
            # Análisis por mes
            print("\nDistribución por mes:")
            print(df['mes'].value_counts().sort_index())
            
        except Exception as e:
            print(f"No se pudo realizar análisis temporal: {e}")

def generar_insights(df, resumen):
    """
    Genera insights automáticos basados en el análisis
    
    Args:
        df (pandas.DataFrame): DataFrame analizado
        resumen (dict): Resumen estadístico del análisis
    """
    print("=" * 60)
    print("INSIGHTS Y OBSERVACIONES CLAVE")
    print("=" * 60)
    
    insights = []
    
    # Insights sobre el tamaño del dataset
    filas, columnas = resumen['dimensiones']
    insights.append(f"El dataset contiene {filas} observaciones y {columnas} variables")
    
    # Insights sobre valores faltantes
    total_faltantes = sum(resumen['valores_faltantes'].values())
    if total_faltantes > 0:
        insights.append(f"Hay {total_faltantes} valores faltantes en total")
        columnas_con_faltantes = [col for col, count in resumen['valores_faltantes'].items() if count > 0]
        insights.append(f"Columnas con valores faltantes: {', '.join(columnas_con_faltantes)}")
    else:
        insights.append("No hay valores faltantes en el dataset")
    
    # Insights sobre tipos de datos
    num_numericas = len(resumen['columnas_numericas'])
    num_categoricas = len(resumen['columnas_categoricas'])
    insights.append(f"El dataset tiene {num_numericas} variables numéricas y {num_categoricas} categóricas")
    
    # Insights sobre outliers
    if 'outliers' in resumen:
        total_outliers = sum(resumen['outliers'].values())
        if total_outliers > 0:
            insights.append(f"Se detectaron {total_outliers} outliers en total")
            col_con_mas_outliers = max(resumen['outliers'].items(), key=lambda x: x[1])
            insights.append(f"La variable con más outliers es {col_con_mas_outliers[0]} ({col_con_mas_outliers[1]} outliers)")
    
    # Imprimir insights
    for i, insight in enumerate(insights, 1):
        print(f"{i}. {insight}")
    
    return insights

def main():
    """
    Función principal que ejecuta todo el análisis estadístico
    """
    # Cargar datos limpios
    try:
        df = pd.read_csv("../data/laptop_limpio.csv")
        print("Datos cargados exitosamente para análisis")
    except FileNotFoundError:
        print("Error: No se encontró el archivo laptop_limpio.csv")
        print("Ejecuta primero el script de limpieza de datos")
        return
    
    # Ejecutar análisis completo
    resumen = resumen_estadistico(df)
    analizar_distribuciones(df)
    matriz_corr = analizar_correlaciones(df)
    analizar_categoricas(df)
    detectar_patrones_temporales(df)
    insights = generar_insights(df, resumen)
    
    print("\n" + "=" * 60)
    print("ANÁLISIS ESTADÍSTICO COMPLETADO")
    print("=" * 60)

if __name__ == "__main__":
    main() 