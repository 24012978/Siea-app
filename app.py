import os, json, random
from flask import Flask, request, redirect, session
app = Flask(__name__)
app.secret_key = "siea_prod_2026_control_total"

DB_USERS = os.path.expanduser("~/usuarios_siea.json")

# Funciones de base de datos...
def ld_u():
    if os.path.exists(DB_USERS):
        with open(DB_USERS) as f: return json.load(f)
    return {}

def sv_u(d):
    with open(DB_USERS, "w") as f: json.dump(d, f)

# --- LOGIN INSTITUCIONAL ---
@app.route("/", methods=["GET", "POST"])
def login():
    if "user" in session: return panel()
    if request.method == "POST":
        u = request.form.get("u", "").strip().upper()
        p = request.form.get("p", "").strip()
        users = ld_u()
        if u in users and users[u]['p'] == p:
            session["user"] = u
            return redirect("/panel")
        return "Acceso denegado."

    h = '<style>body{background:#051C05;color:#fff;font-family:sans-serif;text-align:center;padding:20px}'
    h += '.t{font-size:40px;font-style:italic;color:#FFD700} .card{background:#0A2F0A;padding:20px;border-radius:15px;border:1px solid #4CAF50}'
    h += '</style><div class=card><h1 class=t>S.I.E.A.</h1>'
    h += '<p style=font-size:12px>Propósito: Sistema integral de evaluación de reactivos.<br>Aviso de Privacidad: Datos protegidos y exclusivos por usuario.</p>'
    h += '<form method=post><input name=u placeholder="Usuario" required><br><input name=p type=password placeholder="Contraseña" required><br><button>INGRESAR</button></form>'
    h += '<br><a href="https://wa.me/528110290152" style=color:#fff>💳 Pagar suscripción y solicitar acceso</a></div>'
    return h

# --- PANEL PRINCIPAL ---
@app.route("/panel")
def panel():
    if "user" not in session: return redirect("/")
    h = '<style>h1{color:#FFD700} h2{color:#4CAF50} .card{background:#0F380F;padding:10px;margin:10px;border-radius:5px}</style>'
    h += '<h1>Panel de Control</h1>'
    h += '<h2>🚀 Exámenes</h2><div class=card><a href=/exam_g>EXAMEN GENERAL</a></div>'
    h += '<div class=card><a href=/exam_p>EXAMEN PERSONALIZADO</a></div>'
    h += '<h2>📚 Banco de Preguntas</h2><a href=/banco>Gestionar materias y reactivos</a>'
    return h

# --- LÓGICA DE EXAMENES ---
@app.route("/exam_g")
def ex_g():
    # Lógica de examen general
    return "Examen General (Todas las materias)"

@app.route("/exam_p", methods=["GET", "POST"])
def ex_p():
    if request.method == "GET":
        # Formulario con checkboxes para elegir materias
        return "Selecciona materias con casillas"
    return "Iniciando examen personalizado..."

@app.route("/banco")
def banco():
    # Aquí editas materias y preguntas
    return "Gestión de Banco de Preguntas"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)
