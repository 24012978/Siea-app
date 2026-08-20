import os, json, random
from flask import Flask, request, redirect, session
app = Flask(__name__)
app.secret_key = "siea_final_profesional_completo"

# Rutas base generales para credenciales de usuarios
UU = os.path.expanduser("~/user.json")

def ld_u():
 try:
  if os.path.exists(UU):
   with open(UU) as f: return json.load(f)
 except: pass
 return {}
def sv_u(d):
 with open(UU,"w") as f: json.dump(d,f)

# Funciones de datos aisladas por usuario actual
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

def login_page():
 h=""
 h+='<meta name=viewport content="width=device-width,initial-scale=1">'
 h+='<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700;900&display=swap" rel="stylesheet">'
 h+='<style>'
 h+='body{margin:0;background:#060D06;color:#fff;font-family:Montserrat,system-ui;min-height:100vh;display:flex;flex-direction:column}'
 h+='.hero{background:radial-gradient(ellipse at 20% 20%, rgba(197,160,89,0.25), transparent 55%), linear-gradient(180deg,#142913 0%,#080E08 100%);border-bottom:2px solid #C5A059;padding:22px 14px}'
 h+='.sigla{font-size:32px;font-weight:900;letter-spacing:4px;color:#C5A059;text-shadow:0 2px 8px rgba(0,0,0,0.8)}'
 h+='.sub{font-size:10px;letter-spacing:3px;color:#8AB38A;font-weight:700;margin-top:4px}'
 h+='.purpose{background:rgba(0,0,0,0.45);border-left:3px solid #C5A059;padding:12px 12px;margin-top:14px;border-radius:0 10px 10px 0}'
 h+='.purpose b{color:#C5A059;font-size:10px;letter-spacing:1.2px;display:block;margin-bottom:4px}'
 h+='.purpose p{font-size:11px;line-height:1.55;color:#D2DDD2;margin:6px 0 0 0;text-align:justify}'
 h+='.card-login{margin:18px auto;width:90%;max-width:395px;background:rgba(28,43,26,0.96);border:1px solid rgba(197,160,89,0.4);border-radius:14px;padding:18px;box-shadow:0 20px 40px rgba(0,0,0,0.7)}'
 h+='.lbl{font-size:9px;letter-spacing:1.5px;color:#C5A059;font-weight:700;margin:12px 0 4px 2px}'
 h+='.inp{width:100%;padding:13px;background:#0A140A;border:1.5px solid #2A4A2A;border-radius:10px;color:#fff;box-sizing:border-box;font-size:13px}'
 h+='.btn{width:100%;padding:14px;border:0;border-radius:10px;font-weight:900;letter-spacing:2px;margin-top:16px;background:linear-gradient(180deg,#D8B86E,#C5A059);color:#111;cursor:pointer}'
 h+='.legal{font-size:7.5px;color:#7A8E7A;line-height:1.45;text-align:justify;margin-top:18px;border-top:1px solid rgba(255,255,255,0.12);padding-top:12px}'
 h+='.legal b{color:#8AA88A;font-size:7.5px}'
 h+='.foot{margin-top:auto;background:#040804;padding:12px;text-align:center;font-size:7px;color:#4A5A4A;border-top:1px solid #1A2A1A;letter-spacing:1px}'
 h+='</style>'
 h+='<div class=hero>'
 h+='<div class=sigla>S.I.E.A.</div>'
 h+='<div class=sub>SISTEMA INTEGRAL DE EVALUACION PARA EL ASCENSO</div>'
 h+='<div class=purpose>'
 h+='<b>PROPOSITO Y FUNCION INSTITUCIONAL</b>'
 h+='<p>Plataforma de fortalecimiento academico disenada para optimizar la preparacion del personal en proceso de ascenso. Centraliza bancos de reactivos por materia, genera evaluaciones aleatorizadas y otorga metricas de desempeno para la mejora continua.</p>'
 h+='<p>Herramienta de apoyo complementario al estudio doctrinal y normativo vigente, orientada a elevar el nivel de conocimientos mediante practica continua, retroalimentacion inmediata y creacion de materias personalizadas por el propio usuario.</p>'
 h+='</div></div>'
 h+='<div class=card-login>'
 h+='<div style=text-align:center><div style=font-weight:900;letter-spacing:2.5px;color:#C5A059;font-size:12px>ACCESO AUTORIZADO</div><div style=font-size:9px;color:#7E9A7E;margin-top:3px;letter-spacing:1px>PERSONAL EN PREPARACION</div></div>'
 h+='<form method=post action=/login>'
 h+='<div class=lbl>USUARIO / MATRICULA</div><input class=inp name=user placeholder="Ej. 123456" required>'
 h+='<div class=lbl>CONTRASENA</div><input class=inp type=password name=pass placeholder="********" required>'
 h+='<button class=btn>INGRESAR AL SISTEMA</button>'
 h+='</form>'
 h+='<div class=legal>'
 h+='<b>AVISO DE CONFIDENCIALIDAD, USO Y LIMITACION DE RESPONSABILIDAD:</b> Este sistema es de uso exclusivo para fines de preparacion academica y no constituye material oficial de evaluacion. La informacion, reactivos, materias creadas por el usuario y resultados son de caracter privado y orientativo. Queda prohibida su distribucion, reproduccion o comercializacion. No se recopilan datos personales sensibles ni se comparte informacion con terceros. Al ingresar, el usuario acepta que los resultados no garantizan el resultado en evaluaciones oficiales, que las materias personalizadas son responsabilidad del creador y se compromete al uso etico y responsable de la plataforma. <b>S.I.E.A. v5.0 2026.</b> Plataforma de uso interno, no oficial, fines educativos y de fortalecimiento academico.'
 h+='</div></div>'
 h+='<div class=foot>PLATAFORMA DE USO INTERNO | NO OFICIAL | FINES EDUCATIVOS | S.I.E.A. SISTEMA INTEGRAL DE EVALUACION PARA EL ASCENSO 2026</div>'
 return h

