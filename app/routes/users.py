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
