"""
Script de Limpieza de Datos - Dataset de Laptops
Autor: [Tu nombre]
Fecha: [Fecha]

Este script contiene funciones para cargar, limpiar y transformar
el conjunto de datos de laptops para el análisis EDA.
"""

import pandas as pd
import numpy as np
import os
import sys

# Configurar codificación para evitar problemas en Windows
import sys
import codecs
sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())

# Agregar el directorio padre al path para importar módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def cargar_datos(ruta_archivo):
    """
    Carga los datos desde un archivo Excel o CSV
    
    Args:
        ruta_archivo (str): Ruta al archivo de datos
        
    Returns:
        pandas.DataFrame: DataFrame con los datos cargados
    """
    try:
        if ruta_archivo.endswith('.xlsx'):
            df = pd.read_excel(ruta_archivo)
        elif ruta_archivo.endswith('.csv'):
            df = pd.read_csv(ruta_archivo)
        else:
            raise ValueError("Formato de archivo no soportado. Use .xlsx o .csv")
        
        print(f"Datos cargados exitosamente: {df.shape[0]} filas, {df.shape[1]} columnas")
        return df
    
    except Exception as e:
        print(f"Error al cargar los datos: {e}")
        return None

def explorar_datos(df):
    """
    Realiza una exploración inicial de los datos
    
    Args:
        df (pandas.DataFrame): DataFrame a explorar
    """
    print("=" * 50)
    print("EXPLORACIÓN INICIAL DE DATOS")
    print("=" * 50)
    
    print(f"\nDimensiones del dataset: {df.shape}")
    
    print("\nPrimeras 5 filas:")
    print(df.head())
    
    print("\nInformación del dataset:")
    print(df.info())
    
    print("\nEstadísticas descriptivas:")
    print(df.describe())
    
    print("\nValores faltantes por columna:")
    print(df.isnull().sum())
    
    print("\nTipos de datos:")
    print(df.dtypes)

def limpiar_datos(df):
    """
    Limpia y transforma los datos
    
    Args:
        df (pandas.DataFrame): DataFrame original
        
    Returns:
        pandas.DataFrame: DataFrame limpio
    """
    print("=" * 50)
    print("PROCESO DE LIMPIEZA DE DATOS")
    print("=" * 50)
    
    # Crear una copia para no modificar el original
    df_limpio = df.copy()
    
    # 1. Eliminar filas duplicadas
    filas_antes = len(df_limpio)
    df_limpio = df_limpio.drop_duplicates()
    filas_despues = len(df_limpio)
    print(f"Filas duplicadas eliminadas: {filas_antes - filas_despues}")
    
    # 2. Manejar valores faltantes
    print("\nValores faltantes antes de la limpieza:")
    print(df_limpio.isnull().sum())
    
    # Para columnas numéricas, reemplazar con la mediana
    columnas_numericas = df_limpio.select_dtypes(include=[np.number]).columns
    for col in columnas_numericas:
        if df_limpio[col].isnull().sum() > 0:
            mediana = df_limpio[col].median()
            df_limpio[col].fillna(mediana, inplace=True)
            print(f"Valores faltantes en {col} reemplazados con mediana: {mediana}")
    
    # Para columnas categóricas, reemplazar con la moda
    columnas_categoricas = df_limpio.select_dtypes(include=['object']).columns
    for col in columnas_categoricas:
        if df_limpio[col].isnull().sum() > 0:
            moda = df_limpio[col].mode()[0]
            df_limpio[col].fillna(moda, inplace=True)
            try:
                print(f"Valores faltantes en {col} reemplazados con moda: {moda}")
            except UnicodeEncodeError:
                print(f"Valores faltantes en {col} reemplazados con moda")
    
    print("\nValores faltantes después de la limpieza:")
    print(df_limpio.isnull().sum())
    
    # 3. Limpiar nombres de columnas
    df_limpio.columns = df_limpio.columns.str.strip().str.lower().str.replace(' ', '_')
    print(f"\nNombres de columnas normalizados")
    
    # 4. Convertir tipos de datos apropiados
    # Identificar columnas que deberían ser numéricas
    for col in df_limpio.columns:
        if df_limpio[col].dtype == 'object':
            # Intentar convertir a numérico si es posible
            try:
                df_limpio[col] = pd.to_numeric(df_limpio[col], errors='coerce')
                if not df_limpio[col].isnull().all():
                    print(f"Columna {col} convertida a numérica")
            except:
                pass
    
    return df_limpio

