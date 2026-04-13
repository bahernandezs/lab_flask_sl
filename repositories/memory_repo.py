from typing import Optional
import uuid


class MemoryItemRepository:
    """
    Repositorio de items en memoria.
    Los datos se pierden al reiniciar el servidor.
    Ideal para desarrollo y pruebas.
    """

    def __init__(self):
        # Usamos un diccionario para acceso O(1) por ID
        self._storage: dict = {}

    def create(self, name: str, description: str = "") -> dict:
        item_id = str(uuid.uuid4())  # UUID garantiza unicidad
        item = {
            "id": item_id,
            "title": name,
            "description": description,
            "completed": False
        }
        self._storage[item_id] = item
        return item

    def find_all(self) -> list:
        return list(self._storage.values())

    def find_by_id(self, item_id: str) -> Optional[dict]:
        return self._storage.get(item_id)  # Retorna None si no existe

    def update(self, item_id: str, data: dict) -> Optional[dict]:
        item = self._storage.get(item_id)
        if not item:
            return None
        # Solo actualiza los campos que vengan en data
        item.update({k: v for k, v in data.items() if v is not None})
        return item

    def delete(self, item_id: str) -> bool:
        if item_id not in self._storage:
            return False
        del self._storage[item_id]
        return True
