import hashlib
import html
import json
import os
import random
from datetime import datetime
from urllib.parse import quote

from flask import Flask, redirect, request, session

app = Flask(__name__)
app.secret_key = os.environ.get("SIEA_SECRET_KEY", "siea-change-this-secret")
ROOT = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(ROOT, "preguntas.json")
HISTORY = os.path.join(ROOT, "historial.json")
PENDING_USERS = os.path.join(ROOT, "pending_users.json")
USERS = os.path.join(ROOT, "user.json")
PHONE = "528110290152"
PHONE_DISPLAY = "+52 811 029 0152"


def load(path, default):
    try:
        with open(path, encoding="utf-8") as file:
            return json.load(file)
    except (OSError, ValueError):
        return default


def save(path, data):
    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)


def password_hash(value):
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def esc(value):
    return html.escape(str(value), quote=True)


def wa_link(message="Hola, quiero informacion sobre la suscripcion S.I.E.A."):
    return f"https://wa.me/{PHONE}?text={quote(message)}"


CSS = """<style>
:root{--primary:#2563eb;--primary-dark:#1e40af;--primary-light:#3b82f6;--secondary:#7c3aed;--success:#10b981;--danger:#ef4444;--warning:#f59e0b;--dark:#1f2937;--light:#f9fafb;--gray:#6b7280;--border:#e5e7eb;--paper:#ffffff;--ink:#1f2937}
*{box-sizing:border-box}
body{margin:0;background:var(--light);color:var(--ink);font:15px 'Segoe UI',Tahoma,Geneva,Verdana,sans-serif;line-height:1.6}
a{color:var(--primary);text-decoration:none}
a:hover{text-decoration:underline}
.nav{display:flex;justify-content:space-between;align-items:center;padding:16px max(5vw,20px);background:linear-gradient(135deg,var(--primary) 0%,var(--primary-dark) 100%);color:white;box-shadow:0 2px 8px rgba(0,0,0,0.1)}
.brand{font:900 24px 'Trebuchet MS',sans-serif;letter-spacing:2px;color:white}
.navlinks{display:flex;gap:20px;align-items:center;flex-wrap:wrap}
.navlinks a{color:white;font:600 14px sans-serif;padding:8px 12px;border-radius:4px;transition:all 0.3s}
.navlinks a:hover{background:rgba(255,255,255,0.2)}
.button{display:inline-block;border:0;border-radius:6px;background:var(--primary);color:white;padding:12px 24px;text-decoration:none;font:600 14px sans-serif;cursor:pointer;transition:all 0.3s;box-shadow:0 2px 4px rgba(0,0,0,0.1)}
.button:hover{background:var(--primary-dark);transform:translateY(-2px);box-shadow:0 4px 8px rgba(0,0,0,0.15)}
.button.secondary{background:var(--secondary)}
.button.secondary:hover{background:#6d28d9}
.button.success{background:var(--success)}
.button.success:hover{background:#059669}
.button.danger{background:var(--danger)}
.button.danger:hover{background:#dc2626}
.button.warning{background:var(--warning)}
.button.warning:hover{background:#d97706}
.button.small{padding:8px 16px;font-size:13px}
.button-group{display:flex;gap:10px;flex-wrap:wrap}
.wrap{max-width:1200px;margin:auto;padding:28px 20px}
.hero{display:grid;grid-template-columns:1.1fr .9fr;gap:35px;align-items:center;padding:65px 0 50px}
.hero h1{font:900 clamp(40px,6vw,75px) 'Trebuchet MS',sans-serif;margin:0 0 16px;color:var(--dark)}
.hero p{font:500 18px sans-serif;margin:0 0 24px;color:var(--gray)}
.hero-art{background:linear-gradient(135deg,var(--primary-light),var(--secondary));border-radius:12px;min-height:300px}
.section,.panel{padding:42px 0;border-top:1px solid var(--border)}
.section h2,.panel h2{font:900 28px 'Trebuchet MS',sans-serif;margin:0 0 24px;color:var(--dark)}
.feature-grid,.stats{display:grid;grid-template-columns:repeat(3,1fr);gap:24px}
.feature-item,.stat{background:var(--paper);padding:24px;border-radius:8px;border:1px solid var(--border);transition:all 0.3s}
.feature-item:hover,.stat:hover{border-color:var(--primary);box-shadow:0 4px 12px rgba(37,99,235,0.1)}
.feature-item h3{margin:0 0 12px;color:var(--primary);font:600 18px sans-serif}
.stat b{display:block;font:900 32px sans-serif;color:var(--primary);margin-bottom:8px}
.auth{max-width:450px;margin:35px auto;background:var(--paper);padding:36px;border-radius:12px;border:1px solid var(--border);box-shadow:0 4px 16px rgba(0,0,0,0.08)}
.auth h2{margin:0 0 24px;font:900 24px 'Trebuchet MS',sans-serif;color:var(--dark)}
.legal-box{background:var(--light);padding:24px;border-left:4px solid var(--warning);border-radius:8px;margin:24px 0;font-size:13px;line-height:1.8}
.legal-box h3{margin:0 0 12px;color:var(--dark);font:600 16px sans-serif}
.legal-box ul{margin:12px 0;padding-left:20px}
.legal-box li{margin:8px 0}
label{display:block;margin:16px 0 6px;font:600 13px sans-serif;color:var(--dark)}
input,textarea,select{width:100%;padding:12px;border:1px solid var(--border);border-radius:6px;font:14px sans-serif;margin-bottom:12px;transition:all 0.3s;font-family:'Segoe UI',sans-serif}
input:focus,textarea:focus,select:focus{outline:none;border-color:var(--primary);box-shadow:0 0 0 3px rgba(37,99,235,0.1)}
textarea{resize:vertical;min-height:100px}
.notice{padding:16px;border-radius:6px;margin-bottom:16px;font:600 14px sans-serif}
.notice.error{background:#fee;color:#c33;border:1px solid #f88}
.notice.success{background:#efe;color:#3a3;border:1px solid #8f8}
.notice.info{background:#eef;color:#33a;border:1px solid #88f}
.notice.warning{background:#fef08a;color:#854d0e;border:1px solid #fde047}
.page-title{background:linear-gradient(135deg,#ecfdf5 0%,#f0fdf4 100%);padding:30px max(5vw,20px);border-bottom:1px solid var(--border)}
.page-title h1{font:900 36px 'Trebuchet MS',sans-serif;margin:0;color:var(--dark)}
.page-title p{margin:8px 0 0;color:var(--gray)}
.subject-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:24px;margin-top:24px}
.subject{background:var(--paper);padding:24px;border-radius:8px;border:1px solid var(--border);transition:all 0.3s}
.subject:hover{transform:translateY(-4px);box-shadow:0 8px 16px rgba(0,0,0,0.1);border-color:var(--primary)}
.subject h3{margin:0 0 12px;font:600 18px sans-serif;color:var(--dark)}
.subject p{margin:0 0 16px;color:var(--gray);font-size:14px}
.question{background:var(--paper);padding:20px;border-radius:8px;border-left:4px solid var(--primary);margin-bottom:16px;transition:all 0.3s}
.question:hover{box-shadow:0 4px 12px rgba(0,0,0,0.08)}
.question b{display:block;margin-bottom:8px;font-size:16px;color:var(--dark)}
.question p{margin:0;color:var(--gray);font-size:13px}
.muted{color:var(--gray);font-size:14px}
.answer{display:flex;align-items:center;padding:12px;border-radius:6px;margin:8px 0;cursor:pointer;border:1px solid var(--border);transition:all 0.3s}
.answer:hover{background:#f0f9ff;border-color:var(--primary)}
.answer input{width:auto;margin:0 12px 0 0}
.answer.correct{background:#ecfdf5;border-color:var(--success);color:var(--success)}
.answer.wrong{background:#fef2f2;border-color:var(--danger);color:var(--danger)}
.feedback{background:var(--paper);padding:16px;border-radius:8px;border-left:4px solid var(--primary);margin:12px 0}
.feedback.correct{border-left-color:var(--success);background:#f0fdf4}
.feedback.wrong{border-left-color:var(--danger);background:#fef2f2}
.admin-panel{background:var(--paper);border:1px solid var(--border);border-radius:8px;padding:24px;margin-bottom:24px}
.admin-panel h3{margin-top:0;color:var(--dark)}
.badge-pending{background:#fef08a;color:#854d0e;padding:4px 8px;border-radius:4px;font-size:12px;font-weight:600;margin-left:8px}
.user-table{width:100%;border-collapse:collapse;font:14px sans-serif}
.user-table th{background:var(--light);padding:12px;text-align:left;border-bottom:2px solid var(--border);font:600 13px sans-serif;color:var(--dark)}
.user-table td{padding:12px;border-bottom:1px solid var(--border)}
.user-table tr:hover{background:var(--light)}
.status-badge{display:inline-block;padding:6px 12px;border-radius:20px;font:600 12px sans-serif;text-transform:uppercase}
.status-badge.pending{background:#fef08a;color:#854d0e}
.status-badge.aprobado{background:#dcfce7;color:#166534}
.status-badge.rechazado{background:#fee2e2;color:#991b1b}
.actions{display:flex;gap:8px;flex-wrap:wrap}
.form-group{margin-bottom:16px}
.form-row{display:grid;grid-template-columns:1fr 1fr;gap:16px}
.progress-bar{width:100%;height:8px;background:var(--border);border-radius:4px;overflow:hidden;margin:8px 0}
.progress-fill{height:100%;background:var(--primary);transition:width 0.3s}
.progress-fill.success{background:var(--success)}
.progress-fill.warning{background:var(--warning)}
.progress-fill.danger{background:var(--danger)}
@media(max-width:700px){.hero{grid-template-columns:1fr;padding-top:35px}.hero-art{min-height:220px}.feature-grid,.stats{grid-template-columns:1fr}.nav{align-items:flex-start;flex-direction:column}.navlinks{gap:8px;flex-direction:column;width:100%}.form-row{grid-template-columns:1fr}.user-table{font-size:12px}.user-table th,.user-table td{padding:8px}}
</style>"""


