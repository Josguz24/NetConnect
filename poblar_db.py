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
            correo_personal TEXT,
            correo_empresa TEXT,
            telefono TEXT,
            fecha_ultimo_mensaje TEXT,
            relevante INTEGER
        )
    ''')
    conn.commit()
    conn.close()

# Insertar contactos de ejemplo
def poblar_contactos():
    from random import choice, randint
    from datetime import timedelta
    nombres = [
        'Ana Pérez', 'Luis Gómez', 'María López', 'Carlos Ruiz', 'Sofía Torres', 'Javier Sánchez', 'Elena Ramírez', 'Miguel Castro',
        'Lucía Fernández', 'Pedro Morales', 'Valeria Herrera', 'Andrés Vargas', 'Paula Mendoza', 'Diego Ríos', 'Camila Ortega',
        'Gabriel Silva', 'Martina Soto', 'Hugo Delgado', 'Isabel Paredes', 'Tomás Aguirre', 'Natalia León', 'Samuel Peña',
        'Victoria Salas', 'Emilio Bravo', 'Renata Cordero', 'Matías Lozano', 'Daniela Figueroa', 'Pablo Castaño', 'Sara Molina',
        'Adrián Gil', 'Julia Navarro', 'Iván Serrano', 'Alicia Pastor', 'Mario Ibáñez', 'Clara Rueda', 'Álvaro Pastor', 'Teresa Solís',
        'Óscar Marín', 'Carmen Ponce', 'Rubén Arias', 'Nuria Benítez', 'Francisco Vera', 'Marta Zamora', 'Raúl Cordero', 'Patricia Sáez',
        'Sergio Vidal', 'Eva Cano', 'Guillermo Ríos', 'Lorena Pizarro', 'Felipe Barrios', 'Andrea Mena'
    ]
    categorias = ['mentor', 'aliado', 'inversionista', 'prospecto', 'cliente', 'proveedor', 'colaborador', 'amigo profesional']
    sectores = ['tecnología', 'educación', 'salud', 'finanzas', 'energía', 'legal', 'manufactura', 'gobierno']
    roles = ['fundador', 'ceo', 'gerente', 'coordinador', 'asesor', 'estudiante', 'desarrollador', 'diseñador', 'profesor', 'abogado', 'consultor', 'ingeniero']
    intereses_lista = ['innovación', 'docencia', 'contratos', 'leyes', 'desarrollo', 'IA', 'emprendimiento', 'startups', 'networking', 'inversión', 'tecnología', 'proyectos', 'negocios', 'educación', 'legal', 'mentor', 'eventos', 'viajes', 'corporativo']
    tags_lista = ['mentor', 'legal', 'proveedor', 'tecnología', 'IA', 'startups', 'negocios', 'educación', 'global', 'internacional', 'corporativo']
    contactos = []
    base_date = datetime.now()
    for i, nombre in enumerate(nombres):
        categoria = choice(categorias)
        sector = choice(sectores)
        rol = choice(roles)
        intereses = ', '.join(choice(intereses_lista) for _ in range(randint(2, 4)))
        tags = ', '.join(choice(tags_lista) for _ in range(randint(2, 3)))
        correo_personal = f"{nombre.split()[0].lower()}.{nombre.split()[1].lower()}@gmail.com"
        correo_empresa = f"{nombre.split()[0][0].lower()}{nombre.split()[1].lower()}@empresa.com"
        telefono = f"555-{randint(1000,9999)}"
        fecha_ultimo_mensaje = (base_date - timedelta(days=randint(0, 365))).strftime('%Y-%m-%d')
        relevante = 1 if i % 3 == 0 else 0
        contactos.append((nombre, categoria, sector, rol, intereses, tags, correo_personal, correo_empresa, telefono, fecha_ultimo_mensaje, relevante))
    # Si menos de 50, rellena con nombres generados
    while len(contactos) < 50:
        nombre = f"Nombre{len(contactos)+1} Apellido{len(contactos)+1}"
        categoria = choice(categorias)
        sector = choice(sectores)
        rol = choice(roles)
        intereses = ', '.join(choice(intereses_lista) for _ in range(randint(2, 4)))
        tags = ', '.join(choice(tags_lista) for _ in range(randint(2, 3)))
        correo_personal = f"nombre{len(contactos)+1}.apellido{len(contactos)+1}@gmail.com"
        correo_empresa = f"n{len(contactos)+1}apellido{len(contactos)+1}@empresa.com"
        telefono = f"555-{randint(1000,9999)}"
        fecha_ultimo_mensaje = (base_date - timedelta(days=randint(0, 365))).strftime('%Y-%m-%d')
        relevante = randint(0, 1)
        contactos.append((nombre, categoria, sector, rol, intereses, tags, correo_personal, correo_empresa, telefono, fecha_ultimo_mensaje, relevante))
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    c.executemany('''
        INSERT INTO contactos (nombre, categoria, sector, rol, intereses, tags, correo_personal, correo_empresa, telefono, fecha_ultimo_mensaje, relevante)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', contactos)
    conn.commit()
    conn.close()

if __name__ == '__main__':
    crear_tabla()
    poblar_contactos()
    print('Base de datos poblada con contactos de ejemplo.')
