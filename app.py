import os, json, random
from flask import Flask, request, redirect, session
app = Flask(__name__)
app.secret_key = "siea_app_produccion_playstore_definitivo_2026"

DB_USERS = os.path.expanduser("~/usuarios_siea.json")

def ld_u():
 try:
  if os.path.exists(DB_USERS):
   with open(DB_USERS) as f: return json.load(f)
 except: pass
 return {}

def sv_u(d):
 with open(DB_USERS,"w") as f: json.dump(d,f)

def get_paths():
 usr = session.get("user", "default_user")
 safe_usr = "".join([c if c.isalnum() else "_" for c in usr])
 db = os.path.expanduser(f"~/preg_{safe_usr}.json")
 hu = os.path.expanduser(f"~/hist_{safe_usr}.json")
 mm = os.path.expanduser(f"~/materias_{safe_usr}.json")
 return db, hu, mm

def ld():
 db, _, _ = get_paths()
 try:
  if os.path.exists(db):
   with open(db) as f: return json.load(f)
 except: pass
 return []
def sv(d):
 db, _, _ = get_paths()
 with open(db,"w") as f: json.dump(d,f)

def ld_h():
 _, hu, _ = get_paths()
 try:
  if os.path.exists(hu):
   with open(hu) as f: return json.load(f)
 except: pass
 return []
def sv_h(d):
 _, hu, _ = get_paths()
 with open(hu,"w") as f: json.dump(d,f)

def ld_m():
 _, _, mm = get_paths()
 try:
  if os.path.exists(mm):
   with open(mm) as f: return json.load(f)
 except: pass
 return ["HI","MOM","LEY ORGANICA"]
def sv_m(d):
 _, _, mm = get_paths()
 with open(mm,"w") as f: json.dump(d,f)

# --- 1. PANTALLA DE REGISTRO DE USUARIO ---
@app.route("/registro", methods=["GET", "POST"])
def registro():
 msg = ""
 if request.method == "POST":
  nombre = request.form.get("nombre", "").strip()
  correo = request.form.get("correo", "").strip()
  telefono = request.form.get("telefono", "").strip()
  u = request.form.get("user", "").strip().upper()
  p = request.form.get("pass", "").strip()
  
  if not nombre or not correo or not telefono or not u or not p:
   msg = "Todos los campos son obligatorios para el registro."
  else:
   us = ld_u()
   if u in us:
    msg = "La matrícula o usuario ya se encuentra registrado."
   else:
    us[u] = {"nombre": nombre, "correo": correo, "telefono": telefono, "pass": p}
    sv_u(us)
    return redirect("/?registrado=1")

 h='<meta name=viewport content="width=device-width,initial-scale=1">'
 h+='<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700;900&display=swap" rel="stylesheet">'
 h+='<style>'
 h+='body{margin:0;background:#051C05;color:#fff;font-family:Montserrat,system-ui;min-height:100vh;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:20px 0}'
 h+='.card-login{width:92%;max-width:400px;background:#0A2F0A;border:2px solid #FFD700;border-radius:16px;padding:22px;box-sizing:border-box}'
 h+='.sigla{font-size:28px;font-weight:900;letter-spacing:3px;color:#FFD700;text-align:center;margin-bottom:4px}'
 h+='.sub{font-size:10px;letter-spacing:2px;color:#81C784;text-align:center;font-weight:700;margin-bottom:15px}'
 h+='.lbl{font-size:9px;letter-spacing:1px;color:#FFD700;font-weight:700;margin:8px 0 2px 2px}'
 h+='.inp{width:100%;padding:11px;background:#051C05;border:1.5px solid #FFD700;border-radius:8px;color:#fff;box-sizing:border-box;font-size:13px}'
 h+='.btn{width:100%;padding:13px;border:0;border-radius:8px;font-weight:900;letter-spacing:1px;margin-top:14px;background:linear-gradient(180deg,#FFCA28,#FFA000);color:#000;cursor:pointer;font-size:12px}'
 h+='.btn-vol{background:#2E7D32;color:#fff;margin-top:8px;display:block;text-align:center;text-decoration:none;padding:11px;border-radius:8px;font-weight:900;font-size:12px}'
 h+='.msg{background:#5A1A1A;color:#FF8A80;padding:6px;border-radius:6px;font-size:11px;text-align:center;margin-bottom:8px}'
 h+='</style>'
 h+='<div class=card-login>'
 h+='<div class=sigla>S.I.E.A.</div>'
 h+='<div class=sub>REGISTRO OFICIAL DE USUARIO</div>'
 if msg: h+=f'<div class=msg>{msg}</div>'
 h+='<form method=post>'
 h+='<div class=lbl>NOMBRE COMPLETO</div><input class=inp name=nombre placeholder="Tu nombre completo" required>'
 h+='<div class=lbl>CORREO ELECTRONICO</div><input class=inp type=email name=correo placeholder="correo@ejemplo.com" required>'
 h+='<div class=lbl>NUMERO TELEFONICO</div><input class=inp type=tel name=telefono placeholder="10 dígitos" required>'
 h+='<div class=lbl>USUARIO / MATRICULA</div><input class=inp name=user placeholder="Tu matrícula única" required>'
 h+='<div class=lbl>CONTRASENA</div><input class=inp type=password name=pass placeholder="********" required>'
 h+='<button class=btn>COMPLETAR REGISTRO</button>'
 h+='</form>'
 h+='<a href=/ class=btn-vol>⬅️ VOLVER AL LOGIN</a>'
 h+='</div>'
 return h

