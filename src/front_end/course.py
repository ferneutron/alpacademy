import gradio as gr 
import json
import random

# Cargar el JSON
with open('contenido.json', 'r', encoding='utf-8') as file:
    curso_data = json.load(file)

semanas = list(curso_data.keys())
semana_actual = 0

def mostrar_semana(semana_index):
    semana = semanas[semana_index]
    contenido = curso_data[semana]['material']
    clases = [item for item, tipo in zip(contenido, curso_data[semana]['tipo']) if tipo == 'clase']
    return "\n\n".join(clases), f"## {semana}", obtener_texto_boton(semana_index)

def obtener_texto_boton(semana_index):
    siguiente_index = (semana_index + 1) % len(semanas)
    return f"Avanza a la {semanas[siguiente_index]}"

def siguiente_semana():
    global semana_actual
    semana_actual = (semana_actual + 1) % len(semanas)
    return mostrar_semana(semana_actual)

def responder_pregunta(mensaje, historial):
    respuestas = [
        "Interesante pregunta. ¿Podrías elaborar un poco más?",
        "Esa es una buena observación. ¿Qué te hace pensar eso?",
        "Entiendo tu punto. ¿Has considerado también...?",
        "Gracias por tu pregunta. Déjame pensar en eso por un momento.",
        "Esa es una perspectiva interesante. ¿Cómo llegaste a esa conclusión?",
    ]
    respuesta = random.choice(respuestas)
    historial.append((mensaje, respuesta))
    return "", historial

css = """
h1 {
    text-align: center;
    display:block;
}
"""

if __name__ == '__main__':
    demo = gr.Blocks(theme=gr.themes.Soft(), css=css)
    
    with demo:
        gr.Markdown(f"""# Alpacademy """)
        semana_header = gr.Markdown()
        gr.Markdown(f""" """)

        with gr.Column():
            gr.Markdown(f"""-------------------------------------------- """)
            contenido_semana = gr.Markdown()
            gr.Markdown(f"""-------------------------------------------- """)
            with gr.Row():
                with gr.Column():
                    gr.Markdown()
                with gr.Column():
                    siguiente_btn = gr.Button(interactive=True)
                with gr.Column():
                    gr.Markdown()

            # Chatbot
            chatbot = gr.Chatbot(label="Conversación con el Agente")
            mensaje = gr.Textbox(label="Tu pregunta", placeholder="Escribe tu pregunta aquí...", autofocus=True)
            enviar_btn = gr.Button("Enviar pregunta")

        # Inicializar con la primera semana
        contenido_inicial, header_inicial, texto_boton_inicial = mostrar_semana(0)
        contenido_semana.value = contenido_inicial
        semana_header.value = header_inicial
        siguiente_btn.value = texto_boton_inicial

        siguiente_btn.click(siguiente_semana, outputs=[contenido_semana, semana_header, siguiente_btn])
        enviar_btn.click(responder_pregunta, inputs=[mensaje, chatbot], outputs=[mensaje, chatbot])

    demo.launch(debug=True, server_name="127.0.0.1", server_port=8080)