def page(title, body, public=False):
    links = '<a href="/">Inicio</a>'
    if session.get("user"):
        user = load(USERS, {}).get(session.get("user"), {})
        if user.get("role") == "admin" and not public:
            pending = len([u for u in load(PENDING_USERS, {}).values() if u.get("status") == "pendiente"])
            badge = f'<span class="badge-pending">{pending}</span>' if pending else ""
            links += f'<a href="/admin">Admin{badge}</a>'
        if not public:
            links += '<a href="/progreso">Progreso</a><a href="/logout">Salir</a>'
    return f"""<!doctype html><html lang=es><head><meta charset=utf-8><meta name=viewport content='width=device-width,initial-scale=1'><title>{esc(title)} | S.I.E.A.</title>{CSS}</head><body><nav class=nav><div class=brand>S.I.E.A.</div><div class=navlinks>{links}</div></nav>{body}</body></html>"""


def landing(message=""):
    alert = f'<div class="wrap"><div class="notice info">{esc(message)}</div></div>' if message else ""
    body = f"""<main class=wrap>
<section class=hero>
<div>
<p style="color:var(--primary);font:700 13px 'Trebuchet MS',sans-serif;letter-spacing:2px">APRENDE CON DIRECCION</p>
<h1>Sistema Inteligente de Estudio Adaptativo</h1>
<p>Aprende a tu propio ritmo con preguntas y examenes personalizados. Recibe retroalimentacion detallada y mejora tu desempeno academico.</p>
<div class=button-group><a class=button href="/login">Ingresar</a><a class="button secondary" href="/registro">Crear cuenta</a></div>
</div>
<div class=hero-art></div>
</section>

<section class=section>
<h2>Caracteristicas Principales</h2>
<div class=feature-grid>
<div class=feature-item>
<h3>Preguntas Personalizadas</h3>
<p>Crea y organiza preguntas por materia. Estudia de forma estructurada y enfocada.</p>
</div>
<div class=feature-item>
<h3>Examenes Inteligentes</h3>
<p>Realiza examenes aleatorios y obtén calificaciones instantaneas con analisis detallado.</p>
</div>
<div class=feature-item>
<h3>Retroalimentacion Completa</h3>
<p>Analisis por pregunta, recomendaciones de mejora y seguimiento de progreso.</p>
</div>
</div>
</section>

<section class=section>
<h2>Objetivo de la Plataforma</h2>
<div class=legal-box>
<p><strong>S.I.E.A. (Sistema Inteligente de Estudio Adaptativo)</strong> es una plataforma educativa disenada para facilitar el aprendizaje autodirigido y adaptativo. Nuestro objetivo es:</p>
<ul>
<li>Proporcionar herramientas efectivas para el estudio independiente</li>
<li>Permitir a los docentes crear evaluaciones personalizadas</li>
<li>Facilitar la retroalimentacion inmediata para mejorar el aprendizaje</li>
<li>Registrar y analizar el progreso academico</li>
<li>Promover una educacion inclusiva y accesible</li>
</ul>
</div>
</section>

<section class=section>
<h2>Marco Legal y Privacidad</h2>
<div class=legal-box>
<h3>Terminos de Uso y Proteccion de Datos</h3>
<p>Al utilizar esta plataforma, usted acepta que:</p>
<ul>
<li><strong>Responsabilidad del Contenido:</strong> Los usuarios son responsables del contenido que crean. S.I.E.A. no se responsabiliza por contenido ilicito o inapropiado.</li>
<li><strong>Proteccion de Datos Personales:</strong> Sus datos personales (nombre, correo, progreso academico) se almacenan de forma segura y confidencial.</li>
<li><strong>Uso Educativo:</strong> Esta plataforma esta destinada unicamente para fines educativos legales y academicos.</li>
<li><strong>Propiedad Intelectual:</strong> El contenido generado por usuarios permanece como propiedad del usuario, pero S.I.E.A. tiene derecho a usarlo para mejorar la plataforma.</li>
<li><strong>Consentimiento Parental:</strong> Si eres menor de edad, tus padres o tutores deben consentir tu uso de esta plataforma.</li>
<li><strong>Politica de Moderacion:</strong> S.I.E.A. se reserva el derecho de rechazar registros que no cumplan con nuestros estandares eticos y educativos.</li>
</ul>
</div>
</section>

<section class=section>
<h2>Contacto y Soporte</h2>
<div class=legal-box>
<p>Para preguntas, soporte tecnico o mas informacion sobre suscripciones:</p>
<p><strong>WhatsApp:</strong> <a href="{wa_link()}">{PHONE_DISPLAY}</a></p>
<p><strong>Correo:</strong> soporte@siea.edu.mx</p>
</div>
</section>
</main>
{alert}"""
    return page("Estudio inteligente", body, True)


