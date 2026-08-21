import os,json,random,hashlib
from flask import Flask,request,redirect,session
from datetime import datetime as dt

app=Flask(__name__)
app.secret_key="siea_final_profesional_completo"
DB=os.path.expanduser("~/preg.json")
HU=os.path.expanduser("~/hist.json")
UU=os.path.expanduser("~/user.json")
MM=os.path.expanduser("~/materias.json")
ADMIN_DB=os.path.expanduser("~/admin.json")

def ld():
 try:
  if os.path.exists(DB):
   with open(DB) as f: return json.load(f)
 except: pass
 return []
def sv(d):
 with open(DB,"w") as f: json.dump(d,f)
def ld_h():
 try:
  if os.path.exists(HU):
   with open(HU) as f: return json.load(f)
 except: pass
 return []
def sv_h(d):
 with open(HU,"w") as f: json.dump(d,f)
def ld_u():
 try:
  if os.path.exists(UU):
   with open(UU) as f: return json.load(f)
 except: pass
 return {}
def sv_u(d):
 with open(UU,"w") as f: json.dump(d,f)
def ld_m():
 try:
  if os.path.exists(MM):
   with open(MM) as f: return json.load(f)
 except: pass
 return {}
def sv_m(d):
 with open(MM,"w") as f: json.dump(d,f)
def ld_admin():
 try:
  if os.path.exists(ADMIN_DB):
   with open(ADMIN_DB) as f: return json.load(f)
 except: pass
 return {}
def sv_admin(d):
 with open(ADMIN_DB,"w") as f: json.dump(d,f)

def hash_password(p):
 return hashlib.sha256(p.encode()).hexdigest()

