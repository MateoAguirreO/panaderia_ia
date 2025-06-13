# app.py - Aplicación Flask para el sistema de pedidos por voz
import os
import time
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify
from transcriber import Transcriber
from llm import LLM
from tts import TTS
from order_system import OrderSystem
from contextlib import closing

# Configuración inicial
load_dotenv()
app = Flask(__name__)

# Cargar API keys
DEEPSEEK_API_KEY = os.getenv('DEEP_SEEK_API_KEY')
ELEVENLABS_KEY = os.getenv('ELEVENLABS_API_KEY')

@app.route("/")
def index():
    #Ruta principal que muestra la interfaz de grabación
    return render_template("recorder.html")

@app.route("/audio", methods=["POST"])
def audio():
    #Endpoint para procesar audio y generar respuestas
    try:
        # 1. Transcribir audio a texto
        audio_file = request.files.get("audio")
        if not audio_file:
            return jsonify({"error": "No se recibió audio"}), 400
            
        text = Transcriber().transcribe(audio_file)
        if not text:
            return jsonify({"error": "Error en transcripción"}), 400

        # 2. Procesar con LLM
        llm = LLM(api_key=DEEPSEEK_API_KEY)
        request_type, response_data = llm.process_request(text)
        
        # 3. Manejar los tipos de solicitud
        with closing(OrderSystem()) as order_system:
            if request_type == "order":
                # Validar datos mínimos
                if not response_data.get("items") or not response_data.get("address"):
                    final_response = "Por favor indica qué productos deseas y la dirección de entrega"
                    order_id = None
                else:
                    # Procesar pedido válido
                    order = order_system.create_order(
                        items=response_data["items"],
                        address=response_data["address"],
                        customer_name=response_data.get("customer_name", "")
                    )
                    final_response = (
                        f"Pedido {order['order_id']} confirmado. "
                        f"Entregaremos {order['items']} en {order['address']}. "
                        "¡Gracias por tu compra!"
                    )
                    order_id = order['order_id']
                
                # Registrar en logs
                order_system.log_conversation(text, final_response)
            elif request_type == "info":
                # Solicitud de información
                final_response = llm.get_info_response(text)
                order_id = None
                order_system.log_conversation(text, final_response)

            # 4. Generar audio de respuesta
            tts_file = TTS().process(final_response)
            time.sleep(3)
            return jsonify({
                "result": "success",
                "type": request_type,
                "text": final_response,
                "file": tts_file,
                "order_id": order_id
            })
            
    except Exception as e:
        print(f"Error en endpoint /audio: {str(e)}")
        return jsonify({
            "result": "error",
            "message": "Ocurrió un error. Por favor intenta nuevamente."
        }), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)