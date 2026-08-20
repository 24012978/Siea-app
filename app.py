import os, json, random
from flask import Flask, request, redirect, session
from datetime import datetime as dt
app = Flask(__name__)
app.secret_key = "siea_app_definitivo_2026"

# Ruta de base de datos
DB_USERS = os.path.expanduser("~/usuarios_siea.json")

def ld_u():
    if os.path.exists(DB_USERS):
        with open(DB_USERS) as f: return json.load(f)
    return {}

def sv_u(d):
    with open(DB_USERS, "w") as f: json.dump(d, f)

# --- DISEÑO BASE Y ESTILOS PROFESIONALES ---
def layout(contenido, titulo="S.I.E.A."):
    return f'''
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@300;600;900&display=swap" rel="stylesheet">
    <style>
        body {{ margin: 0; background: #051C05; color: #E8F5E9; font-family: 'Montserrat', sans-serif; }}
        .header {{ background: #0A2F0A; padding: 20px; border-bottom: 4px solid #4CAF50; text-align: center; }}
        .title {{ font-size: 32px; font-style: italic; font-weight: 900; color: #FFD700; margin: 0; }}
        .card {{ background: #0D2E0D; border: 1px solid #2E7D32; border-radius: 12px; padding: 20px; margin: 20px; }}
        .btn {{ display: block; width: 100%; padding: 15px; background: #FFD700; color: #000; text-align: center; border-radius: 8px; font-weight: 900; text-decoration: none; margin-top: 10px; border: none; cursor: pointer; }}
        input {{ width: 100%; padding: 12px; margin: 10px 0; border-radius: 6px; border: 1px solid #4CAF50; background: #051C05; color: #fff; box-sizing: border-box; }}
        label {{ display: block; margin: 10px 0; color: #C8E6C9; }}
    </style>
    <div class="header"><h1 class="title">{titulo}</h1></div>
    {contenido}
    '''

@app.route("/", methods=["GET", "POST"])
def login():
    if "user" in session: return redirect("/panel")
    if request.method == "POST":
        u = request.form.get("u", "").strip().upper()
        p = request.form.get("p", "").strip()
        users = ld_u()
        if u in users and users[u]['p'] == p:
            session["user"] = u
            return redirect("/panel")
        return "Acceso denegado. <a href='/'>Reintentar</a>"

    form = f'''
    <div class="card">
        <p style="font-size: 14px; text-align: justify;"><b>Propósito Institucional:</b> Sistema avanzado para la evaluación y gestión de reactivos académicos. <br><br>
        <b>Aviso de Privacidad:</b> El acceso es restringido. Cada cuenta está vinculada a un usuario único bajo suscripción activa.</p>
        <form method="post">
            <input name="u" placeholder="Matrícula / Usuario" required>
            <input name="p" type="password" placeholder="Contraseña" required>
            <button class="btn">INGRESAR AL SISTEMA</button>
        </form>
        <a href="https://wa.me/528110290152" class="btn" style="background:#2E7D32; color:#fff;">💳 PAGAR SUSCRIPCIÓN</a>
    </div>
    '''
    return layout(form, "S.I.E.A.")

@app.route("/panel")
def panel():
    if "user" not in session: return redirect("/")
    h = f'''
    <div class="card">
        <h2 style="color:#FFD700">🚀 EXÁMENES</h2>
        <a href="/exam_g" class="btn" style="background:#1E88E5; color:#fff;">EXAMEN GENERAL</a>
        <a href="/exam_p" class="btn" style="background:#8E24AA; color:#fff;">EXAMEN PERSONALIZADO</a>
    </div>
    <div class="card">
        <h2 style="color:#4CAF50">📚 BANCO DE PREGUNTAS</h2>
        <a href="/banco" style="color:#81C784;">Gestionar materias y editar reactivos</a>
    </div>
    '''
    return layout(h, "Panel de Control")

# --- LÓGICA DE EXAMENES Y BANCO (RESERVADOS PARA TU LÓGICA ANTERIOR) ---
@app.route("/exam_g")
def ex_g(): return layout("<h2>Examen General</h2><p>Lógica de todas las materias...</p>", "Examen General")

@app.route("/exam_p")
def ex_p(): return layout("<h2>Examen Personalizado</h2><p>Selección por casillas...</p>", "Examen Personalizado")

@app.route("/banco")
def banco(): return layout("<h2>Gestión de Materias</h2><p>Edición de materias y reactivos aquí.</p>", "Banco de Preguntas")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)
