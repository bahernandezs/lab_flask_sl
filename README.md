# lab_flask_sl
Laboratorio para crear un api y subirlo a aws.

HTTP Request
     ↓
[ routes/items.py ]   ← Define los endpoints (Blueprint)
     ↓
[ services/item_service.py ]   ← Lógica de negocio
     ↓
[ repositories/item_repo.py ]  ← Acceso a datos (memoria o DynamoDB)


Tabla de dynamo

aws dynamodb create-table --table-name disputas --attribute-definitions AttributeName=disputaId,AttributeType=S --key-schema AttributeName=disputaId,KeyType=HASH --billing-mode PAY_PER_REQUEST --region us-east-1