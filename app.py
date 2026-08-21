import os, json, random
from flask import Flask, request, redirect, session
from datetime import datetime
app = Flask(__name__)
app.secret_key = "siea_2026_aprobacion_final"
DB = "preg.json"; HU = "hist.json"; UU = "user.json"
ADMINS = ["ADMIN","24012978","UNION"]

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
            with open(UU) as f:
                data=json.load(f)
                # compatibilidad con formato viejo
                for k,v in list(data.items()):
                    if isinstance(v,str): data[k]={"pass":v,"status":"aprobado","fecha":datetime.now().strftime("%d/%m/%Y")}
                return data
    except: pass
    return {}
def sv_u(d):
    with open(UU,"w") as f: json.dump(d,f)

def is_admin(): return session.get("user","") in ADMINS

def login_page(inner,msg=""):
    alert=f'<div style="background:#5A1A1A;border:1px solid #FF4444;padding:10px;border-radius:8px;margin-bottom:10px;text-align:center">{msg}</div>' if msg else ""
    return f"""<meta name="viewport" content="width=device-width,initial-scale=1"><style>
body{{margin:0;background:#060D06;color:#fff;font-family:system-ui;min-height:100vh}}
.top{{background:linear-gradient(180deg,#0A1A0A,#060D06);border-bottom:2px solid #2cff7a;padding:18px;text-align:center}}
.sigla{{font-size:34px;font-weight:900;letter-spacing:4px;color:#C5A059}}.sub{{font-size:11px;letter-spacing:2px;color:#7C9A7C}}
.card{{background:#121E12;border:1.5px solid #2A4A2A;border-radius:16px;padding:18px;margin:14px;box-shadow:0 0 20px rgba(44,255,122,0.15)}}
.lbl{{font-size:10px;letter-spacing:1.5px;color:#2cff7a;font-weight:800;margin:10px 0 4px 2px}}
.inp{{width:100%;padding:13px;background:#0A150A;border:1.5px solid #2A4A2A;border-radius:10px;color:#fff;box-sizing:border-box}}
.btn{{width:100%;padding:14px;border:0;border-radius:10px;font-weight:900;margin-top:12px;background:#2cff7a;color:#000;cursor:pointer}}
.btn-blue{{background:linear-gradient(180deg,#3A8CFF,#1A5DD1);color:#fff}}.badge-gold{{color:#FFD87A;font-weight:900;font-size:18px}}
.legal{{font-size:8.5px;color:#6E8A6E;margin-top:12px;text-align:justify}}
</style>
<div class=top><div class=sigla>S.I.E.A.</div><div class=sub>SISTEMA INTEGRAL DE EVALUACION PARA EL ASCENSO</div></div>
<div class=card><div style="text-align:center;color:#2cff7a;font-weight:900;letter-spacing:2px;margin-bottom:10px">ACCESO AUTORIZADO</div>{alert}{inner}
<div class=legal><b>AVISO:</b> Plataforma de uso interno y control institucional. Informacion confidencial.</div></div>
<div class=card style="border-color:#C5A059"><div style="text-align:center;color:#C5A059;font-weight:900;letter-spacing:2px;font-size:13px;margin-bottom:12px">SOPORTE Y SUSCRIPCION</div>
<div style="background:#1A2E1A;border-radius:12px;padding:14px;text-align:center;border:1px solid #2A4A2A;margin-bottom:12px"><div style="font-weight:900">📞 SOPORTE TECNICO DIRECTO</div><div class=badge-gold>+52 811 0290152</div><div style="font-size:10px;color:#7A9A7A">Lunes a Viernes 08:00-18:00</div></div>
<div style="background:#1A2E1A;border-radius:12px;padding:14px;text-align:center;border:1px solid #2A4A2A"><div style="font-weight:900;color:#2cff7a">💳 SUSCRIPCION PREMIUM</div><a href="https://wa.me/528110290152?text=Hola%20quiero%20pagar%20suscripcion%20SIEA%20Premium" style="text-decoration:none"><div class="btn btn-blue">🔒 PAGAR SUSCRIPCION - $9.99 USD</div></a></div></div>"""

