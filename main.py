import os
from openai import OpenAI
from dotenv import load_dotenv
from agent import Agent

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

# Inicializamos nuestro agente autónomo
agent = Agent(client=client, model="openrouter/free")

print("🤖 Agente autónomo activo. Escribe 'salir' para terminar.\n")

while True:
    user_input = input("Tú: ").strip()

    if not user_input:
        continue
    if user_input.lower() in ("salir", "exit", "bye"):
        print("Hasta pronto.")
        break

    # El agente procesa toda la cadena de pensamiento internamente y nos da el resultado listo
    respuesta_final = agent.run(user_input)
    
    print(f"Asistente: {respuesta_final}\n")