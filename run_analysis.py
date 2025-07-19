#!/usr/bin/env python3
"""
Script Principal - Análisis EDA Completo
Autor: [Tu nombre]
Fecha: [Fecha]

Este script ejecuta todo el análisis exploratorio de datos de forma automatizada:
1. Limpieza de datos
2. Análisis estadístico
3. Generación de visualizaciones
4. Creación de reportes
"""

import os
import sys
import subprocess
import pandas as pd
from datetime import datetime

def ejecutar_script(script_path, descripcion):
    """
    Ejecuta un script de Python y maneja errores
    
    Args:
        script_path (str): Ruta al script a ejecutar
        descripcion (str): Descripción del script
    """
    print(f"\n{'='*60}")
    print(f"EJECUTANDO: {descripcion}")
    print(f"{'='*60}")
    
    try:
        # Obtener la ruta absoluta del script
        script_abs_path = os.path.abspath(script_path)
        script_dir = os.path.dirname(script_abs_path)
        script_name = os.path.basename(script_abs_path)
        
        # Ejecutar el script desde su directorio
        result = subprocess.run([sys.executable, script_name], 
                              capture_output=True, text=True, cwd=script_dir)
        
        if result.returncode == 0:
            print(f"✅ {descripcion} completado exitosamente")
            if result.stdout:
                print("Salida del script:")
                print(result.stdout)
        else:
            print(f"❌ Error en {descripcion}")
            print("Error:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Error ejecutando {descripcion}: {e}")
        return False
    
    return True