def base(t,b):
 u=session.get("user","")
 h=""
 h+='<meta name=viewport content="width=device-width,initial-scale=1"><style>'
 h+='body{margin:0;background:#0A150A;color:#fff;font-family:system-ui}'
 h+='.top{background:#C5A059;color:#000;padding:9px;text-align:center;font-weight:900;font-size:12px;letter-spacing:1px}'
 h+='.bar{background:#101F10;padding:10px 12px;display:flex;justify-content:space-between;align-items:center;border-bottom:2px solid #C5A059}'
 h+='.btn-back{background:#2A3A2A;color:#fff;padding:7px 12px;border-radius:7px;text-decoration:none;font-size:11px;border:1px solid #3A4A3A;display:inline-block}'
 h+='.btn-inicio{background:linear-gradient(180deg,#D8B86E,#C5A059);color:#000;padding:10px 18px;border-radius:8px;text-decoration:none;font-size:12px;font-weight:900;letter-spacing:1px;display:inline-block;box-shadow:0 2px 8px rgba(197,160,89,0.4)}'
 h+='.sec-title{color:#000;padding:11px;text-align:center;font-weight:900;border-radius:9px;margin:12px;font-size:12px;letter-spacing:0.5px}'
 h+='.title-materias{background:linear-gradient(90deg,#4CAF50,#81C784)}'
 h+='.title-trabajando{background:linear-gradient(90deg,#C5A059,#D8B86E)}'
 h+='.title-general{background:linear-gradient(90deg,#FFA000,#FFC107)}'
 h+='.title-general-vacio{background:linear-gradient(90deg,#3A3A3A,#5A5A5A);color:#888}'
 h+='.card{border-radius:12px;padding:14px;margin:10px 12px;box-shadow:0 4px 12px rgba(0,0,0,0.4)}'
 h+='.card-hi{background:linear-gradient(180deg,#1E3A1E,#152B15);border-left:6px solid #4CAF50;border-top:1px solid #2E5A2E}'
 h+='.card-mom{background:linear-gradient(180deg,#162A45,#111F33);border-left:6px solid #2196F3;border-top:1px solid #2A4A6A}'
 h+='.card-ley{background:linear-gradient(180deg,#3A2222,#2A1818);border-left:6px solid #FFC107;border-top:1px solid #5A3A1A}'
 h+='.card-new{background:linear-gradient(180deg,#2A2A2A,#1A1A1A);border-left:6px solid #C5A059}'
 h+='.card-gen{background:linear-gradient(180deg,#1C1C0A,#151505);border:2px solid #C5A059}'
 h+='.card-gen-vacio{background:#1A1A1A;border:2px solid #3A3A3A;opacity:0.6}'
 h+='.card-per{background:linear-gradient(180deg,#1A1428,#141020);border:2px dashed #8E7CC3}'
 h+='.card-create{background:linear-gradient(180deg,#0F2A0F,#0A1F0A);border:2px dashed #4CAF50}'
 h+='.card-preg{background:#111F11;border:1px solid #2A4A2A;border-left:4px solid #4CAF50}'
 h+='.btn{width:100%;padding:12px;border:0;border-radius:8px;font-weight:800;margin-top:8px;cursor:pointer;font-size:12px}'
 h+='.btn-hi{background:linear-gradient(180deg,#4CAF50,#2E7D32);color:#fff}'
 h+='.btn-mom{background:linear-gradient(180deg,#42A5F5,#1E88E5);color:#fff}'
 h+='.btn-ley{background:linear-gradient(180deg,#FFCA28,#FFA000);color:#000}'
 h+='.btn-gold{background:linear-gradient(180deg,#D8B86E,#C5A059);color:#111}'
 h+='.btn-green{background:linear-gradient(180deg,#66BB6A,#2E7D32);color:#fff}'
 h+='.btn-purple{background:linear-gradient(180deg,#B39DDB,#7E57C2);color:#fff}'
 h+='.btn-edit{background:#C5A059;color:#000;padding:8px 14px;border-radius:6px;text-decoration:none;font-size:11px;font-weight:800;display:inline-block}'
 h+='.btn-del{background:#5A1A1A;color:#fff;padding:8px 14px;border-radius:6px;text-decoration:none;font-size:11px;display:inline-block;margin-left:6px}'
 h+='.input{width:100%;padding:11px;background:#10180F;border:1px solid #C5A059;border-radius:8px;color:#fff;margin:5px 0;box-sizing:border-box}'
 h+='.opt{display:block;background:#10180F;border:1px solid #3A5A33;padding:10px;margin:6px 0;border-radius:8px}'
 h+='.badge{padding:3px 10px;border-radius:12px;font-size:10px;font-weight:800;display:inline-block}'
 h+='</style>'
 h+=f'<div class=top>S.I.E.A. - {t}</div><div class=bar><b>{u}</b><div><a href=/historial class=btn-back>HISTORIAL</a> <a href=/logout class=btn-back>SALIR</a></div></div>'
 return h + b

