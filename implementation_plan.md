# Plan de Implementación — API Flask CRUD de Usuarios

## Lo que hay que hacer (resumen)

Reescribir la API de Node.js en **Python + Flask**. Es un CRUD de usuarios
(`name`, `email`, `age`) con almacenamiento en memoria, igual que el original.

---

## Configuración previa (todos hacen esto una sola vez)

Antes de empezar cada integrante debe:

```bash
# 1. Clonar el repositorio
git clone <URL-del-repo>
cd mi-api-flask-python

# 2. Crear el entorno virtual
python -m venv venv

# 3. Activarlo (Windows)
venv\Scripts\activate

# 4. Instalar Flask y las dependencias
#    ⚠️ Hacer esto DESPUÉS de que el Integrante 2 haya mergeado su rama a develop
#    y hayan hecho: git pull origin develop
pip install -r requirements.txt

# 5. Confirmar que están en develop antes de crear su rama
git checkout develop
```

> **Nota:** Si el `requirements.txt` todavía no existe en el repo (Integrante 2 aún no mergeó),
> pueden instalar Flask manualmente mientras tanto:
> ```bash
> pip install Flask flask-cors python-dotenv pytest
> ```

---

## Rama base del proyecto

El **Integrante 1 (Lead)** debe crear las ramas permanentes en el repo **antes** de que los demás empiecen:

```bash
# En main (ya existe)
git checkout main

# Crear develop
git checkout -b develop
git push origin develop
```

### ⚙️ Cambiar la rama por defecto a `develop` en GitHub

Después de hacer el push de develop, el Integrante 1 debe ir a GitHub y cambiar la rama por defecto:

1. Abrir el repositorio en GitHub
2. Ir a **Settings** (pestaña de configuración del repo)
3. En el menú izquierdo, clic en **Branches**
4. En **Default branch**, clic en el ícono de lápiz ✏️ (o botón **Switch to another branch**)
5. Seleccionar `develop` en el desplegable
6. Clic en **Update** y confirmar el cambio

> Esto hace que cuando alguien clone el repo o abra un Pull Request, `develop` sea la rama base por defecto.

A partir de aquí, **todos los demás parten de `develop`**.

---

---

# 👤 INTEGRANTE 1 — Lead / Release Manager

**Rama:** trabaja directo en `develop` y `main`  
**Responsabilidad:** estructura inicial del repo, merges finales, tag de versión

### Qué debe hacer

**Paso 1 — Crear la estructura de carpetas vacías**
```
mi-api-flask-python/
├── app/
│   ├── routes/
│   └── utils/
├── tests/
└── docs/
```

**Paso 2 — Crear el `.gitignore`**

Contenido del archivo:
```
venv/
env/
.venv/
.env
__pycache__/
*.pyc
.pytest_cache/
.coverage
.vscode/
.idea/
.DS_Store
Thumbs.db
```

**Paso 3 — Crear el `.env.example`**
```
PORT=5000
FLASK_ENV=development
```

**Paso 4 — Commits que debe hacer**
```bash
git add .gitignore .env.example
git commit -m "chore: initial project setup and folder structure"
git push origin develop
```

**Paso 5 — Al final (cuando todos terminaron)**

Crear la rama de release, hacer el merge a main y crear el tag:
```bash
git checkout develop
git checkout -b release/v1.0.0
git checkout main
git merge release/v1.0.0 --no-ff
git tag -a v1.0.0 -m "release: initial stable version of the Flask API"
git push origin main --tags
```

---

---

# 👤 INTEGRANTE 2 — Setup del entorno Flask

**Rama:** `feature/setup-entorno`  
**Responsabilidad:** instalar dependencias, crear la app Flask, punto de entrada

### Qué debe hacer

```bash
# Crear su rama desde develop
git checkout develop
git checkout -b feature/setup-entorno
```

**Archivos que debe crear:**

**1. `requirements.txt`**
```
Flask==3.0.3
flask-cors==4.0.1
python-dotenv==1.0.1
pytest==8.2.2
```

**2. `run.py`** (punto de entrada, equivale al `index.ts`)
```python
from app import create_app
import os

app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    app.run(host='0.0.0.0', port=port, debug=debug)
```

**3. `app/__init__.py`** (factory de Flask, equivale al `index.ts` completo)
```python
from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = Flask(__name__)
    CORS(app)

    from app.routes.users import users_bp
    app.register_blueprint(users_bp, url_prefix='/api/users')

    @app.route('/')
    def index():
        return jsonify({
            "message": "¡Bienvenido a la API REST!",
            "version": "1.0.0"
        })

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"error": "Ruta no encontrada"}), 404

    return app
```

**4. `app/__init_placeholder__.py`** — crear archivos vacíos de paquete:
- `app/routes/__init__.py` → vacío
- `app/utils/__init__.py` → vacío
- `tests/__init__.py` → vacío