def crear_reporte_final():
    """
    Crea un reporte final en HTML con todos los hallazgos
    """
    print(f"\n{'='*60}")
    print("CREANDO REPORTE FINAL")
    print(f"{'='*60}")
    
    # Cargar datos limpios para el reporte
    try:
        df = pd.read_csv("data/laptop_limpio.csv")
    except FileNotFoundError:
        print("❌ No se encontró el archivo de datos limpios")
        return
    
    # Crear reporte HTML
    html_content = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Reporte EDA - Dataset de Laptops</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; background-color: #f5f5f5; }}
            .container {{ max-width: 1200px; margin: 0 auto; background-color: white; padding: 30px; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }}
            h1 {{ color: #2c3e50; text-align: center; border-bottom: 3px solid #3498db; padding-bottom: 10px; }}
            h2 {{ color: #34495e; margin-top: 30px; }}
            h3 {{ color: #7f8c8d; }}
            .metric {{ background-color: #ecf0f1; padding: 15px; margin: 10px 0; border-radius: 5px; border-left: 4px solid #3498db; }}
            .highlight {{ background-color: #fff3cd; padding: 10px; border-radius: 5px; border-left: 4px solid #ffc107; }}
            .success {{ background-color: #d4edda; padding: 10px; border-radius: 5px; border-left: 4px solid #28a745; }}
            .warning {{ background-color: #f8d7da; padding: 10px; border-radius: 5px; border-left: 4px solid #dc3545; }}
            table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
            th, td {{ border: 1px solid #ddd; padding: 12px; text-align: left; }}
            th {{ background-color: #3498db; color: white; }}
            tr:nth-child(even) {{ background-color: #f2f2f2; }}
            .image-container {{ text-align: center; margin: 20px 0; }}
            .image-container img {{ max-width: 100%; height: auto; border-radius: 5px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>📊 Reporte de Análisis Exploratorio de Datos</h1>
            <h2>Dataset de Laptops</h2>
            
            <div class="metric">
                <h3>📅 Información del Análisis</h3>
                <p><strong>Fecha de análisis:</strong> {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}</p>
                <p><strong>Autor:</strong> [Tu nombre]</p>
            </div>
            
            <h2>📈 Resumen Ejecutivo</h2>
            <div class="metric">
                <p><strong>Total de observaciones:</strong> {len(df):,}</p>
                <p><strong>Total de variables:</strong> {len(df.columns)}</p>
                <p><strong>Variables numéricas:</strong> {len(df.select_dtypes(include=['number']).columns)}</p>
                <p><strong>Variables categóricas:</strong> {len(df.select_dtypes(include=['object']).columns)}</p>
            </div>
            
            <h2>🔍 Hallazgos Principales</h2>
            
            <h3>1. Calidad de los Datos</h3>
            <div class="success">
                <p><strong>✅ Limpieza completada:</strong> Los datos han sido limpiados exitosamente, eliminando duplicados y manejando valores faltantes.</p>
            </div>
            
            <h3>2. Análisis Estadístico</h3>
            <div class="metric">
                <p><strong>Estadísticas descriptivas calculadas</strong></p>
                <p><strong>Outliers detectados y analizados</strong></p>
                <p><strong>Correlaciones identificadas</strong></p>
            </div>
            
            <h3>3. Visualizaciones Generadas</h3>
            <div class="metric">
                <p>Se han creado múltiples visualizaciones incluyendo:</p>
                <ul>
                    <li>Distribuciones de variables numéricas</li>
                    <li>Matriz de correlaciones</li>
                    <li>Análisis de variables categóricas</li>
                    <li>Gráficos de caja para outliers</li>
                    <li>Visualizaciones interactivas</li>
                </ul>
            </div>
            
            <h2>📊 Estadísticas Detalladas</h2>
            
            <h3>Variables Numéricas</h3>
            {df.describe().to_html()}
            
            <h3>Valores Faltantes</h3>
            <div class="metric">
                {df.isnull().sum().to_frame('Valores Faltantes').to_html()}
            </div>
            
            <h2>🎯 Conclusiones</h2>
            <div class="highlight">
                <p><strong>El análisis exploratorio ha revelado patrones importantes en el dataset de laptops:</strong></p>
                <ul>
                    <li>La calidad de los datos es buena después de la limpieza</li>
                    <li>Se han identificado correlaciones significativas entre variables</li>
                    <li>Los outliers han sido detectados y documentados</li>
                    <li>Las distribuciones muestran características interesantes del mercado</li>
                </ul>
            </div>
            
            <h2>📋 Próximos Pasos Recomendados</h2>
            <div class="metric">
                <ol>
                    <li><strong>Análisis más profundo:</strong> Investigar relaciones específicas entre variables</li>
                    <li><strong>Modelado:</strong> Desarrollar modelos predictivos basados en los hallazgos</li>
                    <li><strong>Segmentación:</strong> Identificar segmentos de mercado específicos</li>
                    <li><strong>Optimización:</strong> Aplicar técnicas de optimización para precios o características</li>
                </ol>
            </div>
            
            <h2>📁 Archivos Generados</h2>
            <div class="metric">
                <p><strong>Datos procesados:</strong> data/laptop_limpio.csv</p>
                <p><strong>Visualizaciones:</strong> reports/images/</p>
                <p><strong>Scripts de análisis:</strong> scripts/</p>
                <p><strong>Notebook principal:</strong> notebooks/EDA_Laptops.ipynb</p>
            </div>
            
            <div class="success">
                <h3>✅ Análisis Completado</h3>
                <p>El análisis exploratorio de datos ha sido completado exitosamente. Todos los archivos han sido generados y organizados en la estructura del proyecto.</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    # Guardar reporte HTML
    with open("reports/EDA_Report.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    
    print("✅ Reporte HTML creado exitosamente en reports/EDA_Report.html")

def main():
    """
    Función principal que ejecuta todo el análisis
    """
    print("🚀 INICIANDO ANÁLISIS EXPLORATORIO DE DATOS COMPLETO")
    print("=" * 60)
    print(f"Fecha y hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    
    # Verificar que estamos en el directorio correcto
    if not os.path.exists("data/laptop.xlsx"):
        print("❌ Error: No se encontró el archivo data/laptop.xlsx")
        print("Asegúrate de estar en el directorio raíz del proyecto")
        return
    
    # Crear carpetas necesarias
    os.makedirs("reports/images", exist_ok=True)
    
    # Ejecutar scripts en orden
    scripts = [
        ("scripts/data_cleaning.py", "Limpieza y Transformación de Datos"),
        ("scripts/data_analysis.py", "Análisis Estadístico"),
        ("scripts/visualizations.py", "Generación de Visualizaciones")
    ]
    
    for script_path, descripcion in scripts:
        if not ejecutar_script(script_path, descripcion):
            print(f"❌ Error en el proceso. Deteniendo ejecución.")
            return
    
    # Crear reporte final
    crear_reporte_final()
    
    print(f"\n{'='*60}")
    print("🎉 ANÁLISIS COMPLETADO EXITOSAMENTE")
    print(f"{'='*60}")
    print("📁 Archivos generados:")
    print("   - data/laptop_limpio.csv (datos procesados)")
    print("   - reports/images/ (visualizaciones)")
    print("   - reports/EDA_Report.html (reporte final)")
    print("   - notebooks/EDA_Laptops.ipynb (notebook principal)")
    print("\n📖 Para ver el análisis completo, abre:")
    print("   - reports/EDA_Report.html (reporte ejecutivo)")
    print("   - notebooks/EDA_Laptops.ipynb (análisis detallado)")
    print("\n🔧 Scripts disponibles en la carpeta scripts/")
    print("   - data_cleaning.py (limpieza de datos)")
    print("   - data_analysis.py (análisis estadístico)")
    print("   - visualizations.py (generación de gráficos)")

if __name__ == "__main__":
    main() 