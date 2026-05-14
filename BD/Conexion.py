import mysql.connector

def conectar():
    conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Redsocial123@",
        database="cgc"
)

    return conexion