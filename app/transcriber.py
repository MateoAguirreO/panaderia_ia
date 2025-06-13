import os
import assemblyai as aai

class Transcriber:
    def __init__(self):
        aai.settings.api_key = os.getenv('ASSEMBLYAI_API_KEY')
        self.config = aai.TranscriptionConfig(
            speech_model=aai.SpeechModel.best,
            language_code="es"  # Configuración clave para español
        )
        
    def transcribe(self, audio):
        #Transcribe audio a texto en español
        try:
            # Guardar audio temporalmente
            audio_path = "temp_audio.mp3"
            audio.save(audio_path)
            
            # Transcribir con configuración en español
            transcriber = aai.Transcriber(config=self.config)
            transcript = transcriber.transcribe(audio_path)
            
            # Eliminar archivo temporal
            if os.path.exists(audio_path):
                os.remove(audio_path)
            
            if transcript.status == "error":
                raise RuntimeError(f"Error en transcripción: {transcript.error}")
                

            return transcript.text
            
        except Exception as e:
            print(f"Error en transcripción: {str(e)}")
            raise RuntimeError("No pude transcribir el audio") from e