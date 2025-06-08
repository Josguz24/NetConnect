from flask import Flask, render_template, request, jsonify, send_file
import sqlite3
from inference import suggest_connections
import qrcode
import io

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
        INSERT INTO contactos (nombre, categoria, sector, rol, intereses, tags, fecha_ultimo_mensaje, relevante, correo_personal, correo_empresa, telefono)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data.get('nombre'),
        data.get('categoria'),
        data.get('sector'),
        data.get('rol'),
        data.get('intereses'),
        data.get('tags'),
        data.get('fecha_ultimo_mensaje'),
        int(data.get('relevante', 0)),
        data.get('correo_personal'),
        data.get('correo_empresa'),
        data.get('telefono'),
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

@app.route('/qr_contacto/<int:contacto_id>')
def qr_contacto(contacto_id):
    conn = sqlite3.connect('db.sqlite3')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM contactos WHERE id = ?", (contacto_id,))
    row = c.fetchone()
    conn.close()
    if not row:
        return 'Contacto no encontrado', 404
    info = f"Nombre: {row['nombre']}\nCategoría: {row['categoria']}\nSector: {row['sector']}\nRol: {row['rol']}\nCorreo personal: {row['correo_personal']}\nCorreo empresa: {row['correo_empresa']}\nTeléfono: {row['telefono']}\nIntereses: {row['intereses']}\nTags: {row['tags']}"
    img = qrcode.make(info)
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)
    return send_file(buf, mimetype='image/png')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
