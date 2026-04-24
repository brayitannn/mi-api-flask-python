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
