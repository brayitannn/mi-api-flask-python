from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.json.sort_keys = False  # Preservar el orden de inserción del diccionario

    # Note: users_bp will be created by Member 3, 
    # but we need to register it here as per instructions
    try:
        from app.routes.users import users_bp
        app.register_blueprint(users_bp, url_prefix='/api/users')
    except ImportError:
        # Member 3 hasn't created the routes yet, this is expected
        pass

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
