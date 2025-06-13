from pymongo import MongoClient
from datetime import datetime
import os
from dotenv import load_dotenv
import random

load_dotenv()

class OrderSystem:
    def __init__(self):
        self.client = MongoClient(os.getenv('MONGO_CONNECTION_STRING'))
        self.db = self.client.panaderia
        self.orders = self.db.pedidos
        self.conversations = self.db.logs_conversaciones

    def create_order(self, items: str, address: str, customer_name: str = None) -> dict:
        #Crea un nuevo pedido en MongoDB
        order_data = {
            "order_id": random.randint(1000, 9999),
            "items": items,
            "address": address,
            "customer_name": customer_name,
            "status": "pendiente",
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }
        print(f"Creando pedido: {order_data}")
        
        result = self.orders.insert_one(order_data)
        return {
            **order_data,
            "mongo_id": str(result.inserted_id)
        }

    def get_order(self, order_id: int) -> dict:
        #Obtiene un pedido por su ID
        order = self.orders.find_one({"order_id": order_id})
        if order:
            order["_id"] = str(order["_id"])  # Convertir ObjectId a string
        return order

    def log_conversation(self, query: str, response: str):
        #Registra una conversación en MongoDB
        self.conversations.insert_one({
            "query": query,
            "response": response,
            "timestamp": datetime.now()
        })

    def close(self):
        #Cierra la conexión con MongoDB
        self.client.close()