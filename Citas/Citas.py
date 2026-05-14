from BD.Conexion import conectar


# =========================
# CREAR CITA
# =========================

def Gestion_citas(
    Fecha,
    Hora,
    Descripcion,
    Estado,
    ID_usuario
):

    con = conectar()

    cursor = con.cursor()

    sql = """
    INSERT INTO citas
    (
        Fecha,
        Hora,
        Descripcion,
        Estado,
        ID
    )
    VALUES (%s, %s, %s, %s, %s)
    """

    valores = (
        Fecha,
        Hora,
        Descripcion,
        Estado,
        ID_usuario
    )

    cursor.execute(sql, valores)

    con.commit()

    cursor.close()

    con.close()


# =========================
# MODIFICAR CITA
# =========================

def Modificar_cita(fecha, hora, descripcion, id_cita):
    conexion = conectar()
    cursor = conexion.cursor()
    sql = """ UPDATE citas
    SET Fecha = %s,Hora = %s,descripcion = %s
    WHERE ID_citas = %s"""
    valores = (fecha,hora, descripcion,id_cita
    )
    cursor.execute(sql, valores)
    conexion.commit()
    cursor.close()
    conexion.close()

# =========================
# OBTENER UNA CITA
# =========================

def obtener_cita(id_cita):

    conexion = conectar()

    cursor = conexion.cursor(dictionary=True)

    sql = """
    SELECT citas.*, registro.Nombre, registro.Apellido
    FROM citas
    INNER JOIN registro
    ON citas.ID = registro.ID
    WHERE citas.ID_citas = %s
    """

    cursor.execute(sql, (id_cita,))

    cita = cursor.fetchone()

    print(cita)

    cursor.close()
    conexion.close()

    return cita


# =========================
# OBTENER TODAS LAS CITAS
# =========================

def obtener_citas(ID_usuario):

    con = conectar()

    cursor = con.cursor(dictionary=True)

    sql = """
    SELECT * FROM citas
    WHERE ID= %s
    """

    cursor.execute(sql, (ID_usuario,))

    citas = cursor.fetchall()

    cursor.close()

    con.close()

    return citas


# =========================
# ELIMINAR CITA
# =========================

def Eliminar_cita(id_cita):

    con = conectar()

    cursor = con.cursor()

    sql = """
    DELETE FROM citas
    WHERE ID_citas = %s
    """

    cursor.execute(sql, (id_cita,))

    con.commit()

    cursor.close()

    con.close()