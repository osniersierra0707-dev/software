from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import session

from BD.Conexion import conectar
from Ingreso.Login import login
from Ingreso.Registro import Registrar

from Citas.Citas import Gestion_citas
from Citas.Citas import obtener_citas
from Citas.Citas import obtener_cita
from Citas.Citas import Eliminar_cita
from Citas.Citas import Modificar_cita

app = Flask(__name__)

app.secret_key = "CGC_SECRET"


# =========================
# LOGIN
# =========================

@app.route('/')
def inicio():

    return render_template('Login.html')


# =========================
# REGISTRO PAGE
# =========================

@app.route('/registro')
def registro():

    return render_template('formulariosUsu.html')



# =========================
# USUARIO PAGE
# =========================

@app.route('/usuario')
def usuario():

    usuario = session.get('usuario')

    if not usuario:
        return redirect('/')

    return render_template(
        'WebUsu.html',
        usuario=usuario
    )


# =========================
# RECUPERAR PASSWORD PAGE
# =========================

@app.route('/recuperar-password')
def recuperar_password_page():

    return render_template('recuperar_password.html')


# =========================
# HISTORIAL
# =========================

@app.route('/historial')
def historial():

    usuario = session.get('usuario')

    if not usuario:
        return redirect('/')

    ID_usuario = usuario['ID']

    citas = obtener_citas(ID_usuario)

    return render_template(
        'historial.html',
        citas=citas,
        usuario=usuario
    )


# =========================
# MODIFICAR PAGE
# =========================

@app.route('/modificar/<int:id_cita>')
def modificar(id_cita):

    usuario = session.get('usuario')

    if not usuario:
        return redirect('/')

    print("ID RECIBIDO:", id_cita)

    cita = obtener_cita(id_cita)

    print("CITA:", cita)

    return render_template(
        'modificar.html',
        usuario=usuario,
        cita=cita
    )


# =========================
# LOGIN API
# =========================

@app.route('/login', methods=['POST'])
def login_api():

    ID = request.form['ID']
    password = request.form['password']

    usuario = login(ID, password)

    if usuario:

        session['usuario'] = usuario

        return redirect('/usuario')

    else:

        return render_template(
            'Login.html',
            error="Usuario no registrado o credenciales incorrectas"
        )


# =========================
# REGISTRO API
# =========================

@app.route('/registro_api', methods=['POST'])
def registro_api():

    data = request.form

    ID = data.get('ID')
    nombre = data.get('nombre')
    apellido = data.get('apellido')
    email = data.get('email')
    password = data.get('password')
    telefono = data.get('telefono')
    direccion = data.get('direccion')

    conexión = conectar()
    cursor = conexión.cursor()

    # Verificar si el ID ya existe
    cursor.execute("SELECT ID FROM registro WHERE ID = %s", (ID,))

    usuario_existente = cursor.fetchone()

    # si el usuario ya existe

    if usuario_existente:
        cursor.close()
        conexión.close()

        return render_template(
            'formulariosUsu.html',
            error="El ID ya está registrado. Por favor, ingrese otro Numero de identificación.")

    Registrar(
        ID,
        nombre,
        apellido,
        email,
        password,
        telefono,
        direccion,
        "usuario"
    )

    cursor.close()
    conexión.close()
    
    return render_template(
        'Login.html',
        success="Registro exitoso. Por favor, inicie sesión.")


# =========================
# RECUPERAR PASSWORD API
# =========================

@app.route('/recuperar_password_api', methods=['POST'])
def recuperar_password_api():

    ID = request.form['ID']
    nueva_password = request.form['password']

    from BD.Conexion import conectar

    con = conectar()
    cursor = con.cursor()

    sql = """
    UPDATE registro
    SET Contraseña = %s
    WHERE ID = %s
    """

    valores = (nueva_password, ID)

    cursor.execute(sql, valores)
    con.commit()

    if cursor.rowcount > 0:

        cursor.close()
        con.close()

        return render_template(
            'Login.html',
            success='Contraseña actualizada correctamente'
        )

    else:

        cursor.close()
        con.close()

        return render_template(
            'recuperar_password.html',
            error='Usuario no encontrado'
        )


# =========================
# AGENDAR CITA
# =========================

@app.route('/agendar', methods=['POST'])
def agendar():

    usuario = session.get('usuario')

    if not usuario:
        return redirect('/')

    Fecha = request.form['fecha']
    Hora = request.form['hora']
    Descripcion = request.form['servicio']

    Estado = "Pendiente"

    ID_usuario = usuario['ID']

    con = conectar()
    cursor = con.cursor()

    # Verificar si ya existe una cita 

    sql = """select * from citas where Fecha = %s and Hora = %s and ID = %s"""
    valores = (Fecha, Hora, ID_usuario)
    cursor.execute(sql, valores)
    cita_existente = cursor.fetchone()

    # si ya existe una cita en esa fecha y hora 

    if cita_existente:

        cursor.close()
        con.close()

        return render_template(
            'WebUsu.html',
            usuario=usuario,
            error="Este horario ya está reservado. Por favor, elija otro.")
    
    #Guardar la cita

    Gestion_citas(
        Fecha,
        Hora,
        Descripcion,
        Estado,
        ID_usuario
    )

    cursor.close()
    con.close()

    return redirect('/historial')


# =========================
# GUARDAR MODIFICACION
# =========================

@app.route('/guardar_modificacion', methods=['POST'])
def guardar_modificacion():

    id_cita = request.form['id_citas']

    fecha = request.form['fecha']
    hora = request.form['hora']
    descripcion = request.form['descripcion']

    Modificar_cita(
        fecha,
        hora,
        descripcion,
        id_cita
    )

    return redirect('/historial')


# =========================
# ELIMINAR CITA
# =========================

@app.route('/eliminar/<int:id_cita>')
def eliminar_cita(id_cita):

    Eliminar_cita(id_cita)

    return redirect('/historial')


# =========================
# LOGOUT
# =========================

@app.route('/logout')
def logout():

    session.clear()

    return redirect('/')


# =========================
# MAIN
# =========================

if __name__ == '__main__':
    app.run(debug=True)