def login_page():
 h=""
 h+='<meta name=viewport content="width=device-width,initial-scale=1">'
 h+='<link href="https://fonts.googleapis.com/css2?family=Montserrat:ital,wght@0,400;0,700;0,900;1,400;1,700&display=swap" rel="stylesheet">'
 h+='<style>'
 h+='body{margin:0;background:#050B05;color:#E0EFE0;font-family:Montserrat,system-ui;min-height:100vh;display:flex;flex-direction:column}'
 h+='.hero{background:radial-gradient(ellipse at 20% 20%, rgba(0,255,128,0.15), transparent 55%), linear-gradient(180deg,#0D1A0D 0%,#050905 100%);border-bottom:2px solid #00FF80;padding:22px 14px}'
 h+='.sigla{font-size:38px;font-weight:900;font-style:italic;letter-spacing:5px;color:#FFD700;text-shadow:0 3px 15px rgba(255,215,0,0.4)}'
 h+='.sub{font-size:10px;letter-spacing:3px;color:#8AB38A;font-weight:700;margin-top:4px}'
 h+='.purpose{background:rgba(0,0,0,0.6);border-left:4px solid #FFD700;padding:12px;margin-top:14px;border-radius:0 10px 10px 0}'
 h+='.purpose b{color:#FFD700;font-size:10px;letter-spacing:1.2px;display:block;margin-bottom:4px}'
 h+='.purpose p{font-size:11px;line-height:1.6;color:#D2DCD2;margin:6px 0 0 0;text-align:justify}'
 h+='.container{display:flex;flex:1;gap:20px;padding:20px;flex-wrap:wrap;justify-content:center}'
 h+='.card-login{width:100%;max-width:395px;background:rgba(13,26,13,0.95);border:1px solid rgba(0,255,128,0.3);border-radius:14px;padding:18px;box-shadow:0 20px 40px rgba(0,0,0,0.8)}'
 h+='.card-support{width:100%;max-width:395px;background:rgba(13,26,13,0.95);border:1px solid rgba(255,215,0,0.3);border-radius:14px;padding:18px;box-shadow:0 20px 40px rgba(0,0,0,0.8);text-align:center}'
 h+='.lbl{font-size:9px;letter-spacing:1.5px;color:#00FF80;font-weight:700;margin:12px 0 4px 2px}'
 h+='.inp{width:100%;padding:13px;background:#020502;border:1.5px solid #1A401A;border-radius:10px;color:#fff;box-sizing:border-box;font-size:13px}'
 h+='.btn{width:100%;padding:14px;border:0;border-radius:10px;font-weight:900;letter-spacing:2px;margin-top:16px;background:linear-gradient(180deg,#00FF80,#00B359);color:#050905;cursor:pointer}'
 h+='.btn-register{background:linear-gradient(180deg,#FF9800,#E65100);margin-top:10px}'
 h+='.btn-paypal{background:linear-gradient(180deg,#003087,#009cde);margin-top:10px;width:100%;padding:12px}'
 h+='.tab-buttons{display:flex;gap:10px;margin-bottom:10px}'
 h+='.tab-btn{flex:1;padding:10px;border:2px solid #00FF80;background:transparent;color:#00FF80;border-radius:8px;cursor:pointer;font-weight:700;font-size:12px}'
 h+='.tab-btn.active{background:#00FF80;color:#050905}'
 h+='.tab-content{display:none}'
 h+='.tab-content.active{display:block}'
 h+='.legal{font-size:7.5px;color:#8EA88E;line-height:1.5;text-align:justify;margin-top:18px;border-top:1px solid rgba(255,255,255,0.1);padding-top:12px}'
 h+='.legal b{color:#FFD700;font-size:7.5px}'
 h+='.support-info{margin:15px 0;padding:12px;background:rgba(0,255,128,0.1);border-left:4px solid #00FF80;border-radius:8px}'
 h+='.support-info b{color:#00FF80;display:block;margin-bottom:5px}'
 h+='.support-info p{margin:5px 0;font-size:11px;color:#D2DCD2}'
 h+='.support-tel{font-size:16px;font-weight:900;color:#FFD700;letter-spacing:2px;margin:10px 0}'
 h+='.foot{margin-top:auto;background:#020402;padding:12px;text-align:center;font-size:7px;color:#3A5A3A;border-top:1px solid #0D1A0D;letter-spacing:1px}'
 h+='.error-msg{background:#260A0A;border:1px solid #5A1A1A;color:#FF8A80;padding:10px;border-radius:8px;margin-bottom:10px;font-size:11px}'
 h+='.success-msg{background:#0A261A;border:1px solid #1A5A2A;color:#00FF80;padding:10px;border-radius:8px;margin-bottom:10px;font-size:11px}'
 h+='</style>'
 h+='<div class=hero>'
 h+='<div class=sigla>S.I.E.A.</div>'
 h+='<div class=sub>SISTEMA INTEGRAL DE EVALUACION PARA EL ASCENSO</div>'
 h+='<div class=purpose>'
 h+='<b>PROPOSITO Y FUNCION INSTITUCIONAL</b>'
 h+='<p>Plataforma de fortalecimiento academico e institucional disenada bajo estrictos estÃ¡ndares de calidad para optimizar la preparacion, evaluacion y profesionalizacion del personal en proceso de ascenso.</p>'
 h+='</div></div>'
 h+='<div class=container>'
 h+='<div class=card-login>'
 h+='<div style="text-align:center"><div style="font-weight:900;letter-spacing:2.5px;color:#00FF80;font-size:12px">ACCESO AUTORIZADO</div><div style="font-size:9px;color:#7EA97E;margin-top:3px;letter-spacing:1px">Ingrese sus credenciales</div></div>'
 h+='<div class=tab-buttons>'
 h+='<button type=button class="tab-btn active" onclick="document.querySelectorAll(\'.tab-content\').forEach(e=>e.classList.remove(\'active\')); document.getElementById(\'login-form\').classList.add(\'active\')">Ingresar</button>'
 h+='<button type=button class="tab-btn" onclick="document.querySelectorAll(\'.tab-content\').forEach(e=>e.classList.remove(\'active\')); document.getElementById(\'register-form\').classList.add(\'active\')">Registrarse</button>'
 h+='</div>'
 h+='<div id=login-form class="tab-content active">'
 h+='<form method=post action=/login>'
 h+='<div class=lbl>USUARIO / MATRICULA</div><input class=inp name=user placeholder="Ej. 123456" required>'
 h+='<div class=lbl>CONTRASENA</div><input class=inp type=password name=pass placeholder="********" required>'
 h+='<button class=btn>INGRESAR AL SISTEMA</button>'
 h+='</form>'
 h+='</div>'
 h+='<div id=register-form class="tab-content">'
 h+='<form method=post action=/register>'
 h+='<div class=lbl>CREAR USUARIO / MATRICULA</div><input class=inp name=new_user placeholder="Ej. 123456" required>'
 h+='<div class=lbl>NOMBRE COMPLETO</div><input class=inp name=full_name placeholder="Ej. Juan PÃ©rez" required>'
 h+='<div class=lbl>CORREO ELECTRONICO</div><input class=inp type=email name=email placeholder="tu@correo.com" required>'
 h+='<div class=lbl>CREAR CONTRASEÃ‘A</div><input class=inp type=password name=new_pass placeholder="Min 6 caracteres" required minlength=6>'
 h+='<div class=lbl>CONFIRMAR CONTRASEÃ‘A</div><input class=inp type=password name=confirm_pass placeholder="Repetir contraseÃ±a" required minlength=6>'
 h+='<button class=btn>âœ… CREAR CUENTA</button>'
 h+='</form>'
 h+='</div>'
 h+='<div class=legal>'
 h+='<b>AVISO DE CONFIDENCIALIDAD Y MARCO LEGAL:</b> La informacion contenida, procesada y generada en esta plataforma es de caracter estrictamente confidencial, reservado y de uso exclusivo para personal autorizado.'
 h+='</div></div>'
 h+='<div class=card-support>'
 h+='<div style="font-weight:900;letter-spacing:2.5px;color:#FFD700;font-size:12px">SOPORTE Y SUSCRIPCION</div>'
 h+='<div class=support-info>'
 h+='<b>ðŸ“ž SOPORTE TECNICO DIRECTO</b>'
 h+='<p>Para dudas, reportes o asistencia inmediata:</p>'
 h+='<div class=support-tel>+52 811 0290152</div>'
 h+='<p style="font-size:10px;color:#FFD700;margin-top:10px">Disponible de Lunes a Viernes<br>08:00 - 18:00 hrs</p>'
 h+='</div>'
 h+='<div class=support-info>'
 h+='<b>ðŸ’³ SUSCRIPCION PREMIUM</b>'
 h+='<p>Acceso ilimitado a todas las materias, reactivos y evaluaciones sin restricciones.</p>'
 h+='<form action="https://www.paypal.com/cgi-bin/webscr" method="post" target="_blank">'
 h+='<input type="hidden" name="cmd" value="_xclick">'
 h+='<input type="hidden" name="business" value="tu_email_paypal@example.com">'
 h+='<input type="hidden" name="item_name" value="SuscripciÃ³n S.I.E.A. Premium">'
 h+='<input type="hidden" name="amount" value="9.99">'
 h+='<input type="hidden" name="currency_code" value="USD">'
 h+='<input type="hidden" name="return" value="http://localhost:5002/payment_success">'
 h+='<input type="hidden" name="cancel_return" value="http://localhost:5002/">'
 h+='<button type="submit" class="btn btn-paypal">ðŸ”’ PAGAR SUSCRIPCION - $9.99 USD</button>'
 h+='</form>'
 h+='</div>'
 h+='</div>'
 h+='</div>'
 h+='<div class=foot>PLATAFORMA DE USO INTERNO Y CONTROL INSTITUCIONAL | S.I.E.A. 2026</div>'
 return h