def questions_for_user():
    return [q for q in load(DB, []) if q.get("usuario") == session.get("user")]


@app.route("/")
def home():
    if not session.get("user"):
        return landing()
    questions = questions_for_user()
    subjects = {}
    for question in questions:
        subjects.setdefault(question["materia"], []).append(question)
    cards = "".join(f'<article class=subject><h3>{esc(name)}</h3><p>{len(items)} pregunta(s) guardada(s)</p><a class=button href="/materia/{quote(name)}">Abrir materia</a></article>' for name, items in sorted(subjects.items()))
    options = ''.join(f'<option value="{esc(name)}">{esc(name)}</option>' for name in sorted(subjects))
    exam_form = f'<form method=post action=/exam><label>Examen por materia</label><select name=materia required>{options}</select><button class="button success" type=submit>Iniciar examen</button></form>' if subjects else ""
    body = f"""<div class=page-title><div class=wrap><h1>Hola, {esc(session.get("user"))}</h1><p>Tu escritorio de estudio inteligente</p></div></div><main class=wrap><section class=panel><h2>Agregar nueva materia</h2><form method=post action=/materia><input type=text name=materia placeholder="Ej: Matematicas, Biologia" required><button class="button primary" type=submit>Crear materia</button></form></section><section class=panel>{exam_form}<h2>Mis materias</h2><div class=subject-grid>{cards if cards else '<p class=muted>Aun no tienes materias. Crea una para comenzar!</p>'}</div></section></main>"""
    return page("Panel de estudio", body)


