# API Flask CRUD de Usuarios

Esta es una API RESTful desarrollada en Python con Flask. El proyecto sirve como un laboratorio práctico para la migración de una API originalmente escrita en Node.js, implementando un CRUD de usuarios con almacenamiento en memoria.

## 🚀 Tecnologías

| Equivalencia Node.js | Tecnología en Python | Descripción |
|----------------------|-----------------------|-------------|
| Express.js           | **Flask**             | Microframework web ligero |
| Jest / Mocha         | **pytest**            | Framework de pruebas (Testing) |
| dotenv               | **python-dotenv**     | Carga de variables de entorno |
| CORS middleware      | **flask-cors**        | Manejo de peticiones de origen cruzado (CORS) |
| nodemon              | **Flask Debug Mode**  | Recarga automática en desarrollo |

## ⚙️ Instalación y Configuración

Sigue estos pasos para levantar el proyecto localmente:

1. **Clonar el repositorio:**
   ```bash
   git clone <URL-del-repo>
   cd mi-api-flask-python
   ```

2. **Crear y activar el entorno virtual:**
   - En Windows:
     ```bash
     python -m venv venv
     venv\Scripts\activate
     ```
   - En macOS / Linux:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

3. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar variables de entorno:**
   - Copia el archivo de ejemplo para crear tu `.env`:
     ```bash
     cp .env.example .env
     ```
   - (Opcional) Ajusta los valores en el `.env` (ej. `PORT=5000`).

## 🏃 Ejecución del Servidor

Para iniciar el servidor en modo desarrollo (con auto-recarga):

```bash
python run.py
```
La API estará disponible en `http://localhost:5000/api/users`.

## 🧪 Pruebas (Tests)

Para correr la suite completa de pruebas unitarias y verificar el correcto funcionamiento de los endpoints:

```bash
pytest tests/ -v
```

## 📡 Endpoints

| Método   | Ruta                 | Descripción                                  |
|----------|----------------------|----------------------------------------------|
| `GET`    | `/api/users/`        | Lista todos los usuarios                     |
| `GET`    | `/api/users/<id>`    | Obtiene un usuario por su ID                 |
| `POST`   | `/api/users/`        | Crea un nuevo usuario                        |
| `PUT`    | `/api/users/<id>`    | Actualiza parcialmente un usuario existente  |
| `DELETE` | `/api/users/<id>`    | Elimina un usuario por su ID                 |

### Ejemplos de Peticiones y Respuestas

#### GET `/api/users/`
**Respuesta (200 OK):**
```json
{
  "success": true,
  "data": [
    { "id": 1, "name": "Juan Garcia", "email": "juangarcia@gmail.com", "age": 28 }
  ],
  "total": 1
}
```

#### GET `/api/users/1`
**Respuesta (200 OK):**
```json
{
  "success": true,
  "data": { "id": 1, "name": "Juan Garcia", "email": "juangarcia@gmail.com", "age": 28 }
}
```

#### POST `/api/users/`
**Body:**
```json
{ "name": "Carlos", "email": "carlos@test.com", "age": 30 }
```
**Respuesta (201 Created):**
```json
{
  "success": true,
  "message": "Usuario Creado exitosamente",
  "data": { "id": 4, "name": "Carlos", "email": "carlos@test.com", "age": 30 }
}
```

#### PUT `/api/users/1`
**Body:**
```json
{ "age": 29 }
```
**Respuesta (200 OK):**
```json
{
  "success": true,
  "message": "Usuario Actualizado exitosamente",
  "data": { "id": 1, "name": "Juan Garcia", "email": "juangarcia@gmail.com", "age": 29 }
}
```

#### DELETE `/api/users/1`
**Respuesta (200 OK):**
```json
{
  "success": true,
  "message": "Usuario eliminado exitosamente",
  "data": { "id": 1, "name": "Juan Garcia", "email": "juangarcia@gmail.com", "age": 29 }
}
```

## 🌿 Git Flow y Commits Semánticos

El proyecto sigue una metodología basada en **Git Flow**:
- `main`: Código de producción (estable).
- `develop`: Rama principal de integración y desarrollo.
- Ramas de características (`feature/*`): Salen de `develop` y se fusionan mediante Pull Requests.
- Ramas de release (`release/*`): Usadas para preparar nuevas versiones de `develop` a `main`.

**Commits Semánticos**:
Se utilizan los prefijos convencionales para mantener un historial ordenado:
- `feat:` Nuevas características.
- `fix:` Solución de errores.
- `docs:` Actualización de documentación (`README`, `CHANGELOG`, Postman).
- `chore:` Tareas de mantenimiento, dependencias o configuración.
- `test:` Adición o mejora de pruebas.