def base(t,b):
 u=session.get("user","")
 frases=["( La disciplina es la clave del Ã©xito operativo )", "( La constancia vence lo que la dicha no alcanza )", "( El conocimiento es poder y preparaciÃ³n )", "( Cada pregunta respondida es un paso hacia el Ã©xito )"]
 f_activa = random.choice(frases)
 h=""
 h+='<meta name=viewport content="width=device-width,initial-scale=1">'
 h+='<link href="https://fonts.googleapis.com/css2?family=Montserrat:ital,wght@0,400;0,700;0,900;1,400;1,700&display=swap" rel="stylesheet">'
 h+='<style>'
 h+='body{margin:0;background:#050B05;color:#E0EFE0;font-family:Montserrat,system-ui}'
 h+='.top{background:linear-gradient(90deg,#00FF80,#00B359);color:#050905;padding:10px;text-align:center;font-weight:900;font-style:italic;font-size:14px;letter-spacing:1.5px}'
 h+='.bar{background:#0D1A0D;padding:10px 12px;display:flex;justify-content:space-between;align-items:center;border-bottom:2px solid #00FF80}'
 h+='.user-info{font-size:12px;color:#00FF80;font-weight:700}'
 h+='.sub-bar{font-size:9px;color:#A0C8A0;font-style:italic;margin-top:2px}'
 h+='.btn-back{background:#1A331A;color:#fff;padding:7px 12px;border-radius:7px;text-decoration:none;font-size:11px;border:1px solid #2E5A2E;display:inline-block}'
 h+='.btn-inicio{background:linear-gradient(180deg,#00FF80,#00B359);color:#050905;padding:10px 18px;border-radius:8px;text-decoration:none;font-size:12px;font-weight:900;letter-spacing:1px;display:inline-block}'
 h+='.sec-title{color:#050905;padding:11px;text-align:center;font-weight:900;border-radius:9px;margin:12px;font-size:12px;letter-spacing:0.5px}'
 h+='.title-materias{background:linear-gradient(90deg,#FFD700,#FFA500)}'
 h+='.title-trabajando{background:linear-gradient(90deg,#00E5FF,#00839F)}'
 h+='.title-general{background:linear-gradient(90deg,#FFD700,#FFA500)}'
 h+='.card{border-radius:12px;padding:14px;margin:10px 12px;box-shadow:0 4px 12px rgba(0,0,0,0.6)}'
 h+='.card-hi{background:linear-gradient(180deg,#0F260F,#081708);border-left:6px solid #00FF80;border-top:1px solid #1A401A}'
 h+='.card-mom{background:linear-gradient(180deg,#0A1F33,#06121F);border-left:6px solid #00E5FF;border-top:1px solid #10314D}'
 h+='.card-ley{background:linear-gradient(180deg,#33260A,#1F1706);border-left:6px solid #FFD700;border-top:1px solid #59420A}'
 h+='.card-new{background:linear-gradient(180deg,#1A1A1A,#0D0D0D);border-left:6px solid #C5A059}'
 h+='.card-gen{background:linear-gradient(180deg,#1A1605,#0D0B02);border:2px solid #FFD700}'
 h+='.card-gen-vacio{background:#141414;border:2px solid #2A2A2A;opacity:0.6}'
 h+='.card-per{background:linear-gradient(180deg,#140F26,#0A0817);border:2px dashed #9C27B0}'
 h+='.card-create{background:linear-gradient(180deg,#2A1B0A,#140D05);border:2px solid #FF9800}'
 h+='.card-preg{background:#0D170D;border:1px solid #1A3A1A;border-left:4px solid #00FF80}'
 h+='.btn{width:100%;padding:12px;border:0;border-radius:8px;font-weight:800;margin-top:8px;cursor:pointer;font-size:12px}'
 h+='.btn-hi{background:linear-gradient(180deg,#00FF80,#00B359);color:#050905}'
 h+='.btn-mom{background:linear-gradient(180deg,#00E5FF,#0099B8);color:#050905}'
 h+='.btn-ley{background:linear-gradient(180deg,#FFD700,#CCAC00);color:#050905}'
 h+='.btn-gold{background:linear-gradient(180deg,#FFD700,#CCAC00);color:#050905}'
 h+='.btn-orange{background:linear-gradient(180deg,#FF9800,#E65100);color:#fff}'
 h+='.btn-green{background:linear-gradient(180deg,#00FF80,#00B359);color:#050905}'
 h+='.btn-purple{background:linear-gradient(180deg,#CE93D8,#AB47BC);color:#050905}'
 h+='.btn-edit{background:#FFD700;color:#050905;padding:8px 14px;border-radius:6px;text-decoration:none;font-size:11px;font-weight:800;display:inline-block}'
 h+='.btn-del{background:#4D1A1A;color:#ff9999;padding:8px 14px;border-radius:6px;text-decoration:none;font-size:11px;display:inline-block;margin-left:6px}'
 h+='.input{width:100%;padding:11px;background:#050B05;border:1px solid #FF9800;border-radius:8px;color:#fff;margin:5px 0;box-sizing:border-box}'
 h+='.opt{display:block;background:#050B05;border:1px solid #1A401A;padding:10px;margin:6px 0;border-radius:8px}'
 h+='.badge{padding:3px 10px;border-radius:12px;font-size:10px;font-weight:800;display:inline-block}'
 h+='</style>'
 h+=f'<div class=top>S.I.E.A. - {t}</div>'
 h+=f'<div class=bar><div><div class=user-info>Bienvenido, {u}</div><div class=sub-bar>{f_activa}</div></div><div><a href=/admin class=btn-back>ADMIN</a> <a href=/historial class=btn-back>HISTORIAL</a> <a href=/logout class=btn-back>SALIR</a></div></div>'
 return h + b

