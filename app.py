import os,json,random,hashlib,uuid,sqlite3
from flask import Flask,request,redirect,session,render_template_string
from datetime import datetime as dt
from functools import wraps

app=Flask(__name__)
app.secret_key="siea_final_profesional_completo_2026"

# ============== RUTAS DE ARCHIVOS ==============
DB=os.path.expanduser("~/preg.json")
HU=os.path.expanduser("~/hist.json")
UU=os.path.expanduser("~/user.json")
MM=os.path.expanduser("~/materias.json")
ADMIN_DB=os.path.expanduser("~/admin.json")
USUARIOS_PENDIENTES=os.path.expanduser("~/usuarios_pendientes.json")
PAGOS_DB=os.path.expanduser("~/pagos.json")

# ============== FUNCIONES HASH Y SEGURIDAD ==============
def hash_password(p):
    return hashlib.sha256(p.encode()).hexdigest()

def require_login(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user" not in session:
            return redirect("/")
        return f(*args, **kwargs)
    return decorated_function

def require_admin(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("role") != "admin":
            return '<div style="text-align:center;padding:50px;color:red"><h1>❌ ACCESO DENEGADO</h1><p>Se requieren permisos de administrador</p><a href="/">← Volver</a></div>'
        return f(*args, **kwargs)
    return decorated_function

# ============== FUNCIONES DE BASE DE DATOS ==============
def ensure_admin():
    try:
        if not os.path.exists(ADMIN_DB):
            adm={"ADMIN":{"password_hash":hash_password("Admin123"),"status":"aprobado","role":"admin","email":"admin@siea.com","created_at":dt.now().strftime("%d/%m/%Y %H:%M")}}
            with open(ADMIN_DB,"w") as f: json.dump(adm,f,indent=2)
        if not os.path.exists(UU):
            u={"ADMIN":{"password_hash":hash_password("Admin123"),"status":"aprobado","role":"admin","email":"admin@siea.com","full_name":"Administrador Sistema","created_at":dt.now().strftime("%d/%m/%Y %H:%M")}}
            with open(UU,"w") as f: json.dump(u,f,indent=2)
        if not os.path.exists(USUARIOS_PENDIENTES):
            with open(USUARIOS_PENDIENTES,"w") as f: json.dump({},f)
        if not os.path.exists(PAGOS_DB):
            with open(PAGOS_DB,"w") as f: json.dump({},f)
    except: pass
ensure_admin()

def ld():
    try:
        if os.path.exists(DB):
            with open(DB) as f: return json.load(f)
    except: pass
    return []

def sv(d):
    with open(DB,"w") as f: json.dump(d,f,indent=2)

def ld_h():
    try:
        if os.path.exists(HU):
            with open(HU) as f: return json.load(f)
    except: pass
    return []

def sv_h(d):
    with open(HU,"w") as f: json.dump(d,f,indent=2)

def ld_u():
    try:
        if os.path.exists(UU):
            with open(UU) as f: return json.load(f)
    except: pass
    return {}

def sv_u(d):
    with open(UU,"w") as f: json.dump(d,f,indent=2)

def ld_m():
    try:
        if os.path.exists(MM):
            with open(MM) as f: return json.load(f)
    except: pass
    return {}

def sv_m(d):
    with open(MM,"w") as f: json.dump(d,f,indent=2)

def ld_admin():
    try:
        if os.path.exists(ADMIN_DB):
            with open(ADMIN_DB) as f: return json.load(f)
    except: pass
    return {}

def sv_admin(d):
    with open(ADMIN_DB,"w") as f: json.dump(d,f,indent=2)

def ld_pendientes():
    try:
        if os.path.exists(USUARIOS_PENDIENTES):
            with open(USUARIOS_PENDIENTES) as f: return json.load(f)
    except: pass
    return {}

def sv_pendientes(d):
    with open(USUARIOS_PENDIENTES,"w") as f: json.dump(d,f,indent=2)

def ld_pagos():
    try:
        if os.path.exists(PAGOS_DB):
            with open(PAGOS_DB) as f: return json.load(f)
    except: pass
    return {}

def sv_pagos(d):
    with open(PAGOS_DB,"w") as f: json.dump(d,f,indent=2)

# ============== PÁGINA DE LOGIN MEJORADA ==============
def login_page(mensaje=""):
    h=""
    h+='<meta name=viewport content="width=device-width,initial-scale=1">'
    h+='<meta charset="UTF-8">'
    h+='<link href="https://fonts.googleapis.com/css2?family=Montserrat:ital,wght@0,400;0,700;0,900;1,400;1,700&display=swap" rel="stylesheet">'
    h+='<style>'
    h+='*{margin:0;padding:0;box-sizing:border-box}'
    h+='body{background:#050B05;color:#E0EFE0;font-family:Montserrat,system-ui;min-height:100vh;display:flex;flex-direction:column}'
    
    # Hero Section Mejorada
    h+='.hero{background:radial-gradient(ellipse at 20% 20%, rgba(0,255,128,0.15), transparent 55%), linear-gradient(180deg,#0D1A0D 0%,#050905 100%);border-bottom:3px solid #00FF80;padding:40px 20px;text-align:center;box-shadow:0 10px 40px rgba(0,255,128,0.1)}'
    h+='.logo-container{display:flex;flex-direction:column;align-items:center;gap:15px}'
    h+='.sigla{font-size:48px;font-weight:900;font-style:italic;letter-spacing:8px;color:#FFD700;text-shadow:0 5px 20px rgba(255,215,0,0.5);animation:glow 2s ease-in-out infinite}'
    h+='@keyframes glow{0%,100%{text-shadow:0 5px 20px rgba(255,215,0,0.5)}50%{text-shadow:0 5px 30px rgba(255,215,0,0.8)}}'
    h+='.sub{font-size:12px;letter-spacing:4px;color:#8AB38A;font-weight:700;margin-top:5px}'
    h+='.tagline{font-size:13px;color:#00FF80;margin-top:15px;font-style:italic;font-weight:600}'
    h+='.purpose{background:rgba(0,0,0,0.7);border-left:5px solid #FFD700;border-radius:8px;padding:15px 20px;margin-top:20px;max-width:600px;margin-left:auto;margin-right:auto}'
    h+='.purpose b{color:#FFD700;font-size:11px;letter-spacing:2px;display:block;margin-bottom:8px;text-transform:uppercase}'
    h+='.purpose p{font-size:12px;line-height:1.8;color:#D2DCD2;text-align:justify}'
    
    # Contenedor principal
    h+='.container{display:flex;flex:1;gap:30px;padding:40px 20px;flex-wrap:wrap;justify-content:center;align-items:flex-start;max-width:1200px;margin:0 auto;width:100%}'
    
    # Tarjetas
    h+='.card{width:100%;max-width:400px;background:linear-gradient(135deg,rgba(13,26,13,0.95),rgba(10,15,10,0.95));border:1.5px solid rgba(0,255,128,0.4);border-radius:16px;padding:25px;box-shadow:0 20px 50px rgba(0,0,0,0.8);backdrop-filter:blur(10px)}'
    h+='.card-admin{border-color:rgba(255,215,0,0.4)}'
    h+='.card-support{border-color:rgba(255,215,0,0.4)}'
    h+='.card-header{text-align:center;margin-bottom:20px;padding-bottom:15px;border-bottom:2px solid rgba(255,255,255,0.1)}'
    h+='.card-title{font-weight:900;letter-spacing:2px;font-size:13px;text-transform:uppercase}'
    h+='.card-title-login{color:#00FF80}'
    h+='.card-title-admin{color:#FFD700}'
    h+='.card-title-support{color:#FFD700}'
    h+='.subtitle{font-size:10px;color:#7EA97E;margin-top:5px;letter-spacing:1px}'
    
    # Tabs
    h+='.tab-buttons{display:flex;gap:10px;margin-bottom:15px}'
    h+='.tab-btn{flex:1;padding:11px;border:2px solid #00FF80;background:transparent;color:#00FF80;border-radius:8px;cursor:pointer;font-weight:700;font-size:11px;transition:all 0.3s}'
    h+='.tab-btn:hover{background:rgba(0,255,128,0.2)}'
    h+='.tab-btn.active{background:#00FF80;color:#050905;box-shadow:0 0 15px rgba(0,255,128,0.4)}'
    h+='.tab-content{display:none}'
    h+='.tab-content.active{display:block}'
    
    # Formularios
    h+='.lbl{font-size:10px;letter-spacing:1.8px;color:#00FF80;font-weight:700;margin:14px 0 5px 0;text-transform:uppercase}'
    h+='.inp{width:100%;padding:13px;background:rgba(5,11,5,0.8);border:1.5px solid #1A401A;border-radius:10px;color:#fff;font-size:13px;transition:all 0.3s;font-family:Montserrat}'
    h+='.inp:focus{outline:none;border-color:#00FF80;box-shadow:0 0 10px rgba(0,255,128,0.3)}'
    h+='.btn{width:100%;padding:14px;border:0;border-radius:10px;font-weight:900;letter-spacing:2px;margin-top:16px;background:linear-gradient(180deg,#00FF80,#00B359);color:#050905;cursor:pointer;font-size:12px;transition:all 0.3s;text-transform:uppercase}'
    h+='.btn:hover{transform:translateY(-2px);box-shadow:0 10px 25px rgba(0,255,128,0.3)}'
    h+='.btn-register{background:linear-gradient(180deg,#FF9800,#E65100)}'
    h+='.btn-register:hover{box-shadow:0 10px 25px rgba(255,152,0,0.4)}'
    h+='.btn-admin{background:linear-gradient(180deg,#FFD700,#CCAC00);color:#050905}'
    h+='.btn-admin:hover{box-shadow:0 10px 25px rgba(255,215,0,0.4)}'
    
    # Mensajes
    h+='.error-msg{background:rgba(38,10,10,0.9);border:1px solid #5A1A1A;color:#FF8A80;padding:12px;border-radius:8px;margin-bottom:12px;font-size:11px;border-left:4px solid #FF6B6B}'
    h+='.success-msg{background:rgba(10,38,26,0.9);border:1px solid #1A5A2A;color:#00FF80;padding:12px;border-radius:8px;margin-bottom:12px;font-size:11px;border-left:4px solid #00FF80}'
    h+='.warning-msg{background:rgba(51,38,10,0.9);border:1px solid #5A4A1A;color:#FFD700;padding:12px;border-radius:8px;margin-bottom:12px;font-size:11px;border-left:4px solid #FFD700}'
    
    # Info
    h+='.support-info{margin:15px 0;padding:14px;background:rgba(0,255,128,0.08);border-left:4px solid #00FF80;border-radius:8px}'
    h+='.support-info b{color:#00FF80;display:block;margin-bottom:6px;font-size:11px}'
    h+='.support-info p{margin:5px 0;font-size:11px;color:#D2DCD2}'
    h+='.support-tel{font-size:18px;font-weight:900;color:#FFD700;letter-spacing:2px;margin:12px 0}'
    
    # Legal
    h+='.legal{font-size:8px;color:#8EA88E;line-height:1.6;text-align:justify;margin-top:18px;border-top:1px solid rgba(255,255,255,0.1);padding-top:12px}'
    h+='.legal b{color:#FFD700}'
    
    # Footer
    h+='.foot{margin-top:auto;background:#020402;padding:15px;text-align:center;font-size:8px;color:#3A5A3A;border-top:1px solid #0D1A0D;letter-spacing:1.5px;width:100%}'
    h+='</style>'
    
    # HTML
    h+='<div class=hero>'
    h+='<div class=logo-container>'
    h+='<div class=sigla>S.I.E.A.</div>'
    h+='<div class=sub>SISTEMA INTEGRAL DE EVALUACIÓN PARA EL ASCENSO</div>'
    h+='<div class=tagline>🎓 Plataforma Profesional de Evaluación y Capacitación</div>'
    h+='</div>'
    h+='<div class=purpose>'
    h+='<b>✨ Propósito y Función Institucional</b>'
    h+='<p>Plataforma integral de fortalecimiento académico diseñada bajo estrictos estándares de calidad para optimizar la preparación, evaluación y profesionalización del personal. Sistema seguro, confiable y accesible que promueve la excelencia institucional.</p>'
    h+='</div>'
    h+='</div>'
    
    h+='<div class=container>'
    
    # TARJETA LOGIN
    h+='<div class=card>'
    h+='<div class=card-header>'
    h+='<div class="card-title card-title-login">🔐 ACCESO AL SISTEMA</div>'
    h+='<div class=subtitle>Ingrese sus credenciales</div>'
    h+='</div>'
    if mensaje: h+=mensaje
    h+='<div class=tab-buttons>'
    h+='<button type=button class="tab-btn active" onclick="document.querySelectorAll(\'.tab-content\').forEach(e=>e.classList.remove(\'active\')); document.getElementById(\'login-form\').classList.add(\'active\')">INGRESAR</button>'
    h+='<button type=button class="tab-btn" onclick="document.querySelectorAll(\'.tab-content\').forEach(e=>e.classList.remove(\'active\')); document.getElementById(\'register-form\').classList.add(\'active\')">REGISTRARSE</button>'
    h+='</div>'
    
    # Formulario Login
    h+='<div id=login-form class="tab-content active">'
    h+='<form method=post action=/login>'
    h+='<div class=lbl>👤 Usuario / Matrícula</div>'
    h+='<input class=inp name=user placeholder="Ej. EMP001" required>'
    h+='<div class=lbl>🔑 Contraseña</div>'
    h+='<input class=inp type=password name=pass placeholder="••••••••" required>'
    h+='<button class=btn>INGRESAR AL SISTEMA</button>'
    h+='</form>'
    h+='</div>'
    
    # Formulario Registro
    h+='<div id=register-form class="tab-content">'
    h+='<form method=post action=/register>'
    h+='<div class=lbl>👤 Usuario / Matrícula</div>'
    h+='<input class=inp name=new_user placeholder="Ej. EMP001" required>'
    h+='<div class=lbl>📝 Nombre Completo</div>'
    h+='<input class=inp name=full_name placeholder="Juan Pérez García" required>'
    h+='<div class=lbl>📧 Correo Electrónico</div>'
    h+='<input class=inp type=email name=email placeholder="tu@correo.com" required>'
    h+='<div class=lbl>🔑 Crear Contraseña</div>'
    h+='<input class=inp type=password name=new_pass placeholder="Min. 8 caracteres" required minlength=8>'
    h+='<div class=lbl>✓ Confirmar Contraseña</div>'
    h+='<input class=inp type=password name=confirm_pass placeholder="Repetir contraseña" required minlength=8>'
    h+='<button class="btn btn-register">✓ REGISTRARSE</button>'
    h+='<p style="font-size:10px;color:#8AB38A;margin-top:10px;text-align:center">Tu solicitud será revisada por un administrador</p>'
    h+='</form>'
    h+='</div>'
    
    h+='<div class=legal>'
    h+='<b>⚖️ AVISO DE CONFIDENCIALIDAD:</b> La información en esta plataforma es estrictamente confidencial y de uso exclusivo autorizado. Prohibido compartir credenciales. Violaciones serán reportadas.'
    h+='</div>'
    h+='</div>'
    
    # TARJETA ADMINISTRADOR
    h+='<div class="card card-admin">'
    h+='<div class=card-header>'
    h+='<div class="card-title card-title-admin">⚙️ PANEL ADMINISTRATIVO</div>'
    h+='<div class=subtitle>Acceso exclusivo - Ingrese contraseña</div>'
    h+='</div>'
    h+='<form method=post action=/admin_login>'
    h+='<div class=lbl>🔐 Contraseña Administrador</div>'
    h+='<input class=inp type=password name=admin_pass placeholder="••••••••" required>'
    h+='<button class="btn btn-admin">ACCEDER A ADMINISTRACIÓN</button>'
    h+='</form>'
    h+='</div>'
    
    # TARJETA SOPORTE
    h+='<div class="card card-support">'
    h+='<div class=card-header>'
    h+='<div class="card-title card-title-support">📞 SOPORTE Y SUSCRIPCIÓN</div>'
    h+='</div>'
    h+='<div class=support-info>'
    h+='<b>☎️ SOPORTE TÉCNICO</b>'
    h+='<p>Para dudas, reportes o asistencia inmediata:</p>'
    h+='<div class=support-tel>+52 811 0290152</div>'
    h+='<p style="font-size:10px;color:#FFD700">Lunes a Viernes | 08:00 - 18:00 hrs</p>'
    h+='</div>'
    h+='<div class=support-info>'
    h+='<b>💳 SUSCRIPCIÓN PREMIUM</b>'
    h+='<p>Acceso ilimitado a todas las materias, reactivos y evaluaciones personalizadas.</p>'
    h+='<p style="font-size:11px;font-weight:700;color:#00FF80;margin-top:10px">Precio: <span style="color:#FFD700">$9.99 USD/mes</span></p>'
    h+='<p style="font-size:10px;margin-top:8px">Contacte al administrador para más información</p>'
    h+='</div>'
    h+='</div>'
    
    h+='</div>'
    h+='<div class=foot>© 2026 S.I.E.A. - Plataforma de Evaluación Institucional | Todos los derechos reservados</div>'
    
    return h

# ============== PÁGINA BASE ==============
def base(t,b):
    u=session.get("user","")
    role=session.get("role","user")
    frases=["📚 La disciplina es la clave del éxito", "💡 La constancia vence lo que la dicha no alcanza", "🎯 El conocimiento es poder", "✨ Cada pregunta te acerca al éxito"]
    f_activa = random.choice(frases)
    h=""
    h+='<meta name=viewport content="width=device-width,initial-scale=1">'
    h+='<meta charset="UTF-8">'
    h+='<link href="https://fonts.googleapis.com/css2?family=Montserrat:ital,wght@0,400;0,700;0,900;1,400;1,700&display=swap" rel="stylesheet">'
    h+='<style>'
    h+='body{margin:0;background:#050B05;color:#E0EFE0;font-family:Montserrat,system-ui}'
    h+='.top{background:linear-gradient(90deg,#00FF80,#00B359);color:#050905;padding:12px;text-align:center;font-weight:900;font-style:italic;font-size:14px;letter-spacing:2px;box-shadow:0 4px 15px rgba(0,255,128,0.3)}'
    h+='.bar{background:#0D1A0D;padding:12px 16px;display:flex;justify-content:space-between;align-items:center;border-bottom:2px solid #00FF80;flex-wrap:wrap;gap:10px}'
    h+='.user-info{font-size:12px;color:#00FF80;font-weight:700}'
    h+='.sub-bar{font-size:10px;color:#A0C8A0;font-style:italic;margin-top:2px}'
    h+='.btn-back{background:#1A331A;color:#fff;padding:8px 14px;border-radius:7px;text-decoration:none;font-size:11px;border:1px solid #2E5A2E;display:inline-block;margin:2px;transition:all 0.3s}'
    h+='.btn-back:hover{background:#2E5A2E;box-shadow:0 0 10px rgba(0,255,128,0.2)}'
    h+='.btn-admin-dash{background:linear-gradient(180deg,#FFD700,#CCAC00);color:#050905;padding:8px 14px;border-radius:7px;text-decoration:none;font-size:11px;font-weight:700;display:inline-block;margin:2px}'
    h+='.btn-logout{background:#4D1A1A;color:#ff9999;padding:8px 14px;border-radius:7px;text-decoration:none;font-size:11px;display:inline-block;margin:2px}'
    h+='.sec-title{color:#050905;padding:12px;text-align:center;font-weight:900;border-radius:9px;margin:12px;font-size:12px;letter-spacing:1px}'
    h+='.title-materias{background:linear-gradient(90deg,#FFD700,#FFA500)}'
    h+='.card{border-radius:12px;padding:14px;margin:10px 12px;box-shadow:0 4px 12px rgba(0,0,0,0.6);border-left:6px solid #00FF80}'
    h+='.card-gen{background:linear-gradient(180deg,#1A1605,#0D0B02);border:2px solid #FFD700}'
    h+='.btn{width:100%;padding:12px;border:0;border-radius:8px;font-weight:800;margin-top:8px;cursor:pointer;font-size:12px;background:linear-gradient(180deg,#00FF80,#00B359);color:#050905;transition:all 0.3s}'
    h+='.btn:hover{transform:translateY(-2px);box-shadow:0 8px 20px rgba(0,255,128,0.3)}'
    h+='</style>'
    h+=f'<div class=top>S.I.E.A. - {t}</div>'
    botones='<a href=/ class=btn-back>🏠 INICIO</a>'
    if role=="admin": botones+=' <a href=/admin_dashboard class=btn-admin-dash>⚙️ ADMINISTRACIÓN</a>'
    botones+=' <a href=/logout class=btn-logout>🚪 CERRAR SESIÓN</a>'
    h+=f'<div class=bar><div><div class=user-info>👤 {u}</div><div class=sub-bar>{f_activa}</div></div><div>{botones}</div></div>'
    return h + b

# ============== RUTAS ==============
@app.route("/")
def index():
    if "user" not in session:
        return login_page()
    return dashboard()

def dashboard():
    u=session.get("user")
    h='<div class="sec-title title-materias">📚 PANEL DE INICIO</div>'
    h+='<div class=card><b>✓ Bienvenido al Sistema</b><p style="font-size:11px;margin:8px 0">Acceso a todas las herramientas de evaluación y capacitación</p>'
    h+='<button class=btn onclick="location.href=\'/examenes\'">📝 MIS EXÁMENES</button>'
    h+='<button class=btn onclick="location.href=\'/banco_preguntas\'">❓ BANCO DE PREGUNTAS</button>'
    h+='<button class=btn onclick="location.href=\'/historial\'">📊 MI HISTORIAL</button>'
    h+='</div>'
    return base("INICIO",h)

@app.route("/login", methods=["POST"])
def login():
    u=request.form.get("user","").strip().upper()
    p=request.form.get("pass","").strip()
    us=ld_u()
    
    if u not in us:
        return login_page('<div class=error-msg>❌ Usuario no encontrado. Regístrese primero.</div>')
    
    if us[u]["password_hash"] != hash_password(p):
        return login_page('<div class=error-msg>❌ Contraseña incorrecta.</div>')
    
    usuario = us[u]
    if usuario.get("status") != "aprobado":
        return login_page(f'<div class=warning-msg>⏳ Tu cuenta está <b>PENDIENTE DE APROBACIÓN</b>. El administrador revisará tu solicitud pronto. Contacta: +52 811 0290152</div>')
    
    session["user"] = u
    session["role"] = usuario.get("role", "user")
    session["email"] = usuario.get("email", "")
    return redirect("/")

@app.route("/register", methods=["POST"])
def register():
    u=request.form.get("new_user","").strip().upper()
    full_name=request.form.get("full_name","").strip()
    e=request.form.get("email","").strip()
    p=request.form.get("new_pass","").strip()
    p_confirm=request.form.get("confirm_pass","").strip()
    
    if not all([u, full_name, e, p, p_confirm]):
        return login_page('<div class=error-msg>❌ Faltan datos en el formulario.</div>')
    
    if p != p_confirm:
        return login_page('<div class=error-msg>❌ Las contraseñas no coinciden.</div>')
    
    if len(p) < 8:
        return login_page('<div class=error-msg>❌ La contraseña debe tener al menos 8 caracteres.</div>')
    
    us = ld_u()
    pendientes = ld_pendientes()
    
    if u in us or u in pendientes:
        return login_page('<div class=error-msg>❌ Este usuario ya existe.</div>')
    
    # Guardar en pendientes
    pendientes[u]={
        "full_name":full_name,
        "email":e,
        "password_hash":hash_password(p),
        "status":"pendiente",
        "role":"user",
        "created_at":dt.now().strftime("%d/%m/%Y %H:%M")
    }
    sv_pendientes(pendientes)
    
    return login_page('<div class=success-msg>✓ ¡Registro enviado! Tu solicitud será revisada por el administrador en breve. Recibirás un correo de confirmación.</div>')

@app.route("/admin_login", methods=["POST"])
def admin_login():
    admin_pass = request.form.get("admin_pass", "").strip()
    # Contraseña: Admin123 (hasheada)
    admin_hash = hash_password("Admin123")
    
    if hash_password(admin_pass) != admin_hash:
        return login_page('<div class=error-msg>❌ Contraseña de administrador incorrecta.</div>')
    
    session["user"] = "ADMIN"
    session["role"] = "admin"
    session["email"] = "admin@siea.com"
    return redirect("/admin_dashboard")

@app.route("/admin_dashboard")
@require_login
@require_admin
def admin_dashboard():
    pendientes = ld_pendientes()
    us = ld_u()
    
    h='<div class="sec-title title-materias">⚙️ PANEL DE ADMINISTRACIÓN</div>'
    h+='<div class=card><b>📋 Usuarios Pendientes de Aprobación</b>'
    
    if not pendientes:
        h+='<p style="font-size:11px;color:#8AB38A;margin:8px 0">No hay usuarios pendientes</p>'
    else:
        for user_id, datos in pendientes.items():
            h+=f'''<div style="background:#0D260D;padding:10px;margin:8px 0;border-radius:8px;border-left:4px solid #00FF80">
            <p style="font-size:11px;margin:4px 0"><b>{user_id}</b> - {datos.get('full_name','')}</p>
            <p style="font-size:10px;color:#8AB38A;margin:4px 0">{datos.get('email','')}</p>
            <form method=post action=/aprobar_usuario style="display:inline">
                <input type=hidden name=user value="{user_id}">
                <button class="btn" style="width:auto;padding:6px 12px;margin:4px 0">✓ APROBAR</button>
            </form>
            <form method=post action=/rechazar_usuario style="display:inline">
                <input type=hidden name=user value="{user_id}">
                <button class="btn" style="width:auto;padding:6px 12px;margin:4px 0;background:#4D1A1A">✗ RECHAZAR</button>
            </form>
            </div>'''
    
    h+='</div>'
    
    h+='<div class=card><b>👥 Usuarios Activos</b>'
    h+=f'<p style="font-size:11px;margin:8px 0">Total: {len(us)} usuarios registrados</p>'
    h+='</div>'
    
    return base("ADMINISTRACIÓN",h)

@app.route("/aprobar_usuario", methods=["POST"])
@require_login
@require_admin
def aprobar_usuario():
    user_id = request.form.get("user", "").strip().upper()
    pendientes = ld_pendientes()
    us = ld_u()
    
    if user_id not in pendientes:
        return redirect("/admin_dashboard")
    
    # Mover a usuarios aprobados
    datos = pendientes[user_id]
    datos["status"] = "aprobado"
    us[user_id] = datos
    
    del pendientes[user_id]
    sv_pendientes(pendientes)
    sv_u(us)
    
    return redirect("/admin_dashboard")

@app.route("/rechazar_usuario", methods=["POST"])
@require_login
@require_admin
def rechazar_usuario():
    user_id = request.form.get("user", "").strip().upper()
    pendientes = ld_pendientes()
    
    if user_id in pendientes:
        del pendientes[user_id]
        sv_pendientes(pendientes)
    
    return redirect("/admin_dashboard")

@app.route("/examenes")
@require_login
def examenes():
    h='<div class="sec-title title-materias">📝 MIS EXÁMENES</div>'
    h+='<div class=card><b>Examen General</b><p style="font-size:11px;margin:8px 0">Todas las materias juntas</p><button class=btn>INICIAR EXAMEN</button></div>'
    h+='<div class=card><b>Examen Personalizado</b><p style="font-size:11px;margin:8px 0">Selecciona materias específicas</p><button class=btn>CREAR EXAMEN</button></div>'
    return base("EXÁMENES",h)

@app.route("/banco_preguntas")
@require_login
def banco_preguntas():
    preguntas = ld()
    u = session.get("user")
    mis_preg = [p for p in preguntas if p.get("usuario")==u]
    
    h='<div class="sec-title title-materias">❓ BANCO DE PREGUNTAS</div>'
    h+='<div class=card><b>➕ NUEVA PREGUNTA</b><form method=post action=/add_pregunta>'
    h+='<textarea name=pregunta placeholder="Escriba la pregunta" style="width:100%;padding:10px;border-radius:8px;border:1px solid #1A401A" required></textarea>'
    h+='<input name=op_a placeholder="Opción A" class=inp required>'
    h+='<input name=op_b placeholder="Opción B" class=inp required>'
    h+='<input name=op_c placeholder="Opción C" class=inp required>'
    h+='<input name=op_d placeholder="Opción D" class=inp required>'
    h+='<select name=correcta class=inp required><option>Selecciona respuesta correcta</option><option>A</option><option>B</option><option>C</option><option>D</option></select>'
    h+='<button class=btn>✓ GUARDAR PREGUNTA</button></form></div>'
    
    h+=f'<div class=card><b>Mis preguntas ({len(mis_preg)})</b>'
    if not mis_preg:
        h+='<p style="font-size:11px;color:#8AB38A">No hay preguntas aún</p>'
    else:
        for i,p in enumerate(mis_preg):
            h+=f'<div style="background:#0D1A0D;padding:10px;margin:8px 0;border-radius:8px"><p style="font-size:11px">{p.get("pregunta","")}</p></div>'
    h+='</div>'
    
    return base("BANCO DE PREGUNTAS",h)

@app.route("/add_pregunta", methods=["POST"])
@require_login
def add_pregunta():
    u = session.get("user")
    pregunta = request.form.get("pregunta", "").strip()
    opciones = [request.form.get(f"op_{x}", "").strip() for x in ['a','b','c','d']]
    correcta = request.form.get("correcta", "").strip().upper()
    
    if not all([pregunta, all(opciones), correcta in ['A','B','C','D']]):
        return redirect("/banco_preguntas")
    
    preguntas = ld()
    preguntas.append({
        "id": str(uuid.uuid4()),
        "usuario": u,
        "pregunta": pregunta,
        "opciones": {x: opciones[i] for i,x in enumerate(['A','B','C','D'])},
        "correcta": correcta,
        "created_at": dt.now().strftime("%d/%m/%Y %H:%M")
    })
    sv(preguntas)
    
    return redirect("/banco_preguntas")

@app.route("/historial")
@require_login
def historial():
    h='<div class="sec-title title-materias">📊 MI HISTORIAL</div>'
    h+='<div class=card><b>Exámenes Realizados</b><p style="font-size:11px;margin:8px 0">Aquí aparecerán tus resultados</p></div>'
    return base("HISTORIAL",h)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5002))
    app.run(host='0.0.0.0', port=port, debug=False)
