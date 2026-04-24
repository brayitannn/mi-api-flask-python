from flask import Blueprint, request
from app.models import users
from app.utils.responses import success_response, error_response

users_bp = Blueprint('users', __name__)

@users_bp.route('/', methods=['GET'])
def get_all_users():
    return success_response(data=users, extra={"total": len(users)})