def base(t,b):
    u=session.get("user",""); admin_btn = f'<a href=/admin class=btn-back style="background:#FFD700;color:#000">ADMIN</a>' if is_admin() else ''
    return f"""<meta name="viewport" content="width=device-width,initial-scale=1"><style>body{{margin:0;background:#0D1A0C;color:#fff;font-family:system-ui}}.top{{background:#C5A059;color:#000;padding:8px;text-align:center;font-weight:900}}.bar{{background:#1C2B1A;padding:8px;display:flex;justify-content:space-between;border-bottom:2px solid #C5A059}}.where{{background:#C5A059;color:#000;padding:10px;text-align:center;font-weight:900;border-radius:8px;margin:10px}}.card{{background:#1C2B1A;border:1px solid #3A5A33;border-radius:10px;padding:12px;margin:10px}}.input{{width:100%;padding:12px;background:#10180F;border:1px solid #C5A059;border-radius:8px;color:#fff;margin:5px 0;box-sizing:border-box}}.btn{{width:100%;padding:12px;border:0;border-radius:8px;font-weight:900;margin-top:8px}}.btn-gold{{background:#C5A059;color:#000}}.btn-back{{background:#2A3A2A;color:#fff;padding:6px 12px;border-radius:6px;text-decoration:none;font-size:13px}}.badge{{background:#C5A059;color:#000;padding:2px 6px;border-radius:4px;font-size:11px;font-weight:900}}.opt{{display:block;background:#10180F;border:1px solid #3A5A33;padding:10px;margin:6px 0;border-radius:8px}}.small{{font-size:12px;opacity:0.8}}</style><div class=top>S.I.E.A. - {t}</div><div class=bar><b>{u} {'(ADMIN)' if is_admin() else ''}</b><div>{admin_btn} <a href=/historial class=btn-back>HISTORIAL</a> <a href=/logout class=btn-back>SALIR</a></div></div>{b}"""

@app.route("/")
def ix():
    if 'user' not in session:
        form = '<div class=lbl>USUARIO / MATRICULA</div><input class=inp name=user placeholder="Ej. 123456"><div class=lbl>CONTRASEÑA</div><input class=inp type=password name=pass placeholder="••••••••"><button class=btn>INGRESAR AL SISTEMA</button><div style="text-align:center;font-size:11px;margin-top:8px;color:#7A9A7A">Nuevo usuario quedara pendiente de aprobacion</div>'
        return login_page(f'<form method=post action=/login>{form}</form>')
    ma=session.get('materia_actual')
    if not ma:
        ms={};
        for p in ld(): ms[p['materia']]=ms.get(p['materia'],0)+1
        h='<div class=where>SELECCIONA MATERIA</div>'
        for m in ["HI","MOM","LEY ORGANICA"]:
            c=ms.get(m,0)
            h+=f'<div class=card><b>{m} - {c} PREG</b><form method=post action=/set_materia><input type=hidden name=materia value="{m}"><button class="btn btn-gold">CONTINUAR EN {m}</button></form></div>'
        h+='<div class=card><b>EXAMEN GENERAL</b><form method=post action=/exam_general><button class="btn btn-gold">INICIAR GENERAL</button></form></div>'
        h+='<div class=card><b>EXAMEN PERSONALIZADO</b><form method=post action=/exam_personalizado>'
        for m in ["HI","MOM","LEY ORGANICA"]: h+=f'<label><input type=checkbox name=mats value="{m}"> {m}</label><br>'
        h+='<button class="btn btn-gold">CREAR PERSONALIZADO</button></form></div>'
        return base("INICIO",h)
    pr=[p for p in ld() if p['materia']==ma]; allp=ld()
    b=f'<a href=/cambiar class=btn-back style=margin:10px;display:inline-block>INICIO</a><div class=where>ESTAS EN: {ma}</div>'
    b+=f'<div class=card><b>AGREGAR A {ma}</b><form method=post action=/add><input class=input name=p placeholder="Pregunta"><input class=input name=o1 placeholder="A) CORRECTA"><input class=input name=o2 placeholder="B"><input class=input name=o3 placeholder="C"><input class=input name=o4 placeholder="D"><select class=input name=c><option value=0>A correcta</option><option value=1>B correcta</option><option value=2>C correcta</option><option value=3>D correcta</option></select><button class="btn btn-gold">GUARDAR EN {ma}</button></form></div>'
    b+=f'<div class=card><form method=post action=/exam_materia><input type=hidden name=m value="{ma}"><button class="btn btn-gold">EXAMEN DE {ma} - {len(pr)} PREG</button></form></div>'
    for idx,p in enumerate(allp):
        if p['materia']!=ma: continue
        b+=f'<div class=card><span class=badge>{p["materia"]}</span> <b>{p["p"]}</b><br><span class=small>A) {p["op"][0]}<br>B) {p["op"][1]}<br>C) {p["op"][2]}<br>D) {p["op"][3]}<br>Correcta: {["A","B","C","D"][p["co"]]} </span><br><br><a href=/edit/{idx} class=btn-back style="background:#C5A059;color:#000">EDITAR</a> <a href=/del/{idx} class=btn-back style="background:#5A1A1A" onclick="return confirm(\'Borrar?\')">BORRAR</a></div>'
    return base("INICIO",b)

