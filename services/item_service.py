import os
from repositories.memory_repo import MemoryItemRepository
from repositories.dynamo_repo import DynamoItemRepository
from typing import Optional





class ItemService:
    """
    Contiene la lógica de negocio para items.
    No sabe si los datos vienen de memoria o DynamoDB —
    eso es responsabilidad del repositorio.
    """
    def __init__(self, repository=None):
        if repository:
            self.repo = repository
        elif os.getenv("USE_DYNAMO", "false").lower() == "true":
            self.repo = DynamoItemRepository()
        else:
            self.repo = MemoryItemRepository()


    def create(self, data: dict) -> tuple[dict, int]:
        """Crea un item. Retorna (item, http_status_code)."""
        if not data.get("title"):
            return {"error": "El campo 'title' es obligatorio"}, 400

        title = data["title"].strip()
        if len(title) == 0:
            return {"error": "El título no puede estar vacío"}, 400

        description = data.get("description", "")
        item = self.repo.create(name=title, description=description)
        return item, 201

    def get_all(self) -> tuple[list, int]:
        return self.repo.find_all(), 200

    def get_by_id(self, item_id: str) -> tuple[dict, int]:
        item = self.repo.find_by_id(item_id)
        if not item:
            return {"error": f"Item con id '{item_id}' no encontrado"}, 404
        return item, 200

    def update(self, item_id: str, data: dict) -> tuple[dict, int]:
        if not self.repo.find_by_id(item_id):
            return {"error": f"Item con id '{item_id}' no encontrado"}, 404
        updated = self.repo.update(item_id, data)
        return updated, 200

    def delete(self, item_id: str) -> tuple[dict, int]:
        deleted = self.repo.delete(item_id)
        if not deleted:
            return {"error": f"Item con id '{item_id}' no encontrado"}, 404
        return {"message": "Item eliminado correctamente"}, 200
