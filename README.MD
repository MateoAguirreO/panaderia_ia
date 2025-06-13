PRUEBA TÉCNICA
• Caso:
Requerimos un agente basado en AI que pueda gestionar requerimientos
básicos relacionados con una panadería que tiene servicio de domicilios y canales de
atención escritos (WPP, Correo, Teams) para recibir los mismos.
• Necesidades:

- Crear una KDB (a su consideración) que contenga FAQs relacionadas con la
  panadería.
- Desarrollar un agente de AI que se conecte a la KDB creada y pueda entregar
  información (según se le consulte) relacionada con la panadería y alojada en la
  KDB.
- Crear una BBDD de pedidos.
- Si se le indica al agente AI que se requiere un pedido, aquel deberá crear el pedido,
  registrarlo en la BBDD de pedidos y confirmar al usuario que fue creado el pedido y
  confirmar el número de orden (el número puede ser aleatorio, pero debe quedar
  registrado igualmente en la BBDD).
- Grabar en una BBDD las respuestas y consultas brindadas y hechas al agente
  respectivamente (un registro de la transacción/conversación).
  • Libertades (a consideración propia):
- Los canales de entrada (las consultas) hacia el agente pueden ser escritos o voz.
- El canal de salida (las respuestas) del agente puede ser a través de audio o texto.
- Usar el LLM de su preferencia (se sugiere usar uno de uso gratis o prueba: Meta,
  deepseek, etc.)
- El funcionamiento/ejercicio práctico de la aplicación (interacción entre humano y
  agente) se puede mostrar por el medio que se desee: consola, front web, una
  llamada, etc.
  • Observaciones:
- No es necesario que nos envíes el código de la aplicación. Sólo haz un video que
  muestre el funcionamiento natural de la misma, su arquitectura y una breve
  explicación del código.
- Por favor compartir el video a los siguientes correos: hamilton.loaiza@arus.com.co
  y luisa.cubides@arus.com.co.
- Cuando llegue el momento de ver los resultados de tu prueba técnica,
  requeriremos que nos muestres en tiempo real la aplicación, su funcionamiento, su
  estructura y/o arquitectura.

Ejecución
flask --app app run --debug

1. Arquitectura General
2. Componentes Principales
   Frontend (Cliente)
   Tecnologías: HTML5, CSS3, JavaScript + Bootstrap 5

   

Características:

    Interfaz basada en componentes (botones, tarjetas)

    Comunicación asíncrona con el backend 

    Gestión de estados básica (grabando/en espera)

Backend (Servidor)
Tecnologías: Python + Flask 


Módulos clave:

    app.py: Router principal

    llm.py: "Caso de uso" (lógica de negocio)

    transcriber.py: Adaptador para STT

    tts.py: Adaptador para texto-a-voz

    order_system.py: "gestiona la persistencia" (gestión de datos)


    DeepSeek API-----Procesamiento de lenguaje
    ElevenLabs-------Text-to-Speech
    Bootstrap--------Estilos frontend
    Font Awesome-----Iconos
    ASSEMBLYAI------- Voz a texto
