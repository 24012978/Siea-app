import os, json, random
from flask import Flask, request, redirect, session
from datetime import datetime as dt
app = Flask(__name__)
app.secret_key = "siea_app_definitivo_2026"

DB_USERS = os.path.expanduser("~/usuarios_siea.json")

def layout(contenido, titulo="S.I.E.A."):
    return f'''
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@300;600;900&display=swap" rel="stylesheet">
    <style>
        body {{ margin: 0; background: #051C05; color: #E8F5E9; font-family: 'Montserrat', sans-serif; }}
        .header {{ background: #0A2F0A; padding: 20px; border-bottom: 4px solid #4CAF50; text-align: center; }}
        .title {{ font-size: 32px; font-style: italic; font-weight: 900; color: #FFD700; margin: 0; }}
        .card {{ background: #0D2E0D; border: 1px solid #2E7D32; border-radius: 12px; padding: 20px; margin: 20px; }}
        .btn {{ display: block; width: 100%; padding: 15px; background: #FFD700; color: #000; text-align: center; border-radius: 8px; font-weight: 900; text-decoration: none; margin-top: 10px; border: none; cursor: pointer; box-sizing: border-box; }}
        input {{ width: 100%; padding: 12px; margin: 10px 0; border-radius: 6px; border: 1px solid #4CAF50; background: #051C05; color: #fff; box-sizing: border-box; }}
        label {{ display: block; margin: 10px 0; color: #C8E6C9; }}
    </style>
    <div class="header"><h1 class="title">{titulo}</h1></div>
    {contenido}
    '''

# ENTRADA DIRECTA AL PANEL (SIN BARRERAS DE ACCESO)
@app.route("/")
def panel():
    h = f'''
    <div class="card">
        <h2 style="color:#FFD700">🚀 MÓDULO DE EXÁMENES</h2>
        <a href="/exam_general" class="btn" style="background:#1E88E5; color:#fff;">EXAMEN GENERAL</a>
        <a href="/exam_personalizado" class="btn" style="background:#8E24AA; color:#fff;">EXAMEN PERSONALIZADO</a>
    </div>
    <div class="card">
        <h2 style="color:#4CAF50">📚 BANCO DE PREGUNTAS Y MATERIAS</h2>
        <a href="/banco" style="color:#81C784; font-weight:bold; font-size:16px;">Gestionar materias y editar reactivos</a>
    </div>
    <div class="card">
        <p style="font-size: 13px; text-align: justify;"><b>Propósito Institucional:</b> Sistema avanzado para la evaluación y gestión de reactivos académicos.<br><br>
        <b>Aviso de Privacidad:</b> Control activo de suscripción y usuarios.</p>
        <a href="https://wa.me/528110290152" class="btn" style="background:#2E7D32; color:#fff;">💳 PAGAR SUSCRIPCIÓN / SOPORTE (+52 81 1029 0152)</a>
    </div>
    '''
    return layout(h, "S.I.E.A. - Panel Principal")

@app.route("/exam_general")
def ex_g(): 
    return layout("<h2>Examen General</h2><p>Aquí se cargan todas las materias de forma aleatoria.</p><a href='/' class='btn'>Volver al Panel</a>", "Examen General")

@app.route("/exam_personalizado")
def ex_p(): 
    # Casillas para elegir materias
    h = '<h2>Examen Personalizado</h2><form>'
    for m in ["HI", "MOM", "LEY ORGANICA"]:
        h += f'<label><input type="checkbox" name="m" value="{m}"> {m}</label><br>'
    h += '<button class="btn">INICIAR EXAMEN SELECCIONADO</button></form><br><a href="/" style="color:#fff;">Volver</a>'
    return layout(h, "Examen Personalizado")

@app.route("/banco")
def banco(): 
    return layout("<h2>Gestión de Banco y Materias</h2><p>Aquí puedes editar, borrar y agregar tus materias y preguntas.</p><a href='/' class='btn'>Volver al Panel</a>", "Banco de Preguntas")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)

