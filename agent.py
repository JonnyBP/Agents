import os
import json


class Agent:
    def __init__(self, client, model):
        self.client = client
        self.model = model
        self.setup_tools()
        self.messages = [
                {"role": "system", "content":"Eres un asistente útil que habla español y eres muy conciso con tus respuestas"}
        ]

    def setup_tools(self):

        # 1. MAPEO DINÁMICO: Vincula el nombre de la API con tu función de Python
        self.available_tools = {
            "list_files_in_dir": self.list_files_in_dir,
            "read_file": self.read_file
        }

        self.tools = [
            {
                "type": "function",
                "function": {
                    "name": "list_files_in_dir",
                    "description": "Lista los archivos que existen en un directorio dado (por defecto es el directorio actual)",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "directory": {
                                "type": "string",
                                "description": "Directorio para listar (opcional). Por defecto es el directorio actual"
                            }
                        },
                        "required": []
                    }
                }
            },
        ]

    def list_files_in_dir(self, directory = "."):
        # 1. Definición de la función local
        print("\n  ⚙️ [Ejecutando herramienta local]: list_files_in_dir")

        try:
            files = os.listdir(directory)
            return {"files": files}
        except Exception as e:
            return {"error": str(e)}
            

    def read_file(self, path):
        pass

    def edit_file(self, path, prev_text, new_text):
        pass


    def run(self, user_prompt):
        
        """
        Recibe el prompt del usuario y ejecuta iterativamente todas las herramientas 
        que el modelo necesite hasta llegar a una respuesta final de texto.
        """
        self.messages.append({"role": "user", "content": user_prompt})
        
        # Bucle de inferencia autónomo
        while True:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=self.messages,
                tools=self.tools
            )
            
            assistant_message = response.choices[0].message
            self.messages.append(assistant_message)
            
            # Caso A: El modelo pide ejecutar herramientas (una o varias en paralelo)
            if assistant_message.tool_calls:
                for tool_call in assistant_message.tool_calls:
                    fn_name = tool_call.function.name
                    fn_args = json.loads(tool_call.function.arguments)
                    
                    print(f"  🤖 El modelo solicita: '{fn_name}' con {fn_args}")
                    
                    # Ejecutar de forma dinámica usando nuestro diccionario
                    if fn_name in self.available_tools:
                        result = self.available_tools[fn_name](**fn_args)
                    else:
                        result = {"error": f"Herramienta '{fn_name}' no disponible."}
                        
                    # Insertar el resultado de la herramienta en el historial
                    self.messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "name": fn_name,
                        "content": json.dumps(result)
                    })
                
                # El bucle continúa: vuelve al inicio de 'while' para enviar los resultados al modelo
                continue
            
            # Caso B: El modelo no necesita más herramientas y responde al usuario
            if assistant_message.content:
                return assistant_message.content