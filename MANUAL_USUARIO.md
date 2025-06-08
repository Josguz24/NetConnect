# Manual de Usuario – Sistema Experto de Gestión de Contactos

## Descripción General

El Sistema Experto de Gestión de Contactos es una aplicación web desarrollada en Python utilizando el framework Flask y una base de datos SQLite. Su objetivo es facilitar la gestión de contactos profesionales y sugerir conexiones relevantes según las necesidades del usuario, apoyando la toma de decisiones en redes de colaboración, mentoría, negocios y educación.

---

## ¿Qué hace el sistema?

- Permite agregar, listar y eliminar contactos en una base de datos.
- Sugiere contactos relevantes según criterios personalizados (palabras clave, sector, perfil, etc.).
- Ofrece una interfaz web sencilla para interactuar con el sistema.
- Incluye un script para poblar la base de datos con ejemplos, facilitando la prueba y demostración.

---

## Estructura de Archivos

- **app.py**: Archivo principal. Define la aplicación Flask y las rutas para agregar, listar, eliminar y sugerir contactos.
- **inference.py**: Contiene la lógica para sugerir contactos relevantes según el contexto proporcionado por el usuario.
- **poblar_db.py**: Script que crea la tabla de contactos (si no existe) y la llena con datos de ejemplo.
- **db.sqlite3**: Base de datos SQLite donde se almacenan los contactos.
- **templates/index.html**: Interfaz web para interactuar con el sistema.
- **requirements.txt**: Lista de dependencias necesarias para ejecutar el sistema.
- **models.py**: Archivo reservado para futuras expansiones.

---

## Instalación y Primeros Pasos

1. **Instalar dependencias**
   - Abre una terminal en la carpeta del proyecto.
   - Ejecuta:
     ```
     pip install -r requirements.txt
     ```

2. **Poblar la base de datos con ejemplos**
   - Ejecuta:
     ```
     python poblar_db.py
     ```
   - Esto creará la base de datos `db.sqlite3` (si no existe) y agregará contactos de ejemplo.

3. **Ejecutar la aplicación**
   - Ejecuta:
     ```
     python app.py
     ```
   - El sistema iniciará en modo servidor web y mostrará la dirección local (por defecto: http://localhost:5000).

4. **Abrir la interfaz web**
   - Abre tu navegador y visita [http://localhost:5000](http://localhost:5000).

---

## ¿Cómo funciona cada parte?

### 1. Agregar Contacto

- Desde la interfaz web puedes ingresar los datos de un nuevo contacto (nombre, categoría, sector, rol, intereses, tags, fecha del último mensaje y si es relevante).
- Al hacer clic en “Agregar”, el sistema guarda el contacto en la base de datos.
- Si el contacto se agrega correctamente, verás un mensaje de confirmación.

### 2. Listar Contactos

- Al ingresar a la página principal, se muestra la lista de todos los contactos almacenados, ordenados alfabéticamente por nombre.
- Cada contacto muestra su información relevante.

### 3. Eliminar Contacto

- Puedes eliminar un contacto desde la interfaz web.
- El sistema solicita el ID del contacto y, si existe, lo elimina de la base de datos.
- Se muestra un mensaje confirmando la eliminación.

### 4. Sugerir Contactos

- El sistema puede sugerir contactos relevantes según el contexto que proporciones (por ejemplo, necesidad, sector, perfil, si buscas solo contactos legales o educativos, etc.).
- La lógica de sugerencia está en `inference.py` y utiliza filtros inteligentes para encontrar coincidencias en intereses, sector, rol, tags y otros criterios.
- Si no hay coincidencias directas, el sistema busca contactos relevantes por sector o por tiempo sin contacto.

- Ahora puedes seleccionar uno o varios tags predefinidos al agregar un contacto.
- El formulario de agregar contacto incluye campos para correo personal, correo de empresa y teléfono.
- Cuando el sistema recomienda un contacto, puedes ver y compartir su información fácilmente mediante un código QR.

### Compartir contacto por QR

- En la sección de recomendaciones, cada contacto sugerido tiene un botón "Ver QR".
- Al hacer clic, se abre una imagen QR que puedes escanear o compartir, la cual contiene toda la información relevante del contacto.

---

## ¿Qué ocurre cuando ejecutas cada archivo?

- **poblar_db.py**: Crea la tabla de contactos si no existe y agrega contactos de ejemplo. Es seguro ejecutarlo varias veces.
- **app.py**: Inicia el servidor web. Permite interactuar con la base de datos a través de la interfaz web.
- **inference.py**: No se ejecuta directamente, pero es llamado por la aplicación para sugerir contactos.

---

## Recomendaciones

- Si quieres empezar con una base vacía, elimina o renombra el archivo `db.sqlite3` y ejecuta de nuevo `poblar_db.py` si deseas cargar ejemplos.
- Puedes modificar el archivo `poblar_db.py` para agregar tus propios contactos de ejemplo.
- El sistema es extensible: puedes agregar nuevas funciones en `models.py` o mejorar la lógica de sugerencias en `inference.py`.

---

## Soporte

Si tienes dudas o problemas, revisa el archivo `README.md` incluido en el proyecto para instrucciones rápidas.

---

*Incluye capturas de pantalla de la interfaz web mostrando la lista de contactos, el formulario de agregar, la función de sugerencias y la eliminación de un contacto para completar la demostración.*