# --- 2. PANTALLA DE LOGIN INSTITUCIONAL CON PAGOS Y WHATSAPP ---
@app.route("/", methods=["GET", "POST"])
def login_page():
 msg = ""
 if request.args.get("registrado"):
  msg = "¡Registro exitoso! Ya puedes iniciar sesión."
 
 if request.method == "POST":
  u = request.form.get("user", "").strip().upper()
  p = request.form.get("pass", "").strip()
  us = ld_u()
  if u in us and us[u].get("pass") == p:
   session["user"] = u
   return redirect("/")
  else:
   msg = "Usuario o contraseña incorrectos."

 if "user" in session:
  return panel_principal()

 h='<meta name=viewport content="width=device-width,initial-scale=1">'
 h+='<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700;900&display=swap" rel="stylesheet">'
 h+='<style>'
 h+='body{margin:0;background:#051C05;color:#fff;font-family:Montserrat,system-ui;min-height:100vh;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:20px}'
 h+='.card-login{width:94%;max-width:420px;background:#0A2F0A;border:2px solid #4CAF50;border-radius:16px;padding:24px;box-sizing:border-box}'
 h+='.sigla{font-size:34px;font-weight:900;letter-spacing:4px;color:#FFD700;text-align:center;margin-bottom:4px}'
 h+='.sub{font-size:10px;letter-spacing:2px;color:#81C784;text-align:center;font-weight:700;margin-bottom:14px}'
 h+='.info-box{background:#051C05;border:1px solid #2E7D32;border-radius:8px;padding:10px;font-size:10px;color:#C8E6C9;line-height:1.4;margin-bottom:14px;text-align:justify}'
 h+='.lbl{font-size:9px;letter-spacing:1px;color:#FFD700;font-weight:700;margin:8px 0 2px 2px}'
 h+='.inp{width:100%;padding:11px;background:#051C05;border:1.5px solid #4CAF50;border-radius:8px;color:#fff;box-sizing:border-box;font-size:13px}'
 h+='.btn{width:100%;padding:13px;border:0;border-radius:8px;font-weight:900;letter-spacing:1px;margin-top:14px;background:linear-gradient(180deg,#66BB6A,#2E7D32);color:#fff;cursor:pointer;font-size:12px}'
 h+='.btn-reg{background:linear-gradient(180deg,#FFCA28,#FFA000);color:#000;margin-top:8px;display:block;text-align:center;text-decoration:none;padding:11px;border-radius:8px;font-weight:900;font-size:12px}'
 h+='.btn-pay{background:linear-gradient(180deg,#AB47BC,#7B1FA2);color:#fff;margin-top:8px;display:block;text-align:center;text-decoration:none;padding:10px;border-radius:8px;font-weight:900;font-size:11px}'
 h+='.whatsapp{text-align:center;margin-top:12px;font-size:11px}'
 h+='.whatsapp a{color:#81C784;text-decoration:none;font-weight:bold}'
 h+='.msg{background:#5A1A1A;color:#FF8A80;padding:6px;border-radius:6px;font-size:11px;text-align:center;margin-bottom:8px}'
 h+='</style>'
 h+='<div class=card-login>'
 h+='<div class=sigla>S.I.E.A.</div>'
 h+='<div class=sub>SISTEMA INTEGRAL DE EVALUACION</div>'
 h+='<div class=info-box><b>Propósito Institucional:</b> Plataforma avanzada para la gestión, práctica y evaluación de reactivos oficiales.<br><br><b>Aviso de Privacidad:</b> Tus datos e historial se encuentran protegidos de forma independiente por cada usuario registrado.</div>'
 if msg: h+=f'<div class=msg>{msg}</div>'
 h+='<form method=post>'
 h+='<div class=lbl>USUARIO / MATRICULA</div><input class=inp name=user placeholder="Ingresa tu matrícula" required>'
 h+='<div class=lbl>CONTRASENA</div><input class=inp type=password name=pass placeholder="********" required>'
 h+='<button class=btn>INGRESAR AL SISTEMA</button>'
 h+='</form>'
 h+='<a href=/registro class=btn-reg>📝 REGISTRAR NUEVO USUARIO</a>'
 h+='<a href="https://wa.me/528110290152?text=Hola,%20deseo%20pagar%20la%20suscripción%20para%20activar%20la%20app%20SIEA" target=_blank class=btn-pay>💳 PAGAR SUSCRIPCIÓN / MONETIZACIÓN</a>'
 h+='<div class=whatsapp>📞 WhatsApp de Contacto: <a href="https://wa.me/528110290152" target=_blank>+52 81 1029 0152</a></div>'
 h+='</div>'
 return h