@app.route("/")
def ix():
 if "user" not in session:
  return login_page()
 u=session.get("user")
 ma=session.get("materia_actual")
 materias_db=ld_m()
 materias_usuario=materias_db.get(u,[])
 total_preg=len([p for p in ld() if p.get("usuario")==u])
 if not ma:
  ms={}
  for p in ld():
   if p.get("usuario")==u:
    ms[p["materia"]]=ms.get(p["materia"],0)+1
  h='<div class="sec-title title-materias">ðŸ“š PANEL PRINCIPAL DE MATERIAS Y GESTION</div>'
  h+='<div class=card card-create style="border-left:6px solid #FF9800"><b>âž• CREAR NUEVA MATERIA PERSONALIZADA</b><p style="font-size:11px;color:#FFE0B2;margin:6px 0">Asigne una nomenclatura oficial o personalizada para organizar sus reactivos</p><form method=post action=/add_materia><input class=input name=nueva_materia placeholder="ETICA, ADMINISTRATIVO, etc." required><button class="btn btn-orange">Crear Materia</button></form></div>'
  colores=[("card-hi","btn-hi","#00FF80"),("card-mom","btn-mom","#00E5FF"),("card-ley","btn-ley","#FFD700"),("card-new","btn-gold","#C5A059")]
  for idx,m in enumerate(materias_usuario):
   c=ms.get(m,0)
   card_c,btn_c,col=colores[idx % len(colores)]
   h+=f'<div class=card {card_c}><div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px"><span style="font-weight:900;font-size:13px">ðŸ“˜ {m}</span><span class=badge style="background:{col};color:#050905">{c} reactivos</span></div>'
   h+=f'<form method=post action=/set_materia><input type=hidden name=materia value="{m}"><button class="btn {btn_c}">ðŸ“‚ ACCEDER A {m} - GESTIÃ“N Y REACTIVOS</button></form>'
   h+=f'<div style="margin-top:10px;display:flex;gap:6px"><a href=/edit_materia/{idx} class=btn-edit style="flex:1;text-align:center">âœï¸ EDITAR MATERIA</a><a href=/del_materia/{idx} class=btn-del>ðŸ—‘ï¸ ELIMINAR</a></div></div>'
  if total_preg>0:
   h+=f'<div class=card card-gen><div style="display:flex;justify-content:space-between;align-items:center"><b>â­ EXAMEN GENERAL</b><span class=badge style="background:#FFD700;color:#050905">{total_preg} reactivos totales</span></div><p style="font-size:11px;color:#FFE0B2;margin:6px 0">EvaluaciÃ³n con todas las preguntas acumuladas</p><form method=post action=/exam_general><button class="btn btn-gold">ðŸ“ REALIZAR EXAMEN GENERAL</button></form></div>'
  else:
   h+=f'<div class=card card-gen-vacio><b>â­ EXAMEN GENERAL (SIN REACTIVOS)</b><p style="font-size:11px;color:#777;margin:6px 0">Agregue preguntas en las materias para habilitar</p><button class="btn btn-gold" disabled>ðŸ“ REALIZAR EXAMEN GENERAL</button></div>'
  h+='<div class=card card-per><b>ðŸŽ¯ EXAMEN PERSONALIZADO</b><p style="font-size:11px;color:#CE93D8;margin:6px 0">Seleccione y combine las materias de su preferencia para prÃ¡ctica focalizada</p><form method=post action=/exam_personalizado>'
  for m in materias_usuario:
   c=ms.get(m,0)
   h+=f'<label style="display:block;background:#0A0817;padding:9px;margin:5px 0;border-radius:7px;font-size:12px;border:1px solid #2A1F40"><input type=checkbox name=mats value="{m}" style="margin-right:8px">{m} ({c})</label>'
  h+='<button class="btn btn-purple" style="margin-top:10px">âœ¨ GENERAR EXAMEN COMBINADO</button></form></div>'
  return base("INICIO",h)

 pr=[p for p in ld() if p["materia"]==ma and p.get("usuario")==u]
 allp=[p for p in ld() if p.get("usuario")==u]
 b='<div style="margin:12px;display:flex;gap:8px"><a href=/cambiar class=btn-inicio>ðŸ  INICIO - PANEL GENERAL</a></div>'
 b+=f'<div class="sec-title title-trabajando">ðŸ“‚ BANCO DE TRABAJO: {ma} ({len(pr)} REACTIVOS)</div>'
 b+=f'<div class=card card-create style="border-left:6px solid #00FF80"><b>âž• NUEVA PREGUNTA PARA {ma}</b><form method=post action=/add><input class=input name=p placeholder="Escriba el enunciado de la pregunta" required><div style="display:flex;gap:8px;margin:10px 0"><input class=input placeholder="OpciÃ³n A" name=o1 required><input class=input placeholder="OpciÃ³n B" name=o2 required></div><div style="display:flex;gap:8px;margin:10px 0"><input class=input placeholder="OpciÃ³n C" name=o3 required><input class=input placeholder="OpciÃ³n D" name=o4 required></div><select class=input name=c required><option>Seleccione respuesta correcta</option><option value=0>A</option><option value=1>B</option><option value=2>C</option><option value=3>D</option></select><button class="btn btn-green">âœ… GUARDAR REACTIVO</button></form></div>'
 if len(pr)==0:
  b+=f'<div class=card style="background:#2A1111;border:1px solid #5A1A1A"><b style="color:#FF8A80">âš ï¸ Sin reactivos en {ma}</b><p style="font-size:11px;color:#BCAAA4">Utilice el formulario superior para agregar preguntas</p></div>'
 for p in allp:
  if p["materia"]!=ma: continue
  idx = allp.index(p)
  letras=["A","B","C","D"]
  correcta=letras[p["co"]]
  b+=f'<div class=card card-preg><div style="display:flex;justify-content:space-between"><span class=badge style="background:#00FF80;color:#050905">{p["materia"]}</span><span class=badge style="background:#00E5FF;color:#050905">Respuesta correcta: {correcta}</span></div><p style="margin:10px 0;font-size:13px"><b>{p["p"]}</b></p><div style="font-size:11px;margin:8px 0"><b>A)</b> {p["op"][0]} | <b>B)</b> {p["op"][1]} | <b>C)</b> {p["op"][2]} | <b>D)</b> {p["op"][3]}</div><a href=/edit/{idx} class=btn-edit>âœï¸ EDITAR</a><a href=/del/{idx} class=btn-del>ðŸ—‘ï¸ ELIMINAR</a></div>'
 return base(ma,b)