def transformar_datos(df):
    """
    Realiza transformaciones adicionales en los datos
    
    Args:
        df (pandas.DataFrame): DataFrame limpio
        
    Returns:
        pandas.DataFrame: DataFrame transformado
    """
    print("=" * 50)
    print("TRANSFORMACIÓN DE DATOS")
    print("=" * 50)
    
    df_transformado = df.copy()
    
    # Crear nuevas variables derivadas si es necesario
    # Por ejemplo, si hay columnas de precio, crear categorías de precio
    
    # Identificar columnas de precio
    columnas_precio = [col for col in df_transformado.columns if 'precio' in col.lower() or 'price' in col.lower()]
    
    if columnas_precio:
        for col in columnas_precio:
            if df_transformado[col].dtype in ['int64', 'float64']:
                try:
                    # Verificar que la columna no esté vacía y tenga valores válidos
                    if not df_transformado[col].isnull().all() and df_transformado[col].nunique() > 1:
                        # Crear categorías de precio usando qcut para evitar errores
                        df_transformado[f'{col}_categoria'] = pd.qcut(
                            df_transformado[col].dropna(),
                            q=5,
                            labels=['Muy Bajo', 'Bajo', 'Medio', 'Alto', 'Muy Alto'],
                            duplicates='drop'
                        )
                        print(f"Categorías de precio creadas para {col}")
                except Exception as e:
                    print(f"No se pudieron crear categorías para {col}: {e}")
    
    # Crear variables dummy para columnas categóricas importantes (solo las primeras 5)
    columnas_categoricas = df_transformado.select_dtypes(include=['object']).columns
    columnas_importantes = [col for col in columnas_categoricas if df_transformado[col].nunique() <= 10][:5]
    
    for col in columnas_importantes:
        try:
            dummies = pd.get_dummies(df_transformado[col], prefix=col, drop_first=True)
            df_transformado = pd.concat([df_transformado, dummies], axis=1)
            print(f"Variables dummy creadas para {col}")
        except Exception as e:
            print(f"No se pudieron crear variables dummy para {col}: {e}")
    
    return df_transformado

def guardar_datos_limpios(df, ruta_salida):
    """
    Guarda los datos limpios en formato CSV
    
    Args:
        df (pandas.DataFrame): DataFrame limpio
        ruta_salida (str): Ruta donde guardar el archivo
    """
    try:
        df.to_csv(ruta_salida, index=False)
        print(f"Datos limpios guardados en: {ruta_salida}")
    except Exception as e:
        print(f"Error al guardar los datos: {e}")

def main():
    """
    Función principal que ejecuta todo el proceso de limpieza
    """
    # Rutas de archivos
    ruta_datos = "../data/laptop.xlsx"
    ruta_salida = "../data/laptop_limpio.csv"
    
    print("INICIANDO PROCESO DE LIMPIEZA DE DATOS")
    print("=" * 50)
    
    # 1. Cargar datos
    df = cargar_datos(ruta_datos)
    if df is None:
        return
    
    # 2. Explorar datos originales
    explorar_datos(df)
    
    # 3. Limpiar datos
    df_limpio = limpiar_datos(df)
    
    # 4. Transformar datos
    df_final = transformar_datos(df_limpio)
    
    # 5. Guardar datos limpios
    guardar_datos_limpios(df_final, ruta_salida)
    
    print("\n" + "=" * 50)
    print("PROCESO DE LIMPIEZA COMPLETADO")
    print("=" * 50)
    print(f"Dataset original: {df.shape}")
    print(f"Dataset final: {df_final.shape}")

if __name__ == "__main__":
    main() 