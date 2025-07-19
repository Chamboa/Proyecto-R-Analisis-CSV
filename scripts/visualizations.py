"""
Script de Visualizaciones - Dataset de Laptops
Autor: [Tu nombre]
Fecha: [Fecha]

Este script contiene funciones para crear visualizaciones
informativas del análisis exploratorio de datos.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

# Configurar estilo de gráficos
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

# Configurar matplotlib para español
plt.rcParams['font.size'] = 10
plt.rcParams['axes.titlesize'] = 12
plt.rcParams['axes.labelsize'] = 10

def configurar_estilo():
    """
    Configura el estilo de los gráficos
    """
    # Configurar estilo de seaborn
    sns.set_style("whitegrid")
    sns.set_palette("husl")
    
    # Configurar matplotlib
    plt.rcParams['figure.figsize'] = (12, 8)
    plt.rcParams['font.size'] = 10
    plt.rcParams['axes.titlesize'] = 14
    plt.rcParams['axes.labelsize'] = 12
    plt.rcParams['xtick.labelsize'] = 10
    plt.rcParams['ytick.labelsize'] = 10

def grafico_distribucion_numericas(df, columnas_numericas=None, max_graficos=6):
    """
    Crea gráficos de distribución para variables numéricas
    
    Args:
        df (pandas.DataFrame): DataFrame a visualizar
        columnas_numericas (list): Lista de columnas numéricas
        max_graficos (int): Máximo número de gráficos a mostrar
    """
    if columnas_numericas is None:
        columnas_numericas = df.select_dtypes(include=[np.number]).columns
    
    # Limitar número de gráficos
    columnas_numericas = columnas_numericas[:max_graficos]
    
    n_cols = min(3, len(columnas_numericas))
    n_rows = (len(columnas_numericas) + n_cols - 1) // n_cols
    
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(15, 5*n_rows))
    fig.suptitle('Distribuciones de Variables Numéricas', fontsize=16, fontweight='bold')
    
    if len(columnas_numericas) == 1:
        axes = [axes]
    elif n_rows == 1:
        axes = axes.reshape(1, -1)
    
    for i, col in enumerate(columnas_numericas):
        row = i // n_cols
        col_idx = i % n_cols
        
        if n_rows == 1:
            ax = axes[col_idx]
        else:
            ax = axes[row, col_idx]
        
        # Histograma con curva de densidad
        sns.histplot(data=df, x=col, kde=True, ax=ax, bins=30)
        ax.set_title(f'Distribución de {col}')
        ax.set_xlabel(col)
        ax.set_ylabel('Frecuencia')
        
        # Agregar estadísticas en el gráfico
        media = df[col].mean()
        mediana = df[col].median()
        ax.axvline(media, color='red', linestyle='--', alpha=0.7, label=f'Media: {media:.2f}')
        ax.axvline(mediana, color='green', linestyle='--', alpha=0.7, label=f'Mediana: {mediana:.2f}')
        ax.legend()
    
    # Ocultar ejes vacíos
    for i in range(len(columnas_numericas), n_rows * n_cols):
        row = i // n_cols
        col_idx = i % n_cols
        if n_rows == 1:
            axes[col_idx].set_visible(False)
        else:
            axes[row, col_idx].set_visible(False)
    
    plt.tight_layout()
    plt.savefig('../reports/images/distribuciones_numericas.png', dpi=300, bbox_inches='tight')
    plt.show()

def grafico_correlaciones(df, columnas_numericas=None):
    """
    Crea un mapa de calor de correlaciones
    
    Args:
        df (pandas.DataFrame): DataFrame a visualizar
        columnas_numericas (list): Lista de columnas numéricas
    """
    if columnas_numericas is None:
        columnas_numericas = df.select_dtypes(include=[np.number]).columns
    
    # Calcular matriz de correlaciones
    matriz_corr = df[columnas_numericas].corr()
    
    # Crear mapa de calor
    plt.figure(figsize=(12, 10))
    mask = np.triu(np.ones_like(matriz_corr, dtype=bool))
    
    sns.heatmap(matriz_corr, 
                mask=mask,
                annot=True, 
                cmap='coolwarm', 
                center=0,
                square=True,
                fmt='.2f',
                cbar_kws={"shrink": .8})
    
    plt.title('Matriz de Correlaciones', fontsize=16, fontweight='bold', pad=20)
    plt.tight_layout()
    plt.savefig('../reports/images/matriz_correlaciones.png', dpi=300, bbox_inches='tight')
    plt.show()

def grafico_categoricas(df, columnas_categoricas=None, max_graficos=6):
    """
    Crea gráficos para variables categóricas
    
    Args:
        df (pandas.DataFrame): DataFrame a visualizar
        columnas_categoricas (list): Lista de columnas categóricas
        max_graficos (int): Máximo número de gráficos a mostrar
    """
    if columnas_categoricas is None:
        columnas_categoricas = df.select_dtypes(include=['object']).columns
    
    # Verificar si hay columnas categóricas
    if len(columnas_categoricas) == 0:
        print("No hay variables categóricas para visualizar")
        return
    
    # Limitar número de gráficos
    columnas_categoricas = columnas_categoricas[:max_graficos]
    
    n_cols = min(2, len(columnas_categoricas))
    n_rows = (len(columnas_categoricas) + n_cols - 1) // n_cols
    
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(15, 6*n_rows))
    fig.suptitle('Análisis de Variables Categóricas', fontsize=16, fontweight='bold')
    
    if len(columnas_categoricas) == 1:
        axes = [axes]
    elif n_rows == 1:
        axes = axes.reshape(1, -1)
    
    for i, col in enumerate(columnas_categoricas):
        row = i // n_cols
        col_idx = i % n_cols
        
        if n_rows == 1:
            ax = axes[col_idx]
        else:
            ax = axes[row, col_idx]
        
        # Gráfico de barras
        valores = df[col].value_counts().head(10)  # Top 10 valores
        sns.barplot(x=valores.values, y=valores.index, ax=ax)
        ax.set_title(f'Top 10 valores de {col}')
        ax.set_xlabel('Frecuencia')
        ax.set_ylabel(col)
        
        # Rotar etiquetas si son muy largas
        if len(valores.index[0]) > 15:
            ax.tick_params(axis='y', rotation=45)
    
    # Ocultar ejes vacíos
    for i in range(len(columnas_categoricas), n_rows * n_cols):
        row = i // n_cols
        col_idx = i % n_cols
        if n_rows == 1:
            axes[col_idx].set_visible(False)
        else:
            axes[row, col_idx].set_visible(False)
    
    plt.tight_layout()
    plt.savefig('../reports/images/analisis_categoricas.png', dpi=300, bbox_inches='tight')
    plt.show()

def grafico_boxplot(df, columnas_numericas=None, max_graficos=6):
    """
    Crea gráficos de caja para detectar outliers
    
    Args:
        df (pandas.DataFrame): DataFrame a visualizar
        columnas_numericas (list): Lista de columnas numéricas
        max_graficos (int): Máximo número de gráficos a mostrar
    """
    if columnas_numericas is None:
        columnas_numericas = df.select_dtypes(include=[np.number]).columns
    
    # Limitar número de gráficos
    columnas_numericas = columnas_numericas[:max_graficos]
    
    n_cols = min(3, len(columnas_numericas))
    n_rows = (len(columnas_numericas) + n_cols - 1) // n_cols
    
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(15, 5*n_rows))
    fig.suptitle('Análisis de Outliers - Gráficos de Caja', fontsize=16, fontweight='bold')
    
    if len(columnas_numericas) == 1:
        axes = [axes]
    elif n_rows == 1:
        axes = axes.reshape(1, -1)
    
    for i, col in enumerate(columnas_numericas):
        row = i // n_cols
        col_idx = i % n_cols
        
        if n_rows == 1:
            ax = axes[col_idx]
        else:
            ax = axes[row, col_idx]
        
        # Gráfico de caja
        sns.boxplot(data=df, y=col, ax=ax)
        ax.set_title(f'Boxplot de {col}')
        ax.set_ylabel(col)
        
        # Agregar estadísticas
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        outliers = df[(df[col] < Q1 - 1.5*IQR) | (df[col] > Q3 + 1.5*IQR)]
        
        ax.text(0.02, 0.98, f'Outliers: {len(outliers)}', 
                transform=ax.transAxes, verticalalignment='top',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    # Ocultar ejes vacíos
    for i in range(len(columnas_numericas), n_rows * n_cols):
        row = i // n_cols
        col_idx = i % n_cols
        if n_rows == 1:
            axes[col_idx].set_visible(False)
        else:
            axes[row, col_idx].set_visible(False)
    
    plt.tight_layout()
    plt.savefig('../reports/images/boxplots_outliers.png', dpi=300, bbox_inches='tight')
    plt.show()

def grafico_dispersion(df, col_x, col_y):
    """
    Crea gráfico de dispersión entre dos variables
    
    Args:
        df (pandas.DataFrame): DataFrame a visualizar
        col_x (str): Variable del eje X
        col_y (str): Variable del eje Y
    """
    plt.figure(figsize=(10, 8))
    
    # Gráfico de dispersión
    sns.scatterplot(data=df, x=col_x, y=col_y, alpha=0.6)
    
    # Línea de regresión
    sns.regplot(data=df, x=col_x, y=col_y, scatter=False, color='red')
    
    # Calcular correlación
    correlacion = df[col_x].corr(df[col_y])
    
    plt.title(f'Relación entre {col_x} y {col_y}\nCorrelación: {correlacion:.3f}', 
              fontsize=14, fontweight='bold')
    plt.xlabel(col_x)
    plt.ylabel(col_y)
    
    plt.tight_layout()
    plt.savefig(f'../reports/images/dispersion_{col_x}_{col_y}.png', dpi=300, bbox_inches='tight')
    plt.show()

def grafico_valores_faltantes(df):
    """
    Crea gráfico de valores faltantes
    
    Args:
        df (pandas.DataFrame): DataFrame a visualizar
    """
    # Calcular valores faltantes
    valores_faltantes = df.isnull().sum()
    porcentaje_faltantes = (valores_faltantes / len(df)) * 100
    
    # Crear DataFrame para visualización
    df_faltantes = pd.DataFrame({
        'Columna': valores_faltantes.index,
        'Valores_Faltantes': valores_faltantes.values,
        'Porcentaje': porcentaje_faltantes.values
    }).sort_values('Valores_Faltantes', ascending=False)
    
    # Filtrar solo columnas con valores faltantes
    df_faltantes = df_faltantes[df_faltantes['Valores_Faltantes'] > 0]
    
    if len(df_faltantes) == 0:
        print("No hay valores faltantes en el dataset")
        return
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # Gráfico de barras - valores absolutos
    sns.barplot(data=df_faltantes, x='Valores_Faltantes', y='Columna', ax=ax1)
    ax1.set_title('Valores Faltantes por Columna', fontweight='bold')
    ax1.set_xlabel('Cantidad de Valores Faltantes')
    
    # Gráfico de barras - porcentajes
    sns.barplot(data=df_faltantes, x='Porcentaje', y='Columna', ax=ax2)
    ax2.set_title('Porcentaje de Valores Faltantes por Columna', fontweight='bold')
    ax2.set_xlabel('Porcentaje (%)')
    
    plt.tight_layout()
    plt.savefig('../reports/images/valores_faltantes.png', dpi=300, bbox_inches='tight')
    plt.show()

def grafico_resumen_estadistico(df, columnas_numericas=None):
    """
    Crea un gráfico resumen de estadísticas descriptivas
    
    Args:
        df (pandas.DataFrame): DataFrame a visualizar
        columnas_numericas (list): Lista de columnas numéricas
    """
    if columnas_numericas is None:
        columnas_numericas = df.select_dtypes(include=[np.number]).columns
    
    # Calcular estadísticas
    stats_df = df[columnas_numericas].describe().T
    stats_df['CV'] = stats_df['std'] / stats_df['mean']  # Coeficiente de variación
    
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle('Resumen Estadístico de Variables Numéricas', fontsize=16, fontweight='bold')
    
    # 1. Medias
    axes[0, 0].bar(stats_df.index, stats_df['mean'])
    axes[0, 0].set_title('Medias por Variable')
    axes[0, 0].tick_params(axis='x', rotation=45)
    
    # 2. Desviaciones estándar
    axes[0, 1].bar(stats_df.index, stats_df['std'])
    axes[0, 1].set_title('Desviaciones Estándar por Variable')
    axes[0, 1].tick_params(axis='x', rotation=45)
    
    # 3. Coeficientes de variación
    axes[1, 0].bar(stats_df.index, stats_df['CV'])
    axes[1, 0].set_title('Coeficientes de Variación por Variable')
    axes[1, 0].tick_params(axis='x', rotation=45)
    
    # 4. Rango (max - min)
    rango = stats_df['max'] - stats_df['min']
    axes[1, 1].bar(stats_df.index, rango)
    axes[1, 1].set_title('Rango por Variable')
    axes[1, 1].tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    plt.savefig('../reports/images/resumen_estadistico.png', dpi=300, bbox_inches='tight')
    plt.show()

def crear_visualizaciones_interactivas(df, columnas_numericas=None):
    """
    Crea visualizaciones interactivas con Plotly
    
    Args:
        df (pandas.DataFrame): DataFrame a visualizar
        columnas_numericas (list): Lista de columnas numéricas
    """
    if columnas_numericas is None:
        columnas_numericas = df.select_dtypes(include=[np.number]).columns
    
    # 1. Matriz de correlaciones interactiva
    matriz_corr = df[columnas_numericas].corr()
    
    fig_corr = px.imshow(matriz_corr,
                         text_auto=True,
                         aspect="auto",
                         title="Matriz de Correlaciones Interactiva")
    fig_corr.write_html("../reports/correlaciones_interactivo.html")
    
    # 2. Gráfico de dispersión 3D (si hay al menos 3 variables numéricas)
    if len(columnas_numericas) >= 3:
        fig_3d = px.scatter_3d(df, 
                               x=columnas_numericas[0], 
                               y=columnas_numericas[1], 
                               z=columnas_numericas[2],
                               title="Gráfico de Dispersión 3D")
        fig_3d.write_html("../reports/dispersion_3d.html")
    
    # 3. Histogramas interactivos
    fig_hist = make_subplots(rows=len(columnas_numericas), cols=1,
                             subplot_titles=columnas_numericas)
    
    for i, col in enumerate(columnas_numericas, 1):
        fig_hist.add_trace(go.Histogram(x=df[col], name=col), row=i, col=1)
    
    fig_hist.update_layout(height=300*len(columnas_numericas), 
                          title_text="Histogramas Interactivos")
    fig_hist.write_html("../reports/histogramas_interactivos.html")
    
    print("Visualizaciones interactivas guardadas en la carpeta reports/")

def main():
    """
    Función principal que ejecuta todas las visualizaciones
    """
    # Configurar estilo
    configurar_estilo()
    
    # Cargar datos limpios
    try:
        df = pd.read_csv("../data/laptop_limpio.csv")
        print("Datos cargados exitosamente para visualización")
    except FileNotFoundError:
        print("Error: No se encontró el archivo laptop_limpio.csv")
        print("Ejecuta primero el script de limpieza de datos")
        return
    
    print("=" * 60)
    print("GENERANDO VISUALIZACIONES")
    print("=" * 60)
    
    # Crear carpeta de imágenes si no existe
    import os
    os.makedirs("../reports/images", exist_ok=True)
    
    # Generar visualizaciones
    print("1. Generando gráficos de distribución...")
    grafico_distribucion_numericas(df)
    
    print("2. Generando matriz de correlaciones...")
    grafico_correlaciones(df)
    
    print("3. Generando análisis de variables categóricas...")
    try:
        grafico_categoricas(df)
    except Exception as e:
        print(f"No se pudieron generar gráficos de variables categóricas: {e}")
    
    print("4. Generando análisis de outliers...")
    grafico_boxplot(df)
    
    print("5. Generando análisis de valores faltantes...")
    grafico_valores_faltantes(df)
    
    print("6. Generando resumen estadístico...")
    grafico_resumen_estadistico(df)
    
    print("7. Generando visualizaciones interactivas...")
    crear_visualizaciones_interactivas(df)
    
    print("\n" + "=" * 60)
    print("VISUALIZACIONES COMPLETADAS")
    print("=" * 60)
    print("Los gráficos se han guardado en la carpeta reports/images/")
    print("Las visualizaciones interactivas se han guardado en la carpeta reports/")

if __name__ == "__main__":
    main() 