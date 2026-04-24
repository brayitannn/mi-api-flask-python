from flask import Blueprint, request
from app.models import users
from app.utils.responses import success_response, error_response

users_bp = Blueprint('users', __name__)

@users_bp.route('/', methods=['GET'])
def get_all_users():
    return success_response(data=users, extra={"total": len(users)})

@users_bp.route('/<int:id>', methods=['GET'])
def get_user_by_id(id):
    user = next((u for u in users if u['id'] == id), None)
    if not user:
        return error_response(f'Usuario con ID {id} no encontrado', 404)
    return success_response(data=user)

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
