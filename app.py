from flask import Flask, jsonify
import os
from datetime import datetime

# Flask(__name__) crea la aplicación usando el nombre del módulo actual
app = Flask(__name__)

@app.route('/')
def hello_world():
    """Endpoint principal — devuelve un saludo con metadata útil."""
    return jsonify({
        "message": "¡Hola, Killua! Flask está funcionando.",
        "timestamp": datetime.utcnow().isoformat(),
        "environment": os.getenv("ENVIRONMENT", "local"),
        "version": "1.0.0"
    })

@app.route('/health')
def health():
    """
    Health check — endpoint estándar en cualquier API de producción.
    Los balanceadores de carga y sistemas de monitoreo usan este endpoint
    para saber si el servicio está vivo.
    """
    return jsonify({"status": "ok", "service": "flask-helloworld-lab_ls"}), 200

# Ejecutar solo cuando el script se corre directamente (no cuando se importa)
if __name__ == '__main__':
    # debug=True recarga automáticamente al guardar cambios (solo para desarrollo)
    debug_mode = os.getenv("DEBUG", "true").lower() == "true"
    app.run(debug=debug_mode, host="0.0.0.0", port=5000)
