from flask import Blueprint, request, jsonify
from services.item_service import ItemService

# Blueprint agrupa todas las rutas de /tasks
items_bp = Blueprint('items', __name__, url_prefix='/tasks')
service = ItemService()


@items_bp.route('', methods=['POST'])
def create():
    """POST /tasks — Crear una nueva tarea."""
    data = request.get_json()

    # Validar que viene un body JSON
    if not data:
        return jsonify({"error": "Se esperaba un JSON en el body"}), 400

    result, status = service.create(data)
    return jsonify(result), status


@items_bp.route('', methods=['GET'])
def get_all():
    """GET /tasks — Obtener todas las tareas."""
    result, status = service.get_all()
    return jsonify(result), status


@items_bp.route('/<string:item_id>', methods=['GET'])
def get_by_id(item_id):
    """GET /tasks/<id> — Obtener una tarea por ID."""
    result, status = service.get_by_id(item_id)
    return jsonify(result), status


@items_bp.route('/<string:item_id>', methods=['PUT'])
def update(item_id):
    """PUT /tasks/<id> — Actualizar una tarea existente."""
    data = request.get_json()
    if not data:
        return jsonify({"error": "Se esperaba un JSON en el body"}), 400

    result, status = service.update(item_id, data)
    return jsonify(result), status


@items_bp.route('/<string:item_id>', methods=['DELETE'])
def delete(item_id):
    """DELETE /tasks/<id> — Eliminar una tarea."""
    result, status = service.delete(item_id)
    return jsonify(result), status
