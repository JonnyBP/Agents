import os
from openai import OpenAI
from dotenv import load_dotenv
from agent import Agent

# Carga las variables del archivo .env
load_dotenv()

# Configuramos el cliente para que apunte a OpenRouter
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

messages = [
    {"role": "system", "content":"Eres un asistente útil que habla español y eres muy conciso con tus respuestas"}
]

while True:

    user_input = input("Tú: ").strip()

    #Validaciones
    if not user_input:
        continue
    
    if user_input.lower() in ("salir", "exit", "bye"):
        print("Hasta pronto")
        break

    messages.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        # En OpenRouter es buena práctica anteponer el proveedor o usar openrouter/free (Enrutador gratuito)
        model="openrouter/free", 
        messages = messages
    )

    # Para acceder al texto de la respuesta en el SDK actual
    assitant_reply = response.choices[0].message.content
    messages.append({"role": "assistant", "content": assitant_reply})
    print(f"Asistente: {assitant_reply}")