def auth(message=""):
    note = f'<div class="notice error">{esc(message)}</div>' if message else ""
    body = f"""<main class=wrap><div class=auth><h2>Acceso de estudiante</h2>{note}<form method=post><label>Usuario</label><input name=user required><label>Contrasena</label><input type=password name=password required><button class="button primary" type=submit>Ingresar</button></form><p class=muted>No tienes cuenta <a href="/registro">Registrate aqui</a></p></div></main>"""
    return page("Ingresar", body, True)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("user", "").strip().upper()
        user = load(USERS, {}).get(username)
        if not user or user.get("password_hash") != password_hash(request.form.get("password", "")):
            return auth("Usuario o contrasena incorrectos.")
        if user.get("status", "aprobado") == "pendiente":
            return auth("Tu cuenta esta pendiente de aprobacion del administrador.")
        if user.get("status", "aprobado") == "rechazado":
            return auth("Tu cuenta ha sido rechazada.")
        session["user"] = username
        return redirect("/")
    return auth()


@app.route("/registro", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("user", "").strip().upper()
        password = request.form.get("password", "")
        pending = load(PENDING_USERS, {})
        users = load(USERS, {})
        if not username or len(password) < 6:
            return registration("Completa todos los campos. Contrasena minimo 6 caracteres.")
        if username in users or username in pending:
            return registration("Este usuario ya existe.")
        pending[username] = {
            "full_name": request.form.get("name", "").strip(),
            "email": request.form.get("email", "").strip(),
            "password_hash": password_hash(password),
            "status": "pendiente",
            "role": "student",
            "created_at": datetime.now().strftime("%d/%m/%Y %H:%M")
        }
        save(PENDING_USERS, pending)
        return registration("Solicitud enviada. Espera la aprobacion del administrador.")
    return registration()


def registration(message=""):
    msg_type = "success" if "Solicitud" in message else "info" if "Solicitud" in message else "error"
    note = f'<div class="notice {msg_type}">{esc(message)}</div>' if message else ""
    body = f"""<main class=wrap><div class=auth><h2>Crear cuenta</h2>{note}<form method=post><label>Usuario</label><input name=user placeholder="Tu nombre de usuario" required><label>Nombre completo</label><input name=name placeholder="Nombre y apellido" required><label>Correo</label><input type=email name=email placeholder="tu@correo.com" required><label>Contrasena</label><input type=password name=password placeholder="Minimo 6 caracteres" required><button class="button primary" type=submit>Crear cuenta</button></form><p class=muted>Ya tienes cuenta <a href="/login">Inicia sesion aqui</a></p></div></main>"""
    return page("Registro", body, True)


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route("/admin")
def admin_panel():
    user = load(USERS, {}).get(session.get("user"), {})
    if user.get("role") != "admin":
        return redirect("/")
    
    pending = load(PENDING_USERS, {})
    users = load(USERS, {})
    
    pending_users = [{"username": k, **v} for k, v in pending.items() if v.get("status") == "pendiente"]
    all_users = [{"username": k, **v} for k, v in users.items()]
    
    pending_rows = ""
    for u in pending_users:
        pending_rows += f"""<tr>
        <td><strong>{esc(u['username'])}</strong></td>
        <td>{esc(u.get('full_name', ''))}</td>
        <td>{esc(u.get('email', ''))}</td>
        <td>{u.get('created_at', '')}</td>
        <td><div class=actions>
        <form method=post action=/admin/approve style="display:inline"><input type=hidden name=username value="{esc(u['username'])}"><button class="button success small" type=submit>Aprobar</button></form>
        <form method=post action=/admin/reject style="display:inline"><input type=hidden name=username value="{esc(u['username'])}"><button class="button danger small" type=submit>Rechazar</button></form>
        </div></td>
        </tr>"""
    
    all_rows = ""
    for u in all_users:
        all_rows += f"""<tr>
        <td><strong>{esc(u['username'])}</strong></td>
        <td>{esc(u.get('full_name', ''))}</td>
        <td>{esc(u.get('email', ''))}</td>
        <td><span class="status-badge {u.get('status')}">{u.get('status', 'aprobado')}</span></td>
        <td>{u.get('role', 'student')}</td>
        <td>{u.get('created_at', '')}</td>
        </tr>"""
    
    pending_table = f'<table class=user-table><thead><tr><th>Usuario</th><th>Nombre</th><th>Correo</th><th>Fecha</th><th>Acciones</th></tr></thead><tbody>{pending_rows}</tbody></table>' if pending_users else '<p class=muted>No hay usuarios pendientes</p>'
    
    body = f"""<div class=page-title><div class=wrap><h1>Panel de Administrador</h1><p>Gestion de usuarios y aprobaciones</p></div></div><main class=wrap>
    <section class=panel>
        <div class=admin-panel>
            <h3>Usuarios Pendientes ({len(pending_users)})</h3>
            {pending_table}
        </div>
    </section>
    
    <section class=panel>
        <div class=admin-panel>
            <h3>Todos los Usuarios ({len(all_users)})</h3>
            <table class=user-table>
                <thead>
                    <tr>
                        <th>Usuario</th>
                        <th>Nombre</th>
                        <th>Correo</th>
                        <th>Estado</th>
                        <th>Rol</th>
                        <th>Fecha de Registro</th>
                    </tr>
                </thead>
                <tbody>{all_rows}</tbody>
            </table>
        </div>
    </section>
    </main>"""
    
    return page("Panel de Administrador", body)


@app.route("/admin/approve", methods=["POST"])
def admin_approve():
    user = load(USERS, {}).get(session.get("user"), {})
    if user.get("role") != "admin":
        return redirect("/")
    
    username = request.form.get("username", "").upper()
    pending = load(PENDING_USERS, {})
    users = load(USERS, {})
    
    if username in pending:
        user_data = pending.pop(username)
        user_data["status"] = "aprobado"
        users[username] = user_data
        save(PENDING_USERS, pending)
        save(USERS, users)
    
    return redirect("/admin")


@app.route("/admin/reject", methods=["POST"])
def admin_reject():
    user = load(USERS, {}).get(session.get("user"), {})
    if user.get("role") != "admin":
        return redirect("/")
    
    username = request.form.get("username", "").upper()
    pending = load(PENDING_USERS, {})
    
    if username in pending:
        pending.pop(username)
        save(PENDING_USERS, pending)
    
    return redirect("/admin")


@app.route("/materia", methods=["POST"])
def add_subject():
    name = request.form.get("materia", "").strip()
    if name:
        data = load(DB, [])
        if not any(q.get("usuario") == session["user"] and q.get("materia", "").casefold() == name.casefold() for q in data):
            data.append({"usuario": session["user"], "materia": name, "placeholder": True})
            save(DB, data)
    return redirect("/")


@app.route("/materia/<path:name>")
def subject(name):
    questions = [q for q in questions_for_user() if q.get("materia") == name and not q.get("placeholder")]
    rows = "".join(f'<article class=question><b>{esc(q["p"])}</b><p class=muted>A) {esc(q["op"][0])} &nbsp; B) {esc(q["op"][1])} &nbsp; C) {esc(q["op"][2])} &nbsp; D) {esc(q["op"][3])}</p><a class="button small" href="/pregunta/{q["id"]}">Editar</a> <a class="button danger small" href="/pregunta/{q["id"]}/eliminar">Eliminar</a></article>' for q in questions)
    body = f"""<div class=page-title><div class=wrap><h1>{esc(name)}</h1><p>{len(questions)} pregunta(s)</p></div></div><main class=wrap><section class=panel><h2>Agregar pregunta</h2><form method=post action=/pregunta><input type=hidden name=materia value="{esc(name)}"><label>Enunciado</label><textarea name=p required></textarea><label>Opcion A</label><input name=o1 required><label>Opcion B</label><input name=o2 required><label>Opcion C</label><input name=o3 required><label>Opcion D</label><input name=o4 required><label>Respuesta correcta</label><select name=co required><option value="">Selecciona</option><option value=0>A</option><option value=1>B</option><option value=2>C</option><option value=3>D</option></select><button class="button success" type=submit>Agregar</button></form></section><section class=panel><h2>Preguntas</h2>{rows if rows else '<p class=muted>Sin preguntas</p>'}</section></main>"""
    return page(name, body)


@app.route("/pregunta", methods=["POST"])
def add_question():
    data = load(DB, [])
    data = [q for q in data if not (q.get("usuario") == session["user"] and q.get("materia") == request.form["materia"] and q.get("placeholder"))]
    question = {"id": os.urandom(8).hex(), "usuario": session["user"], "materia": request.form["materia"], "p": request.form["p"].strip(), "op": [request.form[f"o{i}"].strip() for i in range(1, 5)], "co": int(request.form["co"])}
    data.append(question)
    save(DB, data)
    return redirect("/materia/" + quote(question["materia"]))


@app.route("/pregunta/<qid>", methods=["GET", "POST"])
def edit_question(qid):
    data = load(DB, [])
    question = next((q for q in data if q.get("id") == qid and q.get("usuario") == session["user"]), None)
    if not question:
        return redirect("/")
    if request.method == "POST":
        question.update(p=request.form["p"].strip(), op=[request.form[f"o{i}"].strip() for i in range(1, 5)], co=int(request.form["co"]))
        save(DB, data)
        return redirect("/materia/" + quote(question["materia"]))
    fields = ''.join(f'<div><label>Opcion {chr(65+i)}</label><input name=o{i+1} value="{esc(question["op"][i])}" required></div>' for i in range(4))
    options = ''.join(f'<option value={i} {"selected" if i == question["co"] else ""}>{chr(65+i)}</option>' for i in range(4))
    body = f'<main class=wrap><section class=panel><h2>Editar</h2><form method=post><label>Enunciado</label><textarea name=p required>{esc(question["p"])}</textarea>{fields}<label>Correcta</label><select name=co required>{options}</select><button class="button success" type=submit>Guardar</button></form></section></main>'
    return page("Editar pregunta", body)


@app.route("/pregunta/<qid>/eliminar")
def delete_question(qid):
    save(DB, [q for q in load(DB, []) if not (q.get("id") == qid and q.get("usuario") == session["user"])])
    return redirect(request.referrer or "/")


@app.route("/exam", methods=["POST"])
def start_exam():
    materia = request.form.get("materia")
    questions = [q for q in questions_for_user() if q.get("materia") == materia and not q.get("placeholder")]
    if not questions:
        return redirect("/")
    session["exam"] = {"materia": materia, "ids": [q["id"] for q in random.sample(questions, len(questions))]}
    return redirect("/exam")


@app.route("/exam", methods=["GET"])
def exam():
    info = session.get("exam", {})
    questions = [q for q in questions_for_user() if q.get("id") in info.get("ids", [])]
    if not questions:
        return redirect("/")
    blocks = []
    for index, question in enumerate(questions, 1):
        choices = ''.join(f'<label class=answer><input type=radio name="answer_{question["id"]}" value={j} required> {chr(65+j)}) {esc(option)}</label>' for j, option in enumerate(question["op"]))
        blocks.append(f'<div class=question><p><b>{index}. {esc(question["p"])}</b></p>{choices}</div>')
    body = f'<main class=wrap><section class=panel><h1>Examen: {esc(info["materia"])}</h1><p class=muted>{len(questions)} pregunta(s)</p><form method=post action=/exam/submit>{"".join(blocks)}<button class="button success" type=submit>Enviar</button><a class=button href="/">Cancelar</a></form></section></main>'
    return page("Examen", body)


@app.route("/exam/submit", methods=["POST"])
def submit_exam():
    info = session.pop("exam", {})
    questions = [q for q in questions_for_user() if q.get("id") in info.get("ids", [])]
    answers = {q["id"]: int(request.form.get(f"answer_{q["id"]}", -1)) for q in questions}
    correct = sum(answers[q["id"]] == q["co"] for q in questions)
    result = {"usuario": session["user"], "fecha": datetime.now().strftime("%Y-%m-%d %H:%M"), "materia": info.get("materia", ""), "correctas": correct, "total": len(questions)}
    history = load(HISTORY, [])
    history.append(result)
    save(HISTORY, history)
    percentage = int((correct / len(questions)) * 100) if questions else 0
    
    feedback_html = ""
    for i, q in enumerate(questions, 1):
        is_correct = answers[q["id"]] == q["co"]
        status = "correct" if is_correct else "wrong"
        icon = "OK" if is_correct else "FALLO"
        feedback_html += f'<div class="feedback {status}"><b>{icon} {i}. {esc(q["p"])}</b><br>Tu respuesta: {chr(65+answers[q["id"]])} | Correcta: {chr(65+q["co"])}</div>'
    
    recommendations = ""
    if percentage == 100:
        recommendations = '<div class="notice success"><b>Excelente</b> Dominaste este tema.</div>'
    elif percentage >= 80:
        recommendations = '<div class="notice success"><b>Muy bien</b> Buen desempeno.</div>'
    elif percentage >= 60:
        recommendations = '<div class="notice warning"><b>Buen progreso</b> Necesitas reforzar.</div>'
    else:
        recommendations = '<div class="notice error"><b>Sigue estudiando</b> Dedica mas tiempo.</div>'
    
    return page("Resultado", f"""<main class=wrap><section class=panel>
    <h1>Resultado: {correct}/{len(questions)} ({percentage}%)</h1>
    <div class=stats>
    <div class=stat><b>{percentage}%</b>Desempeno</div>
    <div class=stat><b>{correct}</b>Correctas</div>
    <div class=stat><b>{len(questions)-correct}</b>Por mejorar</div>
    </div>
    {recommendations}
    <h2>Analisis</h2>
    {feedback_html}
    <a class="button success" href="/">Volver</a> <a class=button href="/progreso">Avances</a>
    </section></main>""")


@app.route("/progreso")
def progress():
    history = [x for x in load(HISTORY, []) if x.get("usuario") == session["user"]]
    total = sum(x.get("total", 0) for x in history)
    correct = sum(x.get("correctas", 0) for x in history)
    percentage = int((correct / total) * 100) if total else 0
    
    rows = ""
    for x in reversed(history):
        pct = int((x["correctas"] / x["total"]) * 100) if x["total"] > 0 else 0
        rows += f'<tr><td>{x["fecha"]}</td><td>{esc(x["materia"])}</td><td>{x["correctas"]}/{x["total"]}</td><td>{pct}%</td></tr>'
    
    if not rows:
        rows = '<tr><td colspan=4>Sin examenes</td></tr>'
    
    body = f"""<main class=wrap>
    <h1>Mi Progreso Academico</h1>
    <div class=stats>
    <div class=stat><b>{len(history)}</b>Examenes</div>
    <div class=stat><b>{percentage}%</b>Promedio<div class=progress-bar><div class="progress-fill" style="width:{percentage}%"></div></div></div>
    <div class=stat><b>{correct}/{total}</b>Correctas</div>
    </div>
    
    <section class=panel>
    <h2>Historial</h2>
    <table class=user-table>
    <thead><tr><th>Fecha</th><th>Materia</th><th>Resultado</th><th>%</th></tr></thead>
    <tbody>{rows}</tbody>
    </table>
    </section>
    </main>"""
    return page("Progreso", body)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