@app.route("/admin")
def admin_panel():
    if not is_admin(): return redirect("/")
    us=ld_u(); h=ld_h(); pr=ld()
    pend=[k for k,v in us.items() if v.get("status")!="aprobado"]
    apro=[k for k,v in us.items() if v.get("status")=="aprobado"]
    b='<div class=where>PANEL ADMINISTRADOR - CONTROL DE ACCESO</div><a href=/ class=btn-back style=margin:10px;display:inline-block>INICIO</a>'
    b+=f'<div class=card style="border-color:#FF4444"><b>🔴 PENDIENTES POR APROBAR: {len(pend)}</b><br><br>'
    if not pend: b+='No hay pendientes'
    for u in pend:
        info=us[u]; b+=f'<div style="border-bottom:1px solid #333;padding:8px 0">{u} - {info.get("fecha","")} <a href=/aprobar/{u} class=btn-back style="background:#2cff7a;color:#000">APROBAR</a> <a href=/rechazar/{u} class=btn-back style="background:#5A1A1A">RECHAZAR</a></div>'
    b+='</div>'
    b+=f'<div class=card style="border-color:#2cff7a"><b>🟢 USUARIOS APROBADOS: {len(apro)}</b><br><br>'
    for u in apro: b+=f'{u} - {us[u].get("fecha","")}<br>'
    b+='</div>'
    b+=f'<div class=card><b>TOTAL PREGUNTAS: {len(pr)}</b> | <b>TOTAL EXAMENES: {len(h)}</b></div>'
    return base("ADMIN",b)

@app.route("/aprobar/<u>")
def aprobar(u):
    if not is_admin(): return redirect("/")
    us=ld_u()
    if u in us: us[u]["status"]="aprobado"; sv_u(us)
    return redirect("/admin")

@app.route("/rechazar/<u>")
def rechazar(u):
    if not is_admin(): return redirect("/")
    us=ld_u()
    if u in us: del us[u]; sv_u(us)
    return redirect("/admin")

@app.route("/set_materia",methods=["POST"])
def sm():
    m=request.form.get('materia','').strip().upper()
    if m: session['materia_actual']=m
    return redirect("/")
@app.route("/cambiar")
def ca(): session.pop('materia_actual',None); return redirect("/")
@app.route("/login",methods=["POST"])
def lg():
    u=request.form.get('user','').strip().upper(); p=request.form.get('pass','').strip(); us=ld_u()
    if u in us:
        if us[u].get("pass")!=p: return login_page("",msg="Contraseña incorrecta")
        if us[u].get("status")!="aprobado" and u not in ADMINS:
            return login_page("",msg="Tu cuenta esta PENDIENTE de aprobacion. Contacta al admin al 8110290152")
    else:
        # nuevo usuario -> pendiente, excepto si es admin
        status="aprobado" if u in ADMINS else "pendiente"
        us[u]={"pass":p,"status":status,"fecha":datetime.now().strftime("%d/%m/%Y %H:%M")}; sv_u(us)
        if status=="pendiente":
            return login_page("",msg=f"Usuario {u} registrado. Quedo pendiente de aprobacion por el administrador.")
    session['user']=u; return redirect("/")
@app.route("/logout")
def lo(): session.clear(); return redirect("/")
@app.route("/historial")
def hi():
    h=ld_h(); b='<div class=card><b>HISTORIAL</b> <a href=/ class=btn-back>INICIO</a></div>'
    lista=h if is_admin() else [x for x in h if x.get("usuario","")==session.get("user","")]
    for x in reversed(lista): b+=f'<div class=card>{x["titulo"]} - {x["por"]}% - {x["fecha"]} - {x.get("usuario","")}</div>'
    return base("HISTORIAL",b)
