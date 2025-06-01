# Archivo creado para poblar la base de datos con contactos de ejemplo.
import sqlite3
from datetime import datetime

# Crear tabla si no existe
def crear_tabla():
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS contactos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            categoria TEXT,
            sector TEXT,
            rol TEXT,
            intereses TEXT,
            tags TEXT,
            fecha_ultimo_mensaje TEXT,
            relevante INTEGER
        )
    ''')
    conn.commit()
    conn.close()

# Insertar contactos de ejemplo
def poblar_contactos():
    contactos = [
        ('Ana Pérez', 'mentor', 'educación', 'profesor', 'innovación, docencia', 'educación, mentor', datetime.now().strftime('%Y-%m-%d'), 1),
        ('Luis Gómez', 'proveedor', 'legal', 'abogado', 'contratos, leyes', 'legal, proveedor', datetime.now().strftime('%Y-%m-%d'), 1),
        ('María López', 'colaborador', 'tecnología', 'ingeniero', 'desarrollo, IA', 'tecnología, IA', datetime.now().strftime('%Y-%m-%d'), 0),
        ('Carlos Ruiz', 'amigo profesional', 'negocios', 'consultor', 'emprendimiento, startups', 'negocios, startups', datetime.now().strftime('%Y-%m-%d'), 1),
    ]
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    c.executemany('''
        INSERT INTO contactos (nombre, categoria, sector, rol, intereses, tags, fecha_ultimo_mensaje, relevante)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', contactos)
    conn.commit()
    conn.close()

if __name__ == '__main__':
    crear_tabla()
    poblar_contactos()
    print('Base de datos poblada con contactos de ejemplo.')
