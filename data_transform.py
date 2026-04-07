import pandas as pd
import numpy as np
import locale

# Ruta del archivo CSV intermedio
archivo_csv = 'DataGeneral_read.csv'

try:
    # Leer el archivo CSV
    df = pd.read_csv(archivo_csv)

    locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')

    df = df[['NROENVIO','FECHADESPACHO','FECHALLEGADAOFICINA','SALIODISTRIBUCION','FECHA RECEPCIÓN',
             'ATRI ENTREGADO','ENTREGAS EFECTIVAS','TIPO DE SERV.','DETALLE UM','ITEM','HOJA DE RUTA','TIPO VEHÍCULO']]


    df['TIPO VEHÍCULO'] = df['TIPO VEHÍCULO'].astype(str)


    # Reemplazar texto
    fecha_original = df['FECHA RECEPCIÓN'].replace('Pendiente', np.nan)

    fecha_original = fecha_original.str.replace(',', '', regex=False)

    # Intento 1: con segundos y hora normal
    df['FECHA RECEPCIÓN'] = pd.to_datetime(
        fecha_original,
        format='%d/%m/%Y %H:%M:%S',
        errors='coerce'
    )

    # Intento 2: sin segundos
    mask = df['FECHA RECEPCIÓN'].isna()
    df.loc[mask, 'FECHA RECEPCIÓN'] = pd.to_datetime(
        fecha_original[mask],
        format='%d/%m/%Y %H:%M',
        errors='coerce'
    )

    # Intento 3: fallback flexible (para casos raros como "3:27:59")
    mask = df['FECHA RECEPCIÓN'].isna()
    df.loc[mask, 'FECHA RECEPCIÓN'] = pd.to_datetime(
        fecha_original[mask],
        errors='coerce',
        dayfirst=True
    )

    df['FECHALLEGADAOFICINA'] = df['FECHALLEGADAOFICINA'].str.replace(r'^\w+,\s*', '', regex=True)
    df['FECHALLEGADAOFICINA'] = pd.to_datetime(
        df['FECHALLEGADAOFICINA'],
        format='%d de %B de %Y',
        errors='coerce'
    )
    df['FECHALLEGADAOFICINA'] = df['FECHALLEGADAOFICINA'].dt.strftime('%Y-%m-%d')


    df['SALIODISTRIBUCION'] = df['SALIODISTRIBUCION'].str.replace(r'^\w+,\s*', '', regex=True)
    df['SALIODISTRIBUCION'] = pd.to_datetime(
        df['SALIODISTRIBUCION'],
        format='%d de %B de %Y',
        errors='coerce'
    )
    df['SALIODISTRIBUCION'] = df['SALIODISTRIBUCION'].dt.strftime('%Y-%m-%d')

    
    # Exportar a Excel
    archivo_excel = 'Data_General_transformada.xlsx'
    df.to_excel(archivo_excel, index=False)
    
    print(f"Datos exportados exitosamente a {archivo_excel}")
except Exception as e:
    print(f"Error al transformar los datos: {e}")
    sys.exit(1)