@app.route("/login",methods=["POST"])
def lg():
 u=request.form.get("user","").strip().upper()
 p=request.form.get("pass","").strip()
 us=ld_u()
 
 if u not in us:
  return login_page() + '<div style="margin:20px auto;width:90%;max-width:400px" class=error-msg>âŒ Usuario no encontrado. Cree una cuenta primero.</div>'
 
 if us[u]["password_hash"] != hash_password(p):
  return login_page() + '<div style="margin:20px auto;width:90%;max-width:400px" class=error-msg>âŒ ContraseÃ±a incorrecta.</div>'
 
 usuario = us[u]
 if usuario.get("status") != "aprobado":
  return login_page() + '<div style="margin:20px auto;width:90%;max-width:400px" class=error-msg>â³ Tu cuenta estÃ¡ pendiente de aprobaciÃ³n por el administrador. Contacta al soporte: +52 811 0290152</div>'
 
 session["user"] = u
 session["role"] = usuario.get("role", "user")
 session["u"] = usuario.get("email", "")
 return redirect("/")

@app.route("/register", methods=["GET","POST"])
def reg():
    if request.method=="POST":
        u=request.form.get("user","").strip().upper()
        p=request.form.get("pass","").strip()
        e=request.form.get("email","").strip()
        if not u or not p:
            return login_page() + '<div style="margin:20px auto;width:90%;max-width:400px" class="error-msg">Faltan datos</div>'
        adm=ld_admin()
        if u in adm:
            return login_page() + '<div style="margin:20px auto;width:90%;max-width:400px" class="error-msg">Usuario ya existe</div>'
        adm[u]={"password_hash":hash_password(p),"status":"pendiente","role":"user","email":e}
        sv_admin(adm)
        return login_page() + '<div style="margin:20px auto;width:90%;max-width:400px" style="background:#1A3111;border:1px solid #5A1A1A"><b>Registro enviado. Espera aprobación.</b></div>'
    return login_page()

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/")
def home():
    if "user" not in session:
        return redirect("/login")
    return ixt()

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)


           