**Commits que debe hacer:**
```bash
git add requirements.txt
git commit -m "chore: add requirements.txt with Flask dependencies"

git add run.py
git commit -m "feat(app): add run.py as application entry point"

git add app/
git commit -m "feat(app): create Flask app factory with CORS and dotenv support"

git push origin feature/setup-entorno
```

**Al terminar → abrir Pull Request a `develop`**

---

---

# 👤 INTEGRANTE 3 — Endpoints GET y POST

**Rama:** `feature/endpoint-get-post`  
**Responsabilidad:** modelo de datos, helper de respuestas, y los endpoints GET y POST

### Esperar a que el Integrante 2 haga merge a develop, luego:

```bash
git checkout develop
git pull origin develop
git checkout -b feature/endpoint-get-post
```

**Archivos que debe crear:**

**1. `app/models.py`** (equivale al `User.ts`)
```python
from typing import List, Dict, Any

# Base de datos en memoria — igual que el User.ts original
users: List[Dict[str, Any]] = [
    {"id": 1, "name": "Juan Garcia",  "email": "juangarcia@gmail.com",  "age": 28},
    {"id": 2, "name": "Maria López",  "email": "marialopez@gmail.com",  "age": 22},
    {"id": 3, "name": "Juan Méndez",  "email": "juanmendez@gmail.com",  "age": 25},
]
```

**2. `app/utils/responses.py`** (helper para respuestas JSON)
```python
from flask import jsonify

def success_response(data, message=None, status_code=200, extra=None):
    response = {"success": True, "data": data}
    if message:
        response["message"] = message
    if extra:
        response.update(extra)
    return jsonify(response), status_code

def error_response(message, status_code=400):
    return jsonify({"success": False, "error": message}), status_code
```

**3. `app/routes/users.py`** — solo las rutas GET y POST:
```python
from flask import Blueprint, request
from app.models import users
from app.utils.responses import success_response, error_response

users_bp = Blueprint('users', __name__)

# GET /api/users — lista todos los usuarios
@users_bp.route('/', methods=['GET'])
def get_all_users():
    return success_response(data=users, extra={"total": len(users)})

# GET /api/users/<id> — obtiene usuario por ID
@users_bp.route('/<int:id>', methods=['GET'])
def get_user_by_id(id):
    user = next((u for u in users if u['id'] == id), None)
    if not user:
        return error_response(f'Usuario con ID {id} no encontrado', 404)
    return success_response(data=user)

# POST /api/users — crea un usuario nuevo
@users_bp.route('/', methods=['POST'])
def create_user():
    body = request.get_json()
    if not body:
        return error_response('Los campos name, email, age son obligatorios', 400)
    name  = body.get('name')
    email = body.get('email')
    age   = body.get('age')
    if not name or not email or not age:
        return error_response('Los campos name, email, age son obligatorios', 400)
    new_id = max((u['id'] for u in users), default=0) + 1
    new_user = {"id": new_id, "name": name, "email": email, "age": age}
    users.append(new_user)
    return success_response(data=new_user, message='Usuario Creado exitosamente', status_code=201)
```

**Commits que debe hacer:**
```bash
git add app/models.py
git commit -m "feat(users): add User model with in-memory data store"

git add app/utils/responses.py
git commit -m "feat(utils): add standardized JSON response helpers"

git add app/routes/users.py
git commit -m "feat(users): add GET /users endpoint - list all users"

git add app/routes/users.py
git commit -m "feat(users): add GET /users/:id endpoint - get user by id"

git add app/routes/users.py
git commit -m "feat(users): add POST /users endpoint with auto-increment id"

git push origin feature/endpoint-get-post
```

**Al terminar → abrir Pull Request a `develop`**

---

---

# 👤 INTEGRANTE 4 — Endpoints PUT y DELETE

**Rama:** `feature/endpoint-put-delete`  
**Responsabilidad:** agregar los endpoints PUT y DELETE al archivo de rutas

### Esperar a que el Integrante 3 haga merge a develop, luego:

```bash
git checkout develop
git pull origin develop
git checkout -b feature/endpoint-put-delete
```

**Qué debe hacer:**

Agregar al final del archivo `app/routes/users.py` (que ya existe):

```python
# PUT /api/users/<id> — actualiza usuario existente (parcial)
@users_bp.route('/<int:id>', methods=['PUT'])
def update_user(id):
    body = request.get_json()
    user = next((u for u in users if u['id'] == id), None)
    if not user:
        # Nota: el original Node.js devuelve 400 (no 404) en este caso
        return error_response(f'Usuario con ID {id} no encontrado', 400)
    if body.get('name'):
        user['name']  = body['name']
    if body.get('email'):
        user['email'] = body['email']
    if body.get('age'):
        user['age']   = body['age']
    return success_response(data=user, message='Usuario Actualizado exitosamente')

# DELETE /api/users/<id> — elimina un usuario
@users_bp.route('/<int:id>', methods=['DELETE'])
def delete_user(id):
    index = next((i for i, u in enumerate(users) if u['id'] == id), -1)
    if index == -1:
        return error_response(f'Usuario con ID {id} no encontrado', 404)
    deleted_user = users.pop(index)
    return success_response(data=deleted_user, message='Usuario eliminado exitosamente')
```

