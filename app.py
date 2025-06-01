from flask import Flask, render_template, request, jsonify
import sqlite3
from inference import suggest_connections

app = Flask(__name__)

# Conexión a la base de datos
def get_db_connection():
    conn = sqlite3.connect('db.sqlite3')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sugerir', methods=['POST'])
def sugerir():
    contexto = request.json
    sugerencias = suggest_connections(contexto)
    return jsonify(sugerencias)

@app.route('/agregar_contacto', methods=['POST'])
def agregar_contacto():
    data = request.json
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    c.execute("""
        INSERT INTO contactos (nombre, categoria, sector, rol, intereses, tags, fecha_ultimo_mensaje, relevante)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data.get('nombre'),
        data.get('categoria'),
        data.get('sector'),
        data.get('rol'),
        data.get('intereses'),
        data.get('tags'),
        data.get('fecha_ultimo_mensaje'),
        int(data.get('relevante', 0))
    ))
    conn.commit()
    conn.close()
    return jsonify({"ok": True, "msg": "Contacto agregado correctamente."})

@app.route('/contactos', methods=['GET'])
def contactos():
    conn = sqlite3.connect('db.sqlite3')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM contactos ORDER BY nombre ASC")
    contactos = [dict(row) for row in c.fetchall()]
    conn.close()
    return jsonify(contactos)

@app.route('/eliminar_contacto', methods=['POST'])
def eliminar_contacto():
    data = request.json
    contacto_id = data.get('id')
    if not contacto_id:
        return jsonify({'ok': False, 'msg': 'ID no proporcionado.'}), 400
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    c.execute("DELETE FROM contactos WHERE id = ?", (contacto_id,))
    conn.commit()
    conn.close()
    return jsonify({'ok': True, 'msg': 'Contacto eliminado correctamente.'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