@app.route("/")
def ix():
 if "user" not in session:
  return login_page()
 ma=session.get("materia_actual")
 materias=ld_m()
 total_preg=len(ld())
 if not ma:
  ms={}
  for p in ld():
   ms[p["materia"]]=ms.get(p["materia"],0)+1
  h='<div class="sec-title title-materias">📚 TUS MATERIAS - GESTIONA Y CREA</div>'
  h+='<div class=card card-create><b>➕ CREAR NUEVA MATERIA PERSONALIZADA</b><p style=font-size:11px;color:#81C784;margin:6px 0>Escribe el nombre y crea tu materia, adentro podras crear preguntas</p><form method=post action=/add_materia><input class=input name=nueva_materia placeholder="Ej: DERECHOS HUMANOS, ARMAMENTO, LEGISLACION..." required><button class="btn btn-green">✅ CREAR MATERIA NUEVA</button></form></div>'
  colores=[("card-hi","btn-hi","#4CAF50"),("card-mom","btn-mom","#2196F3"),("card-ley","btn-ley","#FFC107"),("card-new","btn-gold","#C5A059")]
  for idx,m in enumerate(materias):
   c=ms.get(m,0)
   card_c,btn_c,col=colores[idx % len(colores)]
   h+=f'<div class=card {card_c}><div style=display:flex;justify-content:space-between;align-items:center;margin-bottom:8px><span style=font-weight:900;font-size:13px>📘 {m}</span><span class=badge style=background:{col};color:#000>{c} PREGUNTAS</span></div>'
   h+=f'<form method=post action=/set_materia><input type=hidden name=materia value="{m}"><button class="btn {btn_c}">➕ ENTRAR A {m} - CREAR / EDITAR PREGUNTAS ADENTRO</button></form>'
   h+=f'<div style=margin-top:10px;display:flex;gap:6px><a href=/edit_materia/{idx} class=btn-edit style=flex:1;text-align:center>✏️ EDITAR MATERIA</a><a href=/del_materia/{idx} class=btn-del style=flex:1;text-align:center>🗑️ BORRAR</a></div>'
   h+=f'<div style=margin-top:8px><form method=post action=/exam_materia><input type=hidden name=m value="{m}"><button class="btn" style=background:#0F2510;color:#81C784;border:1px solid #4CAF50;padding:9px;font-size:11px>📝 HACER EXAMEN SOLO DE {m} ({c} preg)</button></form></div></div>'
  if total_preg>0:
   h+=f'<div class=card card-gen><div style=display:flex;justify-content:space-between;align-items:center><b>⭐ EXAMEN GENERAL</b><span class=badge style=background:#C5A059;color:#000>{total_preg} PREG TOTAL</span></div><p style=font-size:11px;color:#C5A059;margin:6px 0>Examen con todas tus materias juntas - cambia a dorado cuando tienes preguntas</p><form method=post action=/exam_general><button class="btn btn-gold">🚀 INICIAR EXAMEN GENERAL - {total_preg} PREGUNTAS</button></form></div>'
  else:
   h+=f'<div class=card card-gen-vacio><b>⭐ EXAMEN GENERAL (VACIO)</b><p style=font-size:11px;color:#777;margin:6px 0>Agrega preguntas para activar - esta en gris porque no tienes preguntas aun</p><button class="btn" style=background:#3A3A3A;color:#777 disabled>🚀 SIN PREGUNTAS - AGREGA PRIMERO</button></div>'
  h+='<div class=card card-per><b>🎯 EXAMEN PERSONALIZADO</b><p style=font-size:11px;color:#B39DDB;margin:6px 0>Elige que materias combinar</p><form method=post action=/exam_personalizado>'
  for m in materias:
   c=ms.get(m,0)
   h+=f'<label style=display:block;background:#1E1830;padding:9px;margin:5px 0;border-radius:7px;font-size:12px><input type=checkbox name=mats value="{m}" style=margin-right:8px> {m} ({c} preg)</label>'
  h+='<button class="btn btn-purple" style=margin-top:10px>✨ CREAR EXAMEN PERSONALIZADO</button></form></div>'
  return base("INICIO",h)

 pr=[p for p in ld() if p["materia"]==ma]
 allp=ld()
 b='<div style=margin:12px;display:flex;gap:8px><a href=/cambiar class=btn-inicio>🏠 INICIO - VOLVER A TODAS LAS MATERIAS</a></div>'
 b+=f'<div class="sec-title title-trabajando">📂 TRABAJANDO EN: {ma} - {len(pr)} PREGUNTAS ADENTRO</div>'
 b+=f'<div class=card card-create><b>➕ CREAR NUEVA PREGUNTA ADENTRO DE {ma}</b><form method=post action=/add><input class=input name=p placeholder="Escribe la pregunta completa aqui" required><input class=input name=o1 placeholder="Opcion A) (Correcta)" required><input class=input name=o2 placeholder="Opcion B)" required><input class=input name=o3 placeholder="Opcion C)" required><input class=input name=o4 placeholder="Opcion D)" required><select class=input name=c><option value=0>A es la correcta</option><option value=1>B es la correcta</option><option value=2>C es la correcta</option><option value=3>D es la correcta</option></select><button class="btn btn-green">💾 GUARDAR PREGUNTA EN {ma}</button></form></div>'
 b+=f'<div class=card card-gen><form method=post action=/exam_materia><input type=hidden name=m value="{ma}"><button class="btn btn-gold">📝 HACER EXAMEN DE {ma} - {len(pr)} PREGUNTAS</button></form></div>'
 if len(pr)==0:
  b+=f'<div class=card style=background:#2A1818;border:1px solid #5A1A1A><b style=color:#FF8A80>⚠️ Aun no tienes preguntas en {ma}</b><p style=font-size:11px;color:#BCAAA4>Usa el formulario de arriba para crear tu primera pregunta adentro de esta materia</p></div>'
 for p in allp:
  if p["materia"]!=ma: continue
  idx = allp.index(p)
  letras=["A","B","C","D"]
  correcta=letras[p["co"]]
  b+=f'<div class=card card-preg><div style=display:flex;justify-content:space-between><span class=badge style=background:#C5A059;color:#000>{p["materia"]}</span><span class=badge style=background:#4CAF50;color:#fff>Correcta: {correcta}</span></div><b style=display:block;margin:10px 0;font-size:13px>{p["p"]}</b><div style=font-size:11px;line-height:1.6;opacity:0.9>A) {p["op"][0]}<br>B) {p["op"][1]}<br>C) {p["op"][2]}<br>D) {p["op"][3]}</div><div style=margin-top:12px><a href=/edit/{idx} class=btn-edit>✏️ EDITAR PREGUNTA Y GUARDAR</a><a href=/del/{idx} class=btn-del>🗑️ BORRAR PREGUNTA</a></div></div>'
 return base(ma,b)