@app.route("/logout")
def lo():
 session.clear()
 return redirect("/")

# --- 3. DISEÑO BASE Y FUNCIONALIDADES DE LA APP ---
def base(t,b):
 u=session.get("user","")
 h='<meta name=viewport content="width=device-width,initial-scale=1"><style>'
 h+='body{margin:0;background:#061A06;color:#fff;font-family:system-ui}'
 h+='.top{background:#FFD700;color:#000;padding:10px;text-align:center;font-weight:900;font-size:13px}'
 h+='.bar{background:#0D2E0D;padding:10px 14px;display:flex;justify-content:space-between;align-items:center;border-bottom:3px solid #4CAF50}'
 h+='.btn-back{background:#1B5E20;color:#fff;padding:7px 12px;border-radius:7px;text-decoration:none;font-size:11px;border:1px solid #4CAF50;font-weight:bold}'
 h+='.btn-inicio{background:linear-gradient(180deg,#FFCA28,#FFA000);color:#000;padding:8px 14px;border-radius:8px;text-decoration:none;font-size:11px;font-weight:900}'
 h+='.sec-title{color:#000;padding:12px;text-align:center;font-weight:900;border-radius:9px;margin:12px;font-size:13px}'
 h+='.title-materias{background:linear-gradient(90deg,#FFCA28,#FFA000);color:#000}'
 h+='.title-trabajando{background:linear-gradient(90deg,#00E676,#1DE9B6);color:#000}'
 h+='.title-historial{background:linear-gradient(90deg,#9C27B0,#E040FB);color:#fff}'
 h+='.title-examen{background:linear-gradient(90deg,#29B6F6,#00B0FF);color:#000}'
 h+='.card{border-radius:12px;padding:14px;margin:10px 12px;box-shadow:0 4px 12px rgba(0,0,0,0.5)}'
 h+='.card-create{background:linear-gradient(180deg,#0B2E0B,#061F06);border:2px dashed #FFD700}'
 h+='.card-hi{background:linear-gradient(180deg,#0F380F,#082008);border-left:6px solid #4CAF50}'
 h+='.btn{width:100%;padding:12px;border:0;border-radius:8px;font-weight:800;margin-top:8px;cursor:pointer;font-size:12px}'
 h+='.btn-green{background:linear-gradient(180deg,#66BB6A,#2E7D32);color:#fff}'
 h+='.btn-gold{background:linear-gradient(180deg,#FFCA28,#FFA000);color:#000}'
 h+='.btn-edit{background:#FFD700;color:#000;padding:8px 14px;border-radius:6px;text-decoration:none;font-size:11px;font-weight:900;display:inline-block}'
 h+='.btn-del{background:#D32F2F;color:#fff;padding:8px 14px;border-radius:6px;text-decoration:none;font-size:11px;font-weight:bold;display:inline-block;margin-left:6px}'
 h+='.input{width:100%;padding:11px;background:#051A05;border:1px solid #4CAF50;border-radius:8px;color:#fff;margin:5px 0;box-sizing:border-box}'
 h+='.opt{display:block;background:#0A290A;border:1px solid #2E7D32;padding:10px;margin:6px 0;border-radius:8px}'
 h+='.badge{padding:3px 10px;border-radius:12px;font-size:10px;font-weight:900}'
 h+='</style>'
 h+=f'<div class=top>S.I.E.A. - {t}</div><div class=bar><b style=color:#FFD700>Bienvenido, {u}</b><div><a href=/historial class=btn-back>HISTORIAL</a> <a href=/logout class=btn-back>SALIR</a></div></div>'
 return h + b

