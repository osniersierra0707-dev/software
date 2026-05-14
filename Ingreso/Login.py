from BD.Conexion import conectar

def login(ID, password):
    con = conectar()
    cursor = con.cursor(dictionary=True)
    sql = """SELECT *FROM registro
    WHERE ID = %s
    AND Contraseña = %s"""

    valores = (ID, password)

    cursor.execute(sql, valores)

    usuario = cursor.fetchone()

    cursor.close()
    con.close()

    return usuario