@app.route("/add_materia",methods=["POST"])
def add_mat():
 nueva=request.form.get("nueva_materia","").strip().upper()
 mats=ld_m()
 if nueva and nueva not in mats:
  mats.append(nueva)
  sv_m(mats)
 return redirect("/")

@app.route("/edit_materia/<int:i>",methods=["GET","POST"])
def edit_mat(i):
 mats=ld_m()
 if not (0<=i<len(mats)):
  return redirect("/")
 if request.method=="POST":
  nuevo=request.form.get("nuevo_nombre","").strip().upper()
  if nuevo:
   viejo=mats[i]
   preg=ld()
   for p in preg:
    if p["materia"]==viejo:
     p["materia"]=nuevo
   sv(preg)
   mats[i]=nuevo
   sv_m(mats)
  return redirect("/")
 viejo=mats[i]
 return base("EDITAR MATERIA",f'<div class=card card-create style=margin:12px><b>✏️ EDITAR MATERIA: {viejo}</b><form method=post><input class=input name=nuevo_nombre value="{viejo}" required><button class="btn btn-green">💾 GUARDAR CAMBIO DE NOMBRE</button></form><a href=/ class=btn-back style=margin-top:10px;display:inline-block>VOLVER</a></div>')

@app.route("/del_materia/<int:i>")
def del_mat(i):
 mats=ld_m()
 if 0<=i<len(mats):
  bor=mats[i]
  preg=[x for x in ld() if x["materia"]!=bor]
  sv(preg)
  mats.pop(i)
  sv_m(mats)
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

