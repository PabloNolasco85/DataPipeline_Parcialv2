import pandas as pd
import pyodbc
import json

# Ruta del archivo transformado
archivo_transf = 'Data_General_transformada.xlsx'

try:

    server = 'certus.c3qusqc4qdsy.us-east-2.rds.amazonaws.com'
    database = 'certus'
    username = 'admin'
    password = 'nolose.123'
    port = 1433

    connection_string = (
        f'DRIVER={{ODBC Driver 17 for SQL Server}};'
        f'SERVER={server},{port};'
        f'DATABASE={database};'
        f'UID={username};'
        f'PWD={password}'
    )

    df = pd.read_excel(archivo_transf, engine='openpyxl')
    df = df.astype(object).where(pd.notnull(df), None)

    data = list(
        df[['NROENVIO', 'FECHADESPACHO', 'FECHALLEGADAOFICINA', 'SALIODISTRIBUCION', 'FECHA RECEPCIÓN',
            'ATRI ENTREGADO', 'ENTREGAS EFECTIVAS', 'TIPO DE SERV.', 'DETALLE UM', 'ITEM', 'HOJA DE RUTA',
            'TIPO VEHÍCULO']].itertuples(index=False, name=None))

    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()


    cursor.executemany("""
            insert into report.tb_envios (NROENVIO,FEC_DESPACHO,FEC_LLEGADAOFICINA,FEC_SALIODISTRIBUCION,FEC_RECEPCION,
            ENTREGADO,ENTREG_EFECTIVA,TIPO_DE_SERV,DETALLE,ITEM,HOJA_RUTA,TIPO_VEHICULO)
            VALUES (?, ?, ?, ?, ?,
            ?, ?, ?,?,?,?,?)
            """, data)

    conn.commit()
    cursor.close()
    conn.close()

    with open("resultado.json", "w") as f:
        json.dump({"filas": len(df)}, f)
    
    print(f"Datos exportados exitosamente a {archivo_transf}")
except Exception as e:
    print(f"Error al exportar los datos: {e}")