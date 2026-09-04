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


def wa_link(message="Hola, quiero información sobre la suscripción S.I.E.A."):
    return f"https://wa.me/{PHONE}?text={quote(message)}"


CSS = """<style>
:root{--ink:#12231f;--muted:#60716c;--paper:#f5f1e8;--mint:#d8f0e5;--green:#167b62;--gold:#e3a72f;--red:#b94b45}
*{box-sizing:border-box}body{margin:0;background:var(--paper);color:var(--ink);font:15px Georgia,serif}a{color:inherit}
.nav{display:flex;justify-content:space-between;align-items:center;padding:18px max(5vw,20px);background:#12231f;color:white}.brand{font:900 25px Trebuchet MS,sans-serif;letter-spacing:3px;color:#f3c75b}.navlinks{display:flex;gap:15px;align-items:center;font:13px Trebuchet MS,sans-serif}.navlinks a{text-decoration:none}
.button{display:inline-block;border:0;border-radius:6px;background:var(--green);color:white;padding:12px 17px;text-decoration:none;font:700 13px Trebuchet MS,sans-serif;cursor:pointer}.gold{background:var(--gold);color:#30220c}.danger{background:#f4d7d2;color:#8e352f}
.wrap{max-width:1100px;margin:auto;padding:28px 20px}.hero{display:grid;grid-template-columns:1.1fr .9fr;gap:35px;align-items:center;padding:65px 0 50px}.hero h1{font:900 clamp(40px,6vw,75px) Trebuchet MS,sans-serif;line-height:.96;margin:10px 0 20px}.hero p{color:var(--muted);font-size:18px;line-height:1.5}.hero-art{min-height:330px;border-radius:14px;background:linear-gradient(135deg,rgba(18,35,31,.05),rgba(22,123,98,.28)),url('https://images.unsplash.com/photo-1434030216411-0b793f4b4173?auto=format&fit=crop&w=900&q=80') center/cover;box-shadow:18px 18px 0 #d7e6d8}
.section{padding:42px 0;border-top:1px solid #d8ddd4}.section h2,.panel h2{font:900 28px Trebuchet MS,sans-serif;margin:0 0 18px}.feature-grid,.stats{display:grid;grid-template-columns:repeat(3,1fr);gap:15px}.feature,.panel{padding:22px;background:white;border:1px solid #e0e3da;border-radius:8px}.feature strong{font:700 18px Trebuchet MS,sans-serif;color:var(--green)}.feature p,.muted{line-height:1.45;color:var(--muted)}.legal{background:#e8eee5;padding:22px;line-height:1.5;color:#52635e}
.auth{max-width:430px;margin:35px auto;background:white;padding:28px;border-radius:8px;border-top:5px solid var(--green)}label{display:block;margin:12px 0 5px;font:700 12px Trebuchet MS,sans-serif;color:var(--green)}input,select,textarea{width:100%;padding:12px;border:1px solid #c6d4ca;border-radius:5px;background:#fbfcf8;color:var(--ink);font:15px Georgia,serif}.auth .button{width:100%;margin-top:15px}.notice{padding:12px;background:#fff5d9;border-left:4px solid var(--gold);margin:12px 0}.error{background:#f8dedb;border-left-color:var(--red)}
.page-title{background:var(--mint);padding:30px max(5vw,20px);border-bottom:1px solid #c7dfd3}.page-title h1{font:900 36px Trebuchet MS,sans-serif;margin:0}.subject-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:14px}.subject{padding:18px;border-left:5px solid var(--green);background:#f9fbf7;border-radius:5px}.subject h3{font:700 19px Trebuchet MS,sans-serif;margin:0 0 8px}.form-row{display:grid;grid-template-columns:1fr 1fr;gap:10px}.question{padding:16px;border:1px solid #dce4dc;border-left:4px solid var(--green);margin:12px 0;border-radius:5px}.stat{background:#12231f;color:white;padding:18px;border-radius:7px}.stat b{display:block;font:900 30px Trebuchet MS,sans-serif;color:#f3c75b}.answer{display:block;padding:12px;margin:8px 0;border-radius:5px;background:#f3f5f0}.correct{background:#d9f2df;border:1px solid #74ba88}.wrong{background:#f8d9d5;border:1px solid #cf766d}footer{text-align:center;padding:25px;color:var(--muted);font:12px Trebuchet MS,sans-serif}
@media(max-width:700px){.hero{grid-template-columns:1fr;padding-top:35px}.hero-art{min-height:220px}.feature-grid,.stats{grid-template-columns:1fr}.nav{align-items:flex-start}.navlinks{gap:8px;flex-wrap:wrap;justify-content:flex-end}.form-row{grid-template-columns:1fr}}
</style>"""