@app.route("/login",methods=["POST"])
def lg():
 u=request.form.get("user","").strip().upper()
 p=request.form.get("pass","").strip()
 us=ld_u()
 if u in us and us[u]!=p:
  return "Clave mal <a href=/>Volver</a>"
 if u not in us:
  us[u]=p
  sv_u(us)
 session["user"]=u
 return redirect("/")

@app.route("/logout")
def lo():
 session.clear()
 return redirect("/")

@app.route("/historial")
def hi():
 h=ld_h()
 b='<div class=card><b>HISTORIAL DE EXAMENES</b> <a href=/cambiar class=btn-inicio style=margin-left:10px>INICIO</a></div>'
 for x in reversed(h):
  b+=f'<div class=card card-hi>{x["titulo"]} - {x["por"]}% - {x["fecha"]}</div>'
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
 if 0<=i<len(d):
  d.pop(i)
  sv(d)
 return redirect("/")

@app.route("/edit/<int:i>",methods=["GET","POST"])
def ed(i):
 d=ld()
 if not (0<=i<len(d)): return redirect("/")
 if request.method=="POST":
  d[i]["p"]=request.form.get("p","")
  d[i]["op"]=[request.form.get("o1",""),request.form.get("o2",""),request.form.get("o3",""),request.form.get("o4","")]
  d[i]["co"]=int(request.form.get("c",0))
  sv(d)
  return redirect("/")
 q=d[i]
 return base("EDITAR PREGUNTA",f'<div class=card card-create style=margin:12px><b>✏️ EDITAR PREGUNTA Y GUARDAR</b><form method=post><input class=input name=p value="{q["p"]}"><input class=input name=o1 value="{q["op"][0]}"><input class=input name=o2 value="{q["op"][1]}"><input class=input name=o3 value="{q["op"][2]}"><input class=input name=o4 value="{q["op"][3]}"><select class=input name=c><option value=0 {"selected" if q["co"]==0 else ""}>A correcta</option><option value=1 {"selected" if q["co"]==1 else ""}>B correcta</option><option value=2 {"selected" if q["co"]==2 else ""}>C correcta</option><option value=3 {"selected" if q["co"]==3 else ""}>D correcta</option></select><button class="btn btn-green">💾 GUARDAR CAMBIO</button></form><a href=/cambiar class=btn-back style=margin-top:10px;display:inline-block>VOLVER SIN GUARDAR</a></div>')

