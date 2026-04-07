import pandas as pd
import openpyxl


# Ruta del archivo
archivo_base = 'DataGeneral.xlsx'
archivo_csv = 'DataGeneral_read.csv'
try:

    # Leer el archivo BASE
    df = pd.read_excel(archivo_base, sheet_name="BD_GENERAL" , engine='openpyxl')

    # Guardar los datos en un archivo CSV temporal
    df.to_csv(archivo_csv, index=False , encoding='utf-8-sig')
    print(f"Datos leídos y guardados en {archivo_csv}")

except Exception as e:
    print(f"Error al leer el archivo: {e}")