**Commits que debe hacer:**
```bash
git add app/routes/users.py
git commit -m "feat(users): add PUT /users/:id endpoint - update user"

git add app/routes/users.py
git commit -m "feat(users): add DELETE /users/:id endpoint - remove user"

git add app/routes/users.py
git commit -m "fix(users): return 404 on DELETE and 400 on PUT for nonexistent user"

git push origin feature/endpoint-put-delete
```

**Al terminar → abrir Pull Request a `develop`**

---

---

# 👤 INTEGRANTE 5 — Documentación y Tests

**Rama:** `feature/docs-tests`  
**Responsabilidad:** README, CHANGELOG, tests con pytest, colección de Postman

### Puede trabajar en paralelo con los demás. Al terminar espera a que todo esté en develop.

```bash
git checkout develop
git pull origin develop
git checkout -b feature/docs-tests
```

**Archivos que debe crear:**

**1. `README.md`** — debe incluir:
- Descripción del proyecto
- Tabla de tecnologías (Flask = Express, pytest = Jest, etc.)
- Pasos de instalación (clonar, crear venv, instalar deps, copiar .env)
- Cómo correr el servidor (`python run.py`)
- Tabla de endpoints con método, ruta y descripción
- Ejemplos de request y response para cada endpoint
- Cómo correr los tests (`pytest tests/ -v`)
- Sección de Git Flow y commits semánticos

**2. `CHANGELOG.md`** — debe incluir:
```markdown
# Changelog

## [1.0.0] - 2026-04-24

### Added
- feat(app): Flask app factory con CORS y dotenv
- feat(users): GET /api/users — lista usuarios con campo total
- feat(users): GET /api/users/:id — obtiene usuario por ID
- feat(users): POST /api/users — crea usuario con ID autoincremental
- feat(users): PUT /api/users/:id — actualización parcial de usuario
- feat(users): DELETE /api/users/:id — elimina y retorna el usuario
- test(users): suite de tests con pytest
- docs: README y CHANGELOG
- chore: requirements.txt, .gitignore, .env.example
```

**3. `tests/test_users.py`** — casos de prueba mínimos requeridos:

| Test | Qué verifica |
|---|---|
| `test_get_all_returns_200` | GET / retorna status 200 |
| `test_get_all_has_total` | GET / incluye campo `total` |
| `test_get_by_id_returns_200` | GET /1 retorna 200 |
| `test_get_by_id_not_found` | GET /999 retorna 404 |
| `test_create_user_returns_201` | POST retorna 201 |
| `test_create_user_increments_id` | El ID nuevo es max+1 |
| `test_create_user_missing_fields` | POST sin campos retorna 400 |
| `test_update_user_returns_200` | PUT retorna 200 |
| `test_update_user_not_found` | PUT /999 retorna 400 |
| `test_delete_user_returns_200` | DELETE retorna 200 |
| `test_delete_user_not_found` | DELETE /999 retorna 404 |
| `test_delete_removes_from_list` | Tras DELETE el GET no lo incluye |

**4. `docs/postman_collection.json`** — exportar desde Postman después de probar todos los endpoints manualmente. Debe incluir los 5 requests con ejemplos de respuesta guardados.

**Commits que debe hacer:**
```bash
git add tests/
git commit -m "test(users): add pytest suite covering all CRUD endpoints"

git add README.md
git commit -m "docs: add README with setup, endpoints and Git Flow guide"

git add CHANGELOG.md
git commit -m "docs: add CHANGELOG with v1.0.0 release notes"

git add docs/
git commit -m "docs(postman): add Postman collection with all endpoint examples"

git push origin feature/docs-tests
```

**Al terminar → abrir Pull Request a `develop`**

---

---

## Orden recomendado de merges a develop

```
Integrante 1 → crea estructura base (primero)
Integrante 2 → merge feature/setup-entorno
Integrante 3 → merge feature/endpoint-get-post
Integrante 4 → merge feature/endpoint-put-delete
Integrante 5 → merge feature/docs-tests (puede ir en paralelo con 3 y 4)
Integrante 1 → crea release/v1.0.0 → merge a main → tag v1.0.0
```

---

## Resumen de commits por integrante

| Integrante | Commits esperados |
|---|---|
| 1 | `chore: initial project setup` + merge + tag |
| 2 | `chore: requirements` + `feat: run.py` + `feat: app factory` |
| 3 | `feat: User model` + `feat: response helpers` + `feat: GET all` + `feat: GET by id` + `feat: POST` |
| 4 | `feat: PUT` + `feat: DELETE` + `fix: status codes` |
| 5 | `test: pytest suite` + `docs: README` + `docs: CHANGELOG` + `docs: postman` |
