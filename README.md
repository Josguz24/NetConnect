# Sistema Experto de Gestión de Contactos

Este proyecto es una aplicación web desarrollada en Python usando Flask y SQLite para gestionar contactos y sugerir conexiones según diferentes criterios.

## Estructura del proyecto
- `app.py`: Código principal de la aplicación Flask.
- `inference.py`: Lógica para sugerir contactos.
- `models.py`: Archivo reservado para futuras implementaciones de modelos.
- `poblar_db.py`: Script para crear y poblar la base de datos con contactos de ejemplo.
- `db.sqlite3`: Base de datos SQLite (puede ser generada con el script de poblar).
- `templates/index.html`: Interfaz web.
- `requirements.txt`: Dependencias del proyecto.

## Instalación y uso
1. **Instala las dependencias:**
   ```powershell
   pip install -r requirements.txt
   ```
2. **Crea y/o pobla la base de datos con datos de ejemplo:**
   ```powershell
   python poblar_db.py
   ```
3. **Ejecuta la aplicación:**
   ```powershell
   python app.py
   ```
4. Abre tu navegador en [http://localhost:5000](http://localhost:5000)

## Notas
- Si ya tienes un archivo `db.sqlite3` con datos, puedes omitir el paso 2.
- El script `poblar_db.py` es seguro de ejecutar varias veces; solo agrega los contactos de ejemplo si la tabla existe.
- Puedes modificar o eliminar los contactos desde la interfaz web.

---

¡Listo para compartir y probar tu sistema experto!