# --- 4. PANEL PRINCIPAL Y GESTIÓN DE MATERIAS ---
@app.route("/panel")
def panel_principal():
 return panel_logica()

def panel_logica():
 ma=session.get("materia_actual")
 materias=ld_m()
 total_preg=len(ld())
 if not ma:
  ms={}
  for p in ld(): ms[p["materia"]]=ms.get(p["materia"],0)+1
  h='<div class="sec-title title-materias">📚 PANEL PRINCIPAL DE MATERIAS Y GESTION</div>'
  h+='<div class="card card-create"><b style=color:#FFD700>➕ CREAR NUEVA MATERIA PERSONALIZADA</b><p style=font-size:11px;color:#A5D6A7;margin:6px 0>Asigne una nomenclatura oficial y cree su materia; posteriormente podrá administrar sus reactivos internos.</p><form method=post action=/add_materia><input class=input name=nueva_materia placeholder="Ej: DERECHOS HUMANOS, ARMAMENTO, LEGISLACION..." required><button class="btn btn-gold" style=font-weight:900>✅ REGISTRAR Y CREAR MATERIA</button></form></div>'
  
  for idx,m in enumerate(materias):
   c=ms.get(m,0)
   h+=f'<div class=card card-hi><div style=display:flex;justify-content:space-between;align-items:center;margin-bottom:8px><span style=font-weight:900;font-size:14px;color:#FFD700>📘 {m}</span><span class=badge style=background:#4CAF50;color:#fff>{c} PREGUNTAS</span></div>'
   h+=f'<form method=post action=/set_materia><input type=hidden name=materia value="{m}"><button class="btn btn-green" style=font-weight:900>📁 ACCEDER A {m} - GESTION Y REACTIVOS</button></form>'
   h+=f'<div style=margin-top:10px;display:flex;gap:6px><a href=/edit_materia/{idx} class=btn-edit style=flex:1;text-align:center>✏️ EDITAR MATERIA</a><a href=/del_materia/{idx} class=btn-del style=flex:1;text-align:center>🗑️ BORRAR</a></div>'
   h+=f'<div style=margin-top:8px><form method=post action=/exam_materia><input type=hidden name=m value="{m}"><button class="btn" style=background:#1B5E20;color:#81C784;border:1px solid #4CAF50;padding:9px;font-size:11px>📝 EXAMEN DE {m} ({c} preg)</button></form></div></div>'
  
  if total_preg>0:
   h+=f'<div class=card style=background:linear-gradient(180deg,#2E2605,#1A1503);border:2px solid #FFD700><div style=display:flex;justify-content:space-between;align-items:center><b style=color:#FFD700>⭐ EXAMEN GENERAL</b><span class=badge style=background:#FFD700;color:#000>{total_preg} PREGUNTAS</span></div><p style=font-size:11px;color:#FFEE58;margin:6px 0>Examen combinado con todas sus materias registradas</p><form method=post action=/exam_general><button class="btn btn-gold">🚀 INICIAR EXAMEN GENERAL</button></form></div>'
  return base("INICIO",h)

 pr=[p for p in ld() if p["materia"]==ma]
 allp=ld()
 b='<div style=margin:12px><a href=/cambiar class=btn-inicio>🏠 VOLVER AL PANEL</a></div>'
 b+=f'<div class="sec-title title-trabajando">📂 TRABAJANDO EN MATERIA: {ma} - {len(pr)} PREGUNTAS</div>'
 b+=f'<div class="card card-create"><b style=color:#FFD700>➕ CREAR NUEVA PREGUNTA EN {ma}</b><form method=post action=/add><input class=input name=p placeholder="Escribe la pregunta completa" required><input class=input name=o1 placeholder="Opcion A) (Correcta)" required><input class=input name=o2 placeholder="Opcion B)" required><input class=input name=o3 placeholder="Opcion C)" required><input class=input name=o4 placeholder="Opcion D)" required><select class=input name=c><option value=0>A es la correcta</option><option value=1>B es la correcta</option><option value=2>C es la correcta</option><option value=3>D es la correcta</option></select><button class="btn btn-green">💾 GUARDAR PREGUNTA</button></form></div>'
 for p in allp:
  if p["materia"]!=ma: continue
  idx = allp.index(p)
  letras=["A","B","C","D"]
  correcta=letras[p["co"]]
  b+=f'<div class=card card-hi><div style=display:flex;justify-content:space-between><span class=badge style=background:#FFD700;color:#000>{p["materia"]}</span><span class=badge style=background:#4CAF50;color:#fff>Correcta: {correcta}</span></div><b style=display:block;margin:10px 0;font-size:13px;color:#E8F5E9>{p["p"]}</b><div style=font-size:11px;line-height:1.6;color:#C8E6C9>A) {p["op"][0]}<br>B) {p["op"][1]}<br>C) {p["op"][2]}<br>D) {p["op"][3]}</div><div style=margin-top:12px><a href=/edit/{idx} class=btn-edit>✏️ EDITAR</a><a href=/del/{idx} class=btn-del>🗑️ BORRAR</a></div></div>'
 return base(ma,b)

