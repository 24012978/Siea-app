from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta_super_segura'

# Configura aquí tu número de WhatsApp para soporte o compras (ej: 5215512345678)
WHATSAPP_NUMERO = "521TU_NUMERO_AQUI" 

# Inicializar Base de Datos con usuarios, materias y preguntas vinculadas
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    # Tabla de Usuarios
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            correo TEXT NOT NULL,
            telefono TEXT NOT NULL,
            usuario TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    
    # Tabla de Materias (vinculada a cada usuario por user_id)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS materias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            user_id INTEGER NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    ''')
    
    # Tabla de Preguntas/Reactivos (vinculada a la materia)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reactivos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            materia_id INTEGER NOT NULL,
            pregunta TEXT NOT NULL,
            opcion_a TEXT,
            opcion_b TEXT,
            opcion_c TEXT,
            opcion_d TEXT,
            correcta TEXT,
            FOREIGN KEY(materia_id) REFERENCES materias(id)
        )
    ''')
    
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    if 'usuario_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

# Ruta de Registro
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nombre = request.form['nombre']
        correo = request.form['correo']
        telefono = request.form['telefono']
        usuario = request.form['usuario']
        password = generate_password_hash(request.form['password'])

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        try:
            cursor.execute('INSERT INTO users (nombre, correo, telefono, usuario, password) VALUES (?, ?, ?, ?, ?)',
                           (nombre, correo, telefono, usuario, password))
            conn.commit()
            flash('¡Registro exitoso! Ahora puedes iniciar sesión.', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('El nombre de usuario ya está en uso.', 'danger')
        finally:
            conn.close()

    return f'''
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Registro - S.I.E.A.</title>
        <style>
            body {{ background-color: #0b0f0c; color: #00ff66; font-family: Arial, sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }}
            .card {{ border: 2px solid #00ff66; padding: 30px; border-radius: 10px; width: 320px; background: #121814; text-align: center; }}
            input {{ width: 100%; padding: 10px; margin: 8px 0; background: #0b0f0c; border: 1px solid #00ff66; color: #fff; border-radius: 5px; box-sizing: border-box; }}
            button {{ width: 100%; padding: 10px; background: #00ff66; border: none; font-weight: bold; cursor: pointer; border-radius: 5px; color: #000; margin-top: 10px; }}
            button:hover {{ background: #00cc52; }}
            a {{ color: #00ff66; text-decoration: none; display: block; margin-top: 12px; font-size: 14px; }}
            .wa-btn {{ color: #25d366; font-weight: bold; }}
        </style>
    </head>
    <body>
        <div class="card">
            <h2>Registro S.I.E.A.</h2>
            <form method="POST">
                <input type="text" name="nombre" placeholder="Nombre completo" required>
                <input type="email" name="correo" placeholder="Correo electrónico" required>
                <input type="text" name="telefono" placeholder="Teléfono" required>
                <input type="text" name="usuario" placeholder="Nombre de usuario / Matrícula" required>
                <input type="password" name="password" placeholder="Contraseña" required>
                <button type="submit">Registrarse</button>
            </form>
            <a href="/login">¿Ya tienes cuenta? Inicia sesión</a>
            <a class="wa-btn" href="https://wa.me/{WHATSAPP_NUMERO}?text=Hola,%20necesito%20soporte%20o%20adquirir%20accesos%20para%20S.I.E.A." target="_blank">💬 Contactar por WhatsApp</a>
        </div>
    </body>
    </html>
    '''

# Ruta de Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        password = request.form['password']

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE usuario = ?', (usuario,))
        user = cursor.fetchone()
        conn.close()

        if user and check_password_hash(user[5], password):
            session['usuario_id'] = user[0]
            session['usuario'] = user[4]
            session['nombre'] = user[1]
            return redirect(url_for('dashboard'))
        else:
            flash('Usuario o contraseña incorrectos', 'danger')

    return f'''
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Acceso - S.I.E.A.</title>
        <style>
            body {{ background-color: #0b0f0c; color: #00ff66; font-family: Arial, sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }}
            .card {{ border: 2px solid #00ff66; padding: 30px; border-radius: 10px; width: 320px; background: #121814; text-align: center; }}
            input {{ width: 100%; padding: 10px; margin: 10px 0; background: #0b0f0c; border: 1px solid #00ff66; color: #fff; border-radius: 5px; box-sizing: border-box; }}
            button {{ width: 100%; padding: 10px; background: #00ff66; border: none; font-weight: bold; cursor: pointer; border-radius: 5px; color: #000; margin-top: 10px; }}
            button:hover {{ background: #00cc52; }}
            a {{ color: #00ff66; text-decoration: none; display: block; margin-top: 12px; font-size: 14px; }}
            .wa-btn {{ color: #25d366; font-weight: bold; }}
        </style>
    </head>
    <body>
        <div class="card">
            <h2>Acceso S.I.E.A.</h2>
            <form method="POST">
                <input type="text" name="usuario" placeholder="Usuario / Matrícula" required>
                <input type="password" name="password" placeholder="Contraseña" required>
                <button type="submit">Ingresar al Sistema</button>
            </form>
            <a href="/register">¿No tienes cuenta? Regístrate</a>
            <a href="https://wa.me/{WHATSAPP_NUMERO}?text=Hola,%20olvidé%20mi%20contraseña%20de%20S.I.E.A." target="_blank">¿Olvidaste tu contraseña?</a>
            <a class="wa-btn" href="https://wa.me/{WHATSAPP_NUMERO}?text=Hola,%20quiero%20comprar%20acceso%20a%20S.I.E.A." target="_blank">💬 Soporte / Comprar por WhatsApp</a>
        </div>
    </body>
    </html>
    '''

# Panel Principal (Muestra solo las materias creadas por este usuario)
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'usuario_id' not in session:
        return redirect(url_for('login'))
    
    user_id = session['usuario_id']
    nombre_usuario = session.get('nombre')

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Si el usuario crea una materia nueva desde su panel
    if request.method == 'POST':
        nombre_materia = request.form['nombre_materia']
        if nombre_materia.strip():
            cursor.execute('INSERT INTO materias (nombre, user_id) VALUES (?, ?)', (nombre_materia.upper(), user_id))
            conn.commit()
        return redirect(url_for('dashboard'))

    # Consultar SOLAMENTE las materias de este usuario logueado
    cursor.execute('SELECT id, nombre FROM materias WHERE user_id = ?', (user_id,))
    materias = cursor.fetchall()
    conn.close()

    # Generar HTML de las materias dinámicas del usuario
    materias_html = ""
    for mat in materias:
        materias_html += f'''
        <div style="border: 1px solid #00ff66; padding: 15px; margin: 10px 0; border-radius: 5px; background: #121814;">
            <h3>📚 {mat[1]}</h3>
            <a href="/borrar_materia/{mat[0]}" style="color: #ff3333; text-decoration: none; font-weight: bold;">[ Borrar Materia ]</a>
        </div>
        '''

    return f'''
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Panel - S.I.E.A.</title>
        <style>
            body {{ background-color: #0b0f0c; color: #00ff66; font-family: Arial, sans-serif; text-align: center; padding: 30px; }}
            .container {{ max-width: 600px; margin: auto; border: 2px solid #00ff66; padding: 30px; border-radius: 10px; background: #121814; }}
            input {{ width: 80%; padding: 10px; background: #0b0f0c; border: 1px solid #00ff66; color: #fff; border-radius: 5px; }}
            button {{ padding: 10px 20px; background: #00ff66; border: none; font-weight: bold; cursor: pointer; border-radius: 5px; color: #000; margin-top: 10px; }}
            button:hover {{ background: #00cc52; }}
            .logout {{ color: #ff3333; text-decoration: none; font-weight: bold; display: inline-block; margin-top: 20px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Bienvenido al S.I.E.A., {nombre_usuario}</h1>
            <p>Gestiona tus propias materias de estudio:</p>
            
            <form method="POST">
                <input type="text" name="nombre_materia" placeholder="Ej: DERECHOS HUMANOS, ARMAMENTO..." required>
                <br>
                <button type="submit">➕ Registrar y Crear Materia</button>
            </form>

            <hr style="border-color: #00ff66; margin: 20px 0;">
            
            <h2>Tus Materias:</h2>
            {materias_html if materias_html else "<p>No tienes materias registradas. ¡Crea una arriba!</p>"}
            
            <br>
            <a class="logout" href="/logout">Cerrar Sesión</a>
        </div>
    </body>
    </html>
    '''

# Ruta para borrar materia del usuario actual
@app.route('/borrar_materia/<int:id>')
def borrar_materia(id):
    if 'usuario_id' not in session:
        return redirect(url_for('login'))
    
    user_id = session['usuario_id']
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM materias WHERE id = ? AND user_id = ?', (id, user_id))
    conn.commit()
    conn.close()
    return redirect(url_for('dashboard'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)