@app.route("/add",methods=["POST"])
def ad():
    mat=session.get('materia_actual'); p=ld(); p.append({"materia":mat,"p":request.form.get('p',''),"op":[request.form.get('o1',''),request.form.get('o2',''),request.form.get('o3',''),request.form.get('o4','')],"co":int(request.form.get('c',0))}); sv(p); return redirect("/")
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
        d[i]["p"]=request.form.get('p',''); d[i]["op"]=[request.form.get('o1',''),request.form.get('o2',''),request.form.get('o3',''),request.form.get('o4','')]; d[i]["co"]=int(request.form.get('c',0)); sv(d); return redirect("/")
    q=d[i]
    return base(f"EDITAR",f'<div class=card><form method=post><input class=input name=p value="{q["p"]}"><input class=input name=o1 value="{q["op"][0]}"><input class=input name=o2 value="{q["op"][1]}"><input class=input name=o3 value="{q["op"][2]}"><input class=input name=o4 value="{q["op"][3]}"><select class=input name=c><option value=0 {"selected" if q["co"]==0 else ""}>A</option><option value=1 {"selected" if q["co"]==1 else ""}>B</option><option value=2 {"selected" if q["co"]==2 else ""}>C</option><option value=3 {"selected" if q["co"]==3 else ""}>D</option></select><button class="btn btn-gold">GUARDAR CAMBIOS</button></form><br><a href=/ class=btn-back>VOLVER</a></div>')
def rex(preg,titulo):
    session['ex']=preg; session['titulo']=titulo; b=f'<div class=where>{titulo} - {len(preg)} preguntas</div><form method=post action=/cal>'
    for i,q in enumerate(preg):
        b+=f'<div class=card><span class=badge>{q["materia"]}</span> <b>{i+1}. {q["p"]}</b>'
        for j,op in enumerate(q["op"]): b+=f'<label class=opt><input type=radio name="r{i}" value="{j}"> {op}</label>'
        b+='</div>'
    b+='<button class=btn style="background:#C5A059;color:#000">CALIFICAR</button></form>'; return base(titulo,b)
@app.route("/exam_materia",methods=["GET","POST"])
def em():
    m=(request.form.get('m') or request.args.get('m') or session.get('materia_actual') or '').strip().upper()
    if not m: return redirect("/")
    pr=[p for p in ld() if p['materia']==m]
    if not pr: return base(m,f'<div class=card>No hay preguntas en {m}</div>')
    random.shuffle(pr); return rex(pr,f"EXAMEN {m}")
@app.route("/exam_general",methods=["GET","POST"])
def eg():
    pr=ld()
    if not pr: return base("GENERAL",'<div class=card>No hay preguntas</div>')
    random.shuffle(pr); return rex(pr,"EXAMEN GENERAL")
@app.route("/exam_personalizado",methods=["GET","POST"])
def ep():
    ms=request.form.getlist('mats')
    if not ms: return redirect("/")
    pr=[p for p in ld() if p['materia'] in ms]
    if not pr: return base("PERSONALIZADO",'<div class=card>No hay preguntas</div>')
    random.shuffle(pr); return rex(pr,"EXAMEN "+" + ".join(ms))
@app.route("/cal",methods=["POST"])
def ca2():
    ex=session.get('ex',[]); ti=session.get('titulo','EXAMEN'); ok=0
    for i,q in enumerate(ex):
        v=request.form.get(f"r{i}")
        try: tu=int(v)
        except: tu=-1
        if tu==q['co']: ok+=1
    po=int(ok/len(ex)*100) if ex else 0
    fe=datetime.now().strftime("%d/%m/%Y %H:%M")
    h=ld_h(); h.append({"fecha":fe,"titulo":ti,"por":po,"ok":ok,"total":len(ex),"usuario":session.get('user','')}); sv_h(h)
    return base(ti,f'<div class=card style=text-align:center><h1>{po}%</h1><p>{ok}/{len(ex)}</p><a href=/cambiar class=btn-back>INICIO</a> <a href=/historial class=btn-back>HISTORIAL</a></div>')
if __name__ == "__main__":
    app.run(host="0.0.0.0",port=10000)