@app.route("/add_materia",methods=["POST"])
def add_mat():
 nueva=request.form.get("nueva_materia","").strip().upper()
 mats=ld_m()
 if nueva and nueva not in mats: mats.append(nueva); sv_m(mats)
 return redirect("/")

@app.route("/edit_materia/<int:i>",methods=["GET","POST"])
def edit_mat(i):
 mats=ld_m()
 if not (0<=i<len(mats)): return redirect("/")
 if request.method=="POST":
  nuevo=request.form.get("nuevo_nombre","").strip().upper()
  if nuevo:
   viejo=mats[i]; preg=ld()
   for p in preg:
    if p["materia"]==viejo: p["materia"]=nuevo
   sv(preg); mats[i]=nuevo; sv_m(mats)
  return redirect("/")
 viejo=mats[i]
 return base("EDITAR MATERIA",f'<div class=card card-create style=margin:12px><b style=color:#FFD700>✏️ EDITAR MATERIA: {viejo}</b><form method=post><input class=input name=nuevo_nombre value="{viejo}" required><button class="btn btn-green">💾 GUARDAR CAMBIO</button></form></div>')

@app.route("/del_materia/<int:i>")
def del_mat(i):
 mats=ld_m()
 if 0<=i<len(mats):
  bor=mats[i]
  preg=[x for x in ld() if x["materia"]!=bor]
  sv(preg); mats.pop(i); sv_m(mats)
 return redirect("/")

@app.route("/set_materia",methods=["POST"])
def sm():
 m=request.form.get("materia","").strip().upper()
 if m: session["materia_actual"]=m
 return redirect("/")

@app.route("/cambiar")
def ca():
 session.pop("materia_actual",None)
 return redirect("/")

# --- 5. HISTORIAL DE EXÁMENES ---
@app.route("/historial")
def hi():
 h=ld_h()
 b='<div class="sec-title title-historial">📜 HISTORIAL DE EXAMENES Y EVALUACIONES</div>'
 b+='<div style=margin:12px><a href=/cambiar class=btn-inicio>🏠 VOLVER AL PANEL</a></div>'
 if not h: b+='<div class=card>No hay exámenes registrados en el historial todavía.</div>'
 else:
  max_por = max([x["por"] for x in h]) if h else 0
  for idx, x in enumerate(reversed(h)):
   es_mejor = (x["por"] == max_por and idx == 0)
   estilo = 'border:2px solid #FFD700; background:linear-gradient(180deg,#2E2605,#1A1503);' if es_mejor else 'background:linear-gradient(180deg,#0F380F,#082008); border-left:6px solid #4CAF50;'
   etiqueta = '<span class=badge style=background:#FFD700;color:#000;margin-bottom:6px>🏆 MEJOR PUNTAJE</span><br>' if es_mejor else ''
   b+=f'<div class=card style="{estilo}">{etiqueta}<b style=color:#FFD700;font-size:13px>{x["titulo"]}</b><br><span style=color:#81C784>Calificación: <b>{x["por"]}%</b></span><br><small style=color:#aaa>{x["fecha"]}</small></div>'
 return base("HISTORIAL",b)

@app.route("/add",methods=["POST"])
def ad():
 mat=session.get("materia_actual")
 p=ld()
 p.append({"materia":mat,"p":request.form.get("p",""),"op":[request.form.get("o1",""),request.form.get("o2",""),request.form.get("o3",""),request.form.get("o4","")],"co":int(request.form.get("c",0))})
 sv(p)
 return redirect("/")

@app.route("/del/<int:i>")
def dl(i):
 d=ld()
 if 0<=i<len(d): d.pop(i); sv(d)
 return redirect("/")