def rex(preg,titulo):
 session["ex"]=preg
 session["titulo"]=titulo
 b=f'<div class="sec-title title-trabajando">{titulo} - {len(preg)} preguntas</div>'
 b+='<div style=margin:12px><a href=/cambiar class=btn-inicio>🏠 INICIO</a></div>'
 b+=f'<form method=post action=/cal>'
 for i,q in enumerate(preg):
  b+=f'<div class=card card-hi><div style=display:flex;justify-content:space-between><span class=badge style=background:#C5A059;color:#000>{q["materia"]}</span><span>{i+1}/{len(preg)}</span></div><b style=display:block;margin:10px 0>{q["p"]}</b>'
  for j,op in enumerate(q["op"]):
   b+=f'<label class=opt><input type=radio name="r{i}" value="{j}" required> {op}</label>'
  b+='</div>'
 b+='<button class="btn btn-gold" style=margin:12px;width:96%;padding:15px;font-size:14px>✅ CALIFICAR EXAMEN</button></form>'
 return base(titulo,b)

@app.route("/exam_materia",methods=["GET","POST"])
def em():
 m=(request.form.get("m") or request.args.get("m") or session.get("materia_actual") or "").strip().upper()
 if not m: return redirect("/")
 pr=[p for p in ld() if p["materia"]==m]
 if not pr: return base(m,f'<div class=card>No hay preguntas en {m} - <a href=/ class=btn-back>VOLVER A CREAR</a></div>')
 random.shuffle(pr)
 return rex(pr,f"EXAMEN {m}")

@app.route("/exam_general",methods=["GET","POST"])
def eg():
 pr=ld()
 if not pr: return base("GENERAL",'<div class=card>No hay preguntas - crea materias y preguntas primero</div>')
 random.shuffle(pr)
 return rex(pr,"EXAMEN GENERAL")

@app.route("/exam_personalizado",methods=["GET","POST"])
def ep():
 ms=request.form.getlist("mats")
 if not ms: return redirect("/")
 pr=[p for p in ld() if p["materia"] in ms]
 if not pr: return base("PERSONALIZADO",'<div class=card>No hay preguntas en las materias seleccionadas</div>')
 random.shuffle(pr)
 return rex(pr,"EXAMEN "+" + ".join(ms))

@app.route("/cal",methods=["POST"])
def ca2():
 ex=session.get("ex",[])
 ti=session.get("titulo","EXAMEN")
 ok=0
 for i,q in enumerate(ex):
  v=request.form.get(f"r{i}")
  try: tu=int(v)
  except: tu=-1
  if tu==q["co"]: ok+=1
 po=int(ok/len(ex)*100) if ex else 0
 from datetime import datetime as dt
 fe=dt.now().strftime("%d/%m/%Y %H:%M")
 h=ld_h()
 h.append({"fecha":fe,"titulo":ti,"por":po})
 sv_h(h)
 return base(ti,f'<div class=card style=text-align:center;padding:30px><h1 style=font-size:48px;color:#4CAF50;margin:0>{po}%</h1><p style=font-size:18px>{ok} correctas de {len(ex)}</p><div style=margin-top:20px;display:flex;gap:10px;justify-content:center><a href=/cambiar class=btn-inicio>🏠 INICIO</a><a href=/historial class=btn-back>HISTORIAL</a></div></div>')

app.run(host="0.0.0.0",port=5002)