def page(title, body, public=False):
    links = '<a href="/">Inicio</a>'
    if session.get("user") and not public:
        links += '<a href="/progreso">Progreso</a><a href="/logout">Salir</a>'
    return f"<!doctype html><html lang=es><head><meta charset=utf-8><meta name=viewport content='width=device-width,initial-scale=1'><title>{esc(title)} | S.I.E.A.</title>{CSS}</head><body><nav class=nav><a class=brand href='/'>S.I.E.A.</a><div class=navlinks>{links}</div></nav>{body}<footer>S.I.E.A. | Estudio, evaluación y progreso académico<br>Uso educativo. Información personal tratada de forma confidencial.</footer></body></html>"


def landing(message=""):
    alert = f'<div class="wrap"><div class="notice">{esc(message)}</div></div>' if message else ""
    body = f'''{alert}<main class=wrap><section class=hero><div><p style="color:var(--green);font:700 13px Trebuchet MS,sans-serif;letter-spacing:2px">APRENDE CON DIRECCIÓN</p><h1>Convierte tus preguntas en progreso.</h1><p>Organiza tu banco de estudio por materia, practica con exámenes y descubre exactamente qué necesitas reforzar.</p><a class=button href=/login>Comenzar a estudiar</a></div><div class=hero-art aria-label="Persona estudiando"></div></section><section class=section><h2>Todo lo que necesitas para avanzar</h2><div class=feature-grid><article class=feature><strong>Materias claras</strong><p>Crea una colección independiente para cada tema y mantén tus reactivos ordenados.</p></article><article class=feature><strong>Exámenes reales</strong><p>Practica por materia para medir tu preparación de forma completa.</p></article><article class=feature><strong>Retroalimentación</strong><p>Al terminar verás respuestas correctas e incorrectas diferenciadas por color.</p></article></div></section><section class=section><h2>Un espacio hecho para estudiar mejor</h2><p class=muted>Registra tus avances, revisa tu historial y vuelve a las preguntas que más trabajo te dieron desde móvil o computadora.</p><div class=legal><b>Marco legal y privacidad</b><br>El acceso es personal e intransferible. S.I.E.A. debe utilizarse con fines educativos y respetando la normativa aplicable de protección de datos. Al registrarte aceptas el tratamiento de la información necesaria para operar tu cuenta y generar tus estadísticas.</div></section></main>'''
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
    cards = "".join(f'<article class=subject><h3>{esc(name)}</h3><p>{len(items)} pregunta(s) guardada(s)</p><a class=button href="/materia/{quote(name)}">Abrir materia</a></article>' for name, items in sorted(subjects.items())) or '<p class=muted>Aún no tienes materias. Crea la primera para comenzar.</p>'
    options = ''.join(f'<option value="{esc(name)}">{esc(name)}</option>' for name in sorted(subjects))
    exam_form = f'<form method=post action=/exam><label>Examen por materia</label><select name=materia required>{options}</select><button class=button type=submit>Iniciar examen</button></form>' if options else '<p class=muted>Agrega preguntas para habilitar los exámenes.</p>'
    body = f'''<div class=page-title><div class=wrap><h1>Hola, {esc(session.get("user"))}</h1><p>Tu escritorio de estudio</p></div></div><main class=wrap><section class=panel><h2>Nueva materia</h2><form method=post action=/materia><div class=form-row><input name=materia placeholder="Ej. Derecho administrativo" required><button class="button gold" type=submit>Crear materia</button></div></form></section><section class=panel><h2>Mis materias</h2><div class=subject-grid>{cards}</div></section><section class=panel><h2>Practicar</h2>{exam_form}<p><a href=/progreso>Ver mi progreso e historial</a></p></section><section class=panel><h2>Suscripción</h2><p class=muted>Solicita información y activa tu acceso directamente por WhatsApp.</p><a class="button gold" target=_blank rel=noopener href="{wa_link()}">Pagar suscripción</a> <span class=muted>{PHONE_DISPLAY}</span></section></main>'''
    return page("Panel de estudio", body)


