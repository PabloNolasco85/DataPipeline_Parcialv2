import pandas as pd
import pyodbc


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

    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()

    sql = """
              TRUNCATE TABLE [report].[tb_envios];
          """

    cursor.execute(sql)

    conn.commit()
    cursor.close()
    conn.close()

    
    print(f"Tabla limpia")
except Exception as e:
    print(f"Error al limpiar los datos: {e}")