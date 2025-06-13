import openai
import json
import re
from typing import Tuple, Optional, Dict

class LLM():
    def __init__(self, api_key: str):
        openai.api_key = api_key
        openai.api_base = "https://api.deepseek.com/v1"
        self.knowledge_base = self._load_knowledge_base()
        
    def _load_knowledge_base(self) -> Dict:
        #Carga y normaliza la base de conocimiento
        try:
            with open("../data/faqs.json", "r", encoding="utf-8") as file:
                kb = json.load(file)
                return {self._normalize_text(k): v for k, v in kb.items()}
        except Exception as e:
            print(f"Error cargando KB: {str(e)}")
            return {}

    def _normalize_text(self, text: str) -> str:
        #Normaliza texto para comparación
        text = text.lower().strip()
        replacements = {'á':'a', 'é':'e', 'í':'i', 'ó':'o', 'ú':'u', '¿':'', '?':''}
        for old, new in replacements.items():
            text = text.replace(old, new)
        return text

    def process_request(self, text: str) -> Tuple[str, Optional[Dict]]:
        """
        Procesa la solicitud y determina si es:
        - Pedido (retorna 'order', datos_del_pedido)
        - Información (retorna 'info', None)
        """
        normalized_text = self._normalize_text(text)
        
        # 1. Primero verificar si es un pedido
        order_keywords = ['pedido', 'orden', 'quiero comprar', 'deseo ordenar']
        if any(keyword in normalized_text for keyword in order_keywords):
            return self._process_order(text)
        
        # 2. Si no es pedido, es solicitud de información
        return 'info', None

    def _process_order(self, text: str) -> Tuple[str, Dict]:
        #Extrae información del pedido 
        try:
            response = openai.ChatCompletion.create(
                model="deepseek-chat",
                
                messages=[
                    {
                        "role": "system", 
                        "content": "vas a estraer información de un pedido de una panadería. y lo entregarás en texto plano, ejemplo: {'items': '2 panes y 1 café', 'address': 'Calle Falsa 123', 'customer_name': 'Juan Pérez'}"
                    },
                    {"role": "user", "content": text},
                ],
                functions=[{
                    "name": "create_order",
                    "description": "Crear nuevo pedido",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "items": {"type": "string", "description": "Productos solicitados, ej: '2 panes y 1 café'"},
                            "address": {"type": "string", "description": "Dirección de entrega"},
                            "customer_name": {"type": "string", "description": "Nombre del cliente si se menciona"}
                        },
                        "required": ["items", "address"]
                    }
                }],
                function_call="auto",
               
            )
            print(f"text: {text}")
            message = response.choices[0].message
            print(f"Respuesta de API: {message}")
            cleaned_content = openai.ChatCompletion.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": "Limpia el texto y extrae los datos del pedido en formato JSON, unicamente el JSON, sin explicaciones adicionales"},
                    {"role": "user", "content": message.content}
                ]
            )
            print(f"Contenido limpiado: {cleaned_content.choices[0].message.content}")

            cleaned_content = cleaned_content.choices[0].message.content
            cleaned_content = re.sub(r'```json\s*', '', cleaned_content)
            cleaned_content = re.sub(r'```', '', cleaned_content)
            cleaned_content = cleaned_content.strip()
            print(f"Contenido limpiado final: {cleaned_content}")
            args = json.loads(cleaned_content)
            
            return 'order', args
            
                
        except Exception as e:
            print(f"Error en API: {str(e)}")


    def get_info_response(self, text: str) -> str:
        normalized_text = self._normalize_text(text)
        
        # 1. Buscar en knowledge base
        for question, answer in self.knowledge_base.items():
            if question in normalized_text:
                return answer
        
        # 2. Respuesta genérica si no está en KB
        return "Por favor, consulta información específica como 'horario', 'ubicación',  'productos' o realiza un pedido."