@app.route("/edit/<int:i>",methods=["GET","POST"])
def ed(i):
 d=ld()
 if not (0<=i<len(d)): return redirect("/")
 if request.method=="POST":
  d[i]["p"]=request.form.get("p","")
  d[i]["op"]=[request.form.get("o1",""),request.form.get("o2",""),request.form.get("o3",""),request.form.get("o4","")]
  d[i]["co"]=int(request.form.get("c",0))
  sv(d); return redirect("/")
 q=d[i]
 return base("EDITAR PREGUNTA",f'<div class=card card-create style=margin:12px><b style=color:#FFD700>✏️ EDITAR PREGUNTA</b><form method=post><input class=input name=p value="{q["p"]}"><input class=input name=o1 value="{q["op"][0]}"><input class=input name=o2 value="{q["op"][1]}"><input class=input name=o3 value="{q["op"][2]}"><input class=input name=o4 value="{q["op"][3]}"><select class=input name=c><option value=0 {"selected" if q["co"]==0 else ""}>A correcta</option><option value=1 {"selected" if q["co"]==1 else ""}>B correcta</option><option value=2 {"selected" if q["co"]==2 else ""}>C correcta</option><option value=3 {"selected" if q["co"]==3 else ""}>D correcta</option></select><button class="btn btn-green">💾 GUARDAR CAMBIO</button></form><a href=/cambiar class=btn-back style=margin-top:10px;display:inline-block>VOLVER</a></div>')

def rex(preg,titulo):
 session["ex"]=preg; session["titulo"]=titulo
 b=f'<div class="sec-title title-examen">{titulo} - {len(preg)} PREGUNTAS ACTIVAS</div>'
 b+='<div style=margin:12px><a href=/cambiar class=btn-inicio>🏠 VOLVER AL PANEL</a></div>'
 b+=f'<form method=post action=/cal>'
 for i,q in enumerate(preg):
  b+=f'<div class=card card-hi><div style=display:flex;justify-content:space-between><span class=badge style=background:#FFD700;color:#000>{q["materia"]}</span><span style=color:#81C784>{i+1}/{len(preg)}</span></div><b style=display:block;margin:10px 0;color:#E8F5E9>{q["p"]}</b>'
  for j,op in enumerate(q["op"]):
   b+=f'<label class=opt><input type=radio name="r{i}" value="{j}" required> {op}</label>'
  b+='</div>'
 b+='<button class="btn btn-gold" style=margin:12px;width:94%;padding:15px;font-size:14px;font-weight:900>✅ CALIFICAR EXAMEN OFICIAL</button></form>'
 return base(titulo,b)

@app.route("/exam_materia",methods=["POST"])
def em():
 m=(request.form.get("m") or "").strip().upper()
 if not m: return redirect("/")
 pr=[p for p in ld() if p["materia"]==m]
 if not pr: return base(m,f'<div class=card>No hay preguntas registradas en {m} - <a href=/ class=btn-back>VOLVER</a></div>')
 random.shuffle(pr)
 return rex(pr,f"EXAMEN {m}")

@app.route("/exam_general",methods=["POST"])
def eg():
 pr=ld()
 if not pr: return base("GENERAL",'<div class=card>No hay preguntas disponibles.</div>')
 random.shuffle(pr)
 return rex(pr,"EXAMEN GENERAL")

@app.route("/cal",methods=["POST"])
def ca2():
 ex=session.get("ex",[]); ti=session.get("titulo","EXAMEN"); ok=0
 for i,q in enumerate(ex):
  v=request.form.get(f"r{i}")
  try: tu=int(v)
  except: tu=-1
  if tu==q["co"]: ok+=1
 po=int(ok/len(ex)*100) if ex else 0
 from datetime import datetime as dt
 fe=dt.now().strftime("%d/%m/%Y %H:%M")
 h=ld_h(); h.append({"fecha":fe,"titulo":ti,"por":po}); sv_h(h)
 return base(ti,f'<div class=card style=text-align:center;padding:30px><h1 style=font-size:48px;color:#FFD700;margin:0>{po}%</h1><p style=font-size:18px;color:#81C784>{ok} aciertos correctos de {len(ex)}</p><div style=margin-top:20px;display:flex;gap:10px;justify-content:center><a href=/cambiar class=btn-inicio>🏠 VOLVER AL PANEL</a><a href=/historial class=btn-back>📜 VER HISTORIAL</a></div></div>')

app.run(host="0.0.0.0",port=5002)