def auth(message=""):
    note = f'<div class="notice error">{esc(message)}</div>' if message else ""
    body = f'<main class=wrap><div class=auth><h2>Acceso de estudiante</h2>{note}<form method=post><label>Usuario</label><input name=user required><label>Contraseña</label><input type=password name=password required><button class=button type=submit>Ingresar</button></form><p class=muted>¿No tienes cuenta? <a href=/registro>Regístrate aquí</a></p></div></main>'
    return page("Ingresar", body, True)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("user", "").strip().upper()
        user = load(USERS, {}).get(username)
        if not user or user.get("password_hash") != password_hash(request.form.get("password", "")):
            return auth("Usuario o contraseña incorrectos.")
        if user.get("status", "aprobado") != "aprobado":
            return auth("Tu cuenta está pendiente de aprobación.")
        session["user"] = username
        return redirect("/")
    return auth()


@app.route("/registro", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("user", "").strip().upper()
        password = request.form.get("password", "")
        users = load(USERS, {})
        if not username or len(password) < 6 or username in users:
            return registration("Usuario existente o contraseña menor a 6 caracteres.")
        users[username] = {"full_name": request.form.get("name", "").strip(), "email": request.form.get("email", "").strip(), "password_hash": password_hash(password), "status": "aprobado", "role": "user", "created_at": datetime.now().isoformat()}
        save(USERS, users)
        return auth("Cuenta creada. Ya puedes ingresar.")
    return registration()


def registration(message=""):
    note = f'<div class="notice error">{esc(message)}</div>' if message else ""
    body = f'<main class=wrap><div class=auth><h2>Crear cuenta</h2>{note}<form method=post><label>Usuario</label><input name=user required><label>Nombre completo</label><input name=name required><label>Correo</label><input type=email name=email required><label>Contraseña</label><input type=password name=password minlength=6 required><button class=button type=submit>Registrarme</button></form><p><a href=/login>Volver a ingresar</a></p></div></main>'
    return page("Registro", body, True)


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


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
    rows = "".join(f'<article class=question><b>{esc(q["p"])}</b><p class=muted>A) {esc(q["op"][0])} &nbsp; B) {esc(q["op"][1])} &nbsp; C) {esc(q["op"][2])} &nbsp; D) {esc(q["op"][3])}</p><a class=button href="/pregunta/{q["id"]}">Editar</a> <a class="button danger" href="/pregunta/{q["id"]}/eliminar">Eliminar</a></article>' for q in questions) or '<p class=muted>Aún no hay preguntas en esta materia.</p>'
    body = f'''<div class=page-title><div class=wrap><h1>{esc(name)}</h1><p>{len(questions)} pregunta(s)</p></div></div><main class=wrap><section class=panel><h2>Agregar pregunta</h2><form method=post action=/pregunta><input type=hidden name=materia value="{esc(name)}"><label>Enunciado</label><textarea name=p rows=3 required></textarea><div class=form-row><div><label>Opción A</label><input name=o1 required><label>Opción C</label><input name=o3 required></div><div><label>Opción B</label><input name=o2 required><label>Opción D</label><input name=o4 required></div></div><label>Respuesta correcta</label><select name=co><option value=0>A</option><option value=1>B</option><option value=2>C</option><option value=3>D</option></select><br><br><button class=button type=submit>Guardar pregunta</button></form></section><section class=panel><h2>Banco de preguntas</h2>{rows}</section></main>'''
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
    fields = ''.join(f'<div><label>Opción {chr(65+i)}</label><input name=o{i+1} value="{esc(question["op"][i])}" required></div>' for i in range(4))
    options = ''.join(f'<option value={i} {"selected" if i == question["co"] else ""}>{chr(65+i)}</option>' for i in range(4))
    body = f'<main class=wrap><section class=panel><h2>Editar pregunta</h2><form method=post><label>Enunciado</label><textarea name=p rows=3 required>{esc(question["p"])}</textarea><div class=form-row>{fields}</div><label>Respuesta correcta</label><select name=co>{options}</select><br><br><button class=button type=submit>Guardar cambios</button></form></section></main>'
    return page("Editar pregunta", body)


@app.route("/pregunta/<qid>/eliminar")
def delete_question(qid):
    save(DB, [q for q in load(DB, []) if not (q.get("id") == qid and q.get("usuario") == session["user"])])
    return redirect(request.referrer or "/")


@app.route("/exam", methods=["POST"])
def start_exam():
    materia = request.form.get("materia")
    questions = [q for q in questions_for_user() if q.get("materia") == materia and not q.get("placeholder")]
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
    body = f'<main class=wrap><section class=panel><h1>Examen: {esc(info["materia"])}</h1><form method=post action=/exam/submit>{"".join(blocks)}<button class="button gold" type=submit>Terminar y revisar respuestas</button></form></section></main>'
    return page("Examen", body)


@app.route("/exam/submit", methods=["POST"])
def submit_exam():
    info = session.pop("exam", {})
    questions = [q for q in questions_for_user() if q.get("id") in info.get("ids", [])]
    answers = {q["id"]: int(request.form.get(f"answer_{q["id"]}", -1)) for q in questions}
    correct = sum(answers[q["id"]] == q["co"] for q in questions)
    result = {"usuario": session["user"], "fecha": datetime.now().strftime("%Y-%m-%d %H:%M"), "materia": info.get("materia", ""), "correctas": correct, "total": len(questions)}
    history = load(HISTORY, []); history.append(result); save(HISTORY, history)
    rows = ''.join(f'<div class="answer {"correct" if answers[q["id"]] == q["co"] else "wrong"}"><b>{i}. {esc(q["p"])}</b><br>Tu respuesta: {chr(65+answers[q["id"]])} | Respuesta correcta: {chr(65+q["co"])}</div>' for i, q in enumerate(questions, 1))
    return page("Resultado", f'<main class=wrap><section class=panel><h1>Resultado: {correct}/{len(questions)}</h1><p class=muted>Verde = correcta · Rojo = incorrecta</p>{rows}<a class=button href=/>Volver al panel</a></section></main>')


@app.route("/progreso")
def progress():
    history = [x for x in load(HISTORY, []) if x.get("usuario") == session["user"]]
    total = sum(x.get("total", 0) for x in history)
    correct = sum(x.get("correctas", 0) for x in history)
    rows = ''.join(f'<tr><td>{esc(x["fecha"])}</td><td>{esc(x["materia"])}</td><td>{x["correctas"]}/{x["total"]}</td></tr>' for x in reversed(history)) or '<tr><td colspan=3>Aún no hay exámenes realizados.</td></tr>'
    body = f'<main class=wrap><h1>Mi progreso</h1><div class=stats><div class=stat><b>{len(history)}</b>Exámenes</div><div class=stat><b>{correct}</b>Respuestas correctas</div><div class=stat><b>{round(correct/total*100) if total else 0}%</b>Precisión</div></div><section class=panel><h2>Historial</h2><table width=100% cellpadding=10><tr><th>Fecha</th><th>Materia</th><th>Resultado</th></tr>{rows}</table></section></main>'
    return page("Progreso", body)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
