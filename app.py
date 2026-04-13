from flask import Flask, jsonify
from routes.items import items_bp
import os
from dotenv import load_dotenv

# Carga las variables del archivo .env
load_dotenv()

def create_app():
    """
    Factory function: crea y configura la aplicación Flask.
    Este patrón facilita crear múltiples instancias para testing.
    """
    app = Flask(__name__)

    # Registrar los blueprints (grupos de rutas)
    app.register_blueprint(items_bp)

    # Manejador global de errores 404
    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"error": "Recurso no encontrado"}), 404

    # Manejador global de errores 500
    @app.errorhandler(500)
    def server_error(e):
        return jsonify({"error": "Error interno del servidor"}), 500

    @app.route('/health')
    def health():
        return jsonify({"status": "ok"}), 200

    return app


app = create_app()

if __name__ == '__main__':
    debug = os.getenv("DEBUG", "true").lower() == "true"
    app.run(debug=debug, host="0.0.0.0", port=5000)
