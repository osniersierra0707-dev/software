from BD.Conexion import conectar

def Registrar(ID, nombre, apellido, correo, contraseña, telefono, direccion, tipo):
    
    conexion = conectar()
    cursor = conexion.cursor()
    
    sql = """INSERT INTO registro 
    (ID, Nombre, Apellido, Email, Contraseña, Tipo, Telefono, Direccion)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
    
    datos = (ID, nombre, apellido, correo, contraseña, tipo, telefono, direccion)
    
    cursor.execute(sql, datos)
    conexion.commit()
    conexion.close()