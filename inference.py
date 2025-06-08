import sqlite3
from datetime import datetime, timedelta
import re

def ia_recomendar_contactos(need, contacts, top_n=3):
    """
    Algoritmo IA mejorado: calcula relevancia por similitud de palabras clave entre la necesidad (contexto del proyecto) y los campos del contacto.
    Devuelve una lista de los contactos más relevantes.
    """
    if not contacts or not need:
        return contacts[:top_n] if contacts else []
    need_words = set(re.findall(r'\w+', need.lower()))
    scored = []
    for c in contacts:
        score = 0
        # Suma puntos por coincidencia en intereses, sector, rol, tags, categoria
        for field in ['intereses', 'sector', 'rol', 'tags', 'categoria']:
            value = (c.get(field) or '').lower()
            value_words = set(re.findall(r'\w+', value))
            score += len(need_words & value_words)
        # Bonus si es relevante
        if c.get('relevante', 0):
            score += 1
        scored.append((score, c))
    # Ordena por score descendente y retorna los top_n
    scored.sort(reverse=True, key=lambda x: x[0])
    mejores = [c for score, c in scored if score > 0]
    if not mejores:
        mejores = [c for score, c in scored[:top_n]]
    return mejores[:top_n]

def suggest_connections(contexto):
    conn = sqlite3.connect('db.sqlite3')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    hoy = datetime.now()
    sugerencias = []
    explicaciones = {}

    necesidad = contexto.get('necesidad', '')
    internacional = contexto.get('internacional', False)
    proyectos_grandes = contexto.get('proyectos_grandes', False)
    perfil = contexto.get('perfil', '')
    solo_educacion = contexto.get('solo_educacion', False)
    solo_legal = contexto.get('solo_legal', False)

    keywords = []
    if necesidad:
        keywords = re.findall(r'\w+', necesidad.lower())

    # Filtros guiados
    if solo_educacion:
        cur.execute("SELECT * FROM contactos WHERE sector LIKE '%educa%' OR rol LIKE '%profesor%' OR rol LIKE '%maestro%' OR categoria='mentor' OR categoria='colaborador'")
        for row in cur.fetchall():
            if 'abogado' not in (row['rol'] or '').lower() and 'legal' not in (row['sector'] or '').lower():
                c = dict(row)
                c['explicacion'] = 'Coincide con sector educativo o rol académico.'
                sugerencias.append(c)
    elif solo_legal:
        cur.execute("SELECT * FROM contactos WHERE sector LIKE '%legal%' OR rol LIKE '%abogado%' OR categoria='proveedor'")
        for row in cur.fetchall():
            c = dict(row)
            c['explicacion'] = 'Coincide con sector legal o rol de abogado/proveedor.'
            sugerencias.append(c)
    else:
        cur.execute('SELECT * FROM contactos')
        for row in cur.fetchall():
            match = False
            explicacion = []
            for kw in keywords:
                if kw in (row['intereses'] or '').lower():
                    match = True
                    explicacion.append(f"Palabra clave en intereses: {kw}")
                if kw in (row['sector'] or '').lower():
                    match = True
                    explicacion.append(f"Palabra clave en sector: {kw}")
                if kw in (row['rol'] or '').lower():
                    match = True
                    explicacion.append(f"Palabra clave en rol: {kw}")
                if kw in (row['tags'] or '').lower():
                    match = True
                    explicacion.append(f"Palabra clave en tags: {kw}")
            if match:
                c = dict(row)
                c['explicacion'] = '; '.join(explicacion) if explicacion else 'Coincidencia por palabra clave.'
                sugerencias.append(c)

    # Filtros adicionales por preguntas
    if internacional:
        nuevas = []
        for c in sugerencias:
            if any(x in (c['intereses'] or '').lower() for x in ['internacional', 'global', 'extranjero', 'eventos', 'viajes']) or any(x in (c['tags'] or '').lower() for x in ['internacional', 'global']):
                c['explicacion'] += '; Coincidencia en intereses/tags internacional'
                nuevas.append(c)
        sugerencias = nuevas
    if proyectos_grandes:
        nuevas = []
        for c in sugerencias:
            if any(x in (c['intereses'] or '').lower() for x in ['proyecto', 'empresa', 'corporativo', 'startup', 'grande']) or any(x in (c['tags'] or '').lower() for x in ['proyecto', 'empresa', 'corporativo', 'startup', 'grande']):
                c['explicacion'] += '; Experiencia en proyectos grandes'
                nuevas.append(c)
        sugerencias = nuevas
    if perfil == 'academico':
        nuevas = []
        for c in sugerencias:
            if c['categoria'] in ['mentor', 'colaborador'] or 'profesor' in (c['rol'] or '').lower() or 'maestro' in (c['rol'] or '').lower():
                c['explicacion'] += '; Perfil académico'
                nuevas.append(c)
        sugerencias = nuevas
    elif perfil == 'practico':
        nuevas = []
        for c in sugerencias:
            if c['categoria'] in ['proveedor', 'amigo profesional', 'cliente potencial'] or 'proveedor' in (c['rol'] or '').lower():
                c['explicacion'] += '; Perfil práctico'
                nuevas.append(c)
        sugerencias = nuevas

    # Si no hay coincidencias, usar reglas generales
    if not sugerencias:
        # Reglas generales (pueden no devolver nada si no hay tablas auxiliares)
        try:
            cur.execute('''\
                SELECT c1.* FROM contactos c1
                JOIN eventos_compartidos e ON c1.id = e.contacto_id
                WHERE c1.sector = (SELECT sector FROM usuario LIMIT 1)
            ''')
            for row in cur.fetchall():
                c = dict(row)
                c['explicacion'] = 'Coincidencia por sector compartido.'
                sugerencias.append(c)
        except Exception:
            pass
        hace_60 = (hoy - timedelta(days=60)).strftime('%Y-%m-%d')
        cur.execute('''
            SELECT * FROM contactos
            WHERE fecha_ultimo_mensaje < ? AND relevante = 1
        ''', (hace_60,))
        for row in cur.fetchall():
            c = dict(row)
            c['explicacion'] = 'Contacto relevante no contactado en 60 días.'
            sugerencias.append(c)

    # NUEVO: Si sigue sin haber sugerencias, recomendar al menos un contacto (el primero o uno aleatorio)
    if not sugerencias:
        cur.execute('SELECT * FROM contactos ORDER BY relevante DESC, fecha_ultimo_mensaje ASC, id ASC LIMIT 1')
        row = cur.fetchone()
        if row:
            c = dict(row)
            c['explicacion'] = 'Sugerencia general: no hubo coincidencias, pero este contacto puede ser útil.'
            sugerencias.append(c)

    # IA propia: Si sigue sin haber sugerencias, recomendar los contactos más relevantes según similitud de palabras clave y contexto
    if not sugerencias:
        cur.execute('SELECT * FROM contactos')
        all_contacts = [dict(row) for row in cur.fetchall()]
        if all_contacts:
            mejores = ia_recomendar_contactos(necesidad, all_contacts, top_n=3)
            for c in mejores:
                c['explicacion'] = 'Seleccionado por IA interna como relevante para tu proyecto/idea.'
                sugerencias.append(c)

    conn.close()
    return sugerencias
