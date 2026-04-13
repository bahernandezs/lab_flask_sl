import boto3
import uuid
import os
from typing import Optional


class DynamoItemRepository:
    """
    Repositorio de items usando AWS DynamoDB.
    Los datos persisten aunque el servidor se reinicie.
    """

    def __init__(self):
        self.dynamodb = boto3.resource(
            'dynamodb',
            region_name=os.getenv("AWS_REGION", "us-east-1")
        )
        self.table = self.dynamodb.Table(
            os.getenv("DYNAMO_TABLE_NAME", "Tasks")
        )

    def create(self, name: str, description: str = "") -> dict:
        item = {
            "disputaId": str(uuid.uuid4()),
            "title": name,
            "description": description,
            "completed": False
        }
        self.table.put_item(Item=item)
        return item

    def find_all(self) -> list:
        # scan() lee toda la tabla — OK para dev, usa Query en producción con datos grandes
        response = self.table.scan()
        return response.get("Items", [])

    def find_by_id(self, item_id: str) -> Optional[dict]:
        response = self.table.get_item(Key={"task_id": item_id})
        return response.get("Item")  # None si no existe

    def update(self, item_id: str, data: dict) -> Optional[dict]:
        if not self.find_by_id(item_id):
            return None

        # Construimos la expresión de actualización dinámicamente
        update_expr = "SET " + ", ".join([f"#{k} = :{k}" for k in data.keys()])
        expr_names = {f"#{k}": k for k in data.keys()}
        expr_values = {f":{k}": v for k, v in data.items()}

        response = self.table.update_item(
            Key={"task_id": item_id},
            UpdateExpression=update_expr,
            ExpressionAttributeNames=expr_names,
            ExpressionAttributeValues=expr_values,
            ReturnValues="ALL_NEW"
        )
        return response.get("Attributes")

    def delete(self, item_id: str) -> bool:
        if not self.find_by_id(item_id):
            return False
        self.table.delete_item(Key={"task_id": item_id})
        return True
