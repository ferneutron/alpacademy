import gradio as gr 
import json
import random
from communicate_with_gradio import say_hello

# Cargar el contenido del curso desde un archivo JSON
with open('contenido.json', 'r', encoding='utf-8') as file:
    curso_data = json.load(file)

semanas = list(curso_data.keys())
semana_actual = 0
elemento_actual = 0


def mostrar_elemento(semana_index, elemento_index):
    """
    Muestra el contenido de un elemento específico (clase, preguntas o examen) de una semana.
    Devuelve el contenido, el encabezado, y los textos de los botones "Siguiente" y "Anterior".
    """
    semana = semanas[semana_index]
    contenido = curso_data[semana]['material'][elemento_index]
    tipo = curso_data[semana]['tipo'][elemento_index]

    if tipo == 'preguntas':
        preguntas_texto = ""
        for pregunta in contenido.values():
            preguntas_texto += f"- {pregunta['question']}\n"
        return preguntas_texto, f"## {semana} - Preguntas", obtener_texto_boton_siguiente(semana_index, elemento_index), obtener_texto_boton_anterior(semana_index, elemento_index)
    elif tipo == 'examen':
        preguntas_texto = ""
        for pregunta, respuesta in contenido.items():
            preguntas_texto += f"### {pregunta}\n{respuesta['question']}\n\n"
        return preguntas_texto, f"## {semana} - Examen", obtener_texto_boton_siguiente(semana_index, elemento_index), obtener_texto_boton_anterior(semana_index, elemento_index)
    else:
        return contenido, f"## {semana} - Clase {elemento_index + 1}", obtener_texto_boton_siguiente(semana_index, elemento_index), obtener_texto_boton_anterior(semana_index, elemento_index)


def saluda():
    """
    Función de saludo del chatbot.
    """
    return say_hello()

def obtener_texto_boton_siguiente(semana_index, elemento_index):
    """
    Obtiene el texto para el botón "Siguiente" según el elemento actual y la semana.
    """
    siguiente_elemento_index = (elemento_index + 1) % len(curso_data[semanas[semana_index]]['tipo'])
    if siguiente_elemento_index == 0:
        siguiente_semana_index = (semana_index + 1) % len(semanas)
        return f"Avanza a la {semanas[siguiente_semana_index]}"
    else:
        tipo_siguiente = curso_data[semanas[semana_index]]['tipo'][siguiente_elemento_index]
        if tipo_siguiente == 'preguntas':
            return "Avanza a las Preguntas"
        elif tipo_siguiente == 'examen':
            return "Avanza al Examen"
        else:
            return f"Avanza a la Clase {siguiente_elemento_index + 1}"

def obtener_texto_boton_anterior(semana_index, elemento_index):
    """
    Obtiene el texto para el botón "Anterior" según el elemento actual y la semana.
    """
    if elemento_index == 0:
        if semana_index == 0:
            return "No hay elemento anterior"
        else:
            semana_anterior_index = semana_index - 1
            ultimo_elemento_index = len(curso_data[semanas[semana_anterior_index]]['tipo']) - 1
            tipo_anterior = curso_data[semanas[semana_anterior_index]]['tipo'][ultimo_elemento_index]
            if tipo_anterior == 'preguntas':
                return f"Retrocede a las Preguntas de la {semanas[semana_anterior_index]}"
            elif tipo_anterior == 'examen':
                return f"Retrocede al Examen de la {semanas[semana_anterior_index]}"
            else:
                return f"Retrocede a la Clase {ultimo_elemento_index + 1} de la {semanas[semana_anterior_index]}"
    else:
        elemento_anterior_index = elemento_index - 1
        tipo_anterior = curso_data[semanas[semana_index]]['tipo'][elemento_anterior_index]
        if tipo_anterior == 'preguntas':
            return "Retrocede a las Preguntas"
        elif tipo_anterior == 'examen':
            return "Retrocede al Examen"
        else:
            return f"Retrocede a la Clase {elemento_anterior_index + 1}"


def siguiente_elemento():
    """
    Avanza al siguiente elemento (clase, preguntas o examen) de la semana actual o la siguiente semana.
    """
    global semana_actual, elemento_actual
    elemento_actual = (elemento_actual + 1) % len(curso_data[semanas[semana_actual]]['tipo'])
    if elemento_actual == 0:
        semana_actual = (semana_actual + 1) % len(semanas)
    return mostrar_elemento(semana_actual, elemento_actual)

def elemento_anterior():
    """
    Retrocede al elemento anterior (clase, preguntas o examen) de la semana actual o la semana anterior.
    """
    global semana_actual, elemento_actual
    if elemento_actual == 0:
        if semana_actual == 0:
            return mostrar_elemento(semana_actual, elemento_actual)
        else:
            semana_actual -= 1
            elemento_actual = len(curso_data[semanas[semana_actual]]['tipo']) - 1
    else:
        elemento_actual -= 1
    return mostrar_elemento(semana_actual, elemento_actual)


def responder_pregunta(mensaje, historial):
    """
    Genera una respuesta aleatoria del chatbot a una pregunta del usuario y la agrega al historial de chat.
    """
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
            contenido_elemento = gr.Markdown()
            gr.Markdown(f"""-------------------------------------------- """)
            with gr.Row():
                with gr.Column():
                    anterior_btn = gr.Button(interactive=True)
                with gr.Column():
                    gr.Markdown()
                with gr.Column():
                    siguiente_btn = gr.Button(interactive=True)

            # Chatbot
            chatbot = gr.Chatbot(label="Conversa con Alpakito 🦙 el Profe")
            with gr.Row():
                mensaje = gr.Textbox(label="¡Alpakito está listo!", placeholder="Pregúntale lo que quieras...", autofocus=True)
                with gr.Column(scale=0.05):  # Ajusta el ancho del botón al 10%
                    enviar_btn = gr.Button("Envía y aprende 🎓")
            #tx_box  = gr.Textbox(
            #            value=saluda(),  # Llama a la función y usa su retorno como valor inicial
            #            interactive=False  # Hace que el Textbox no sea editable
            #    )
        # Inicializar con el primer elemento de la primera semana
        contenido_inicial, header_inicial, texto_boton_siguiente_inicial, texto_boton_anterior_inicial = mostrar_elemento(0, 0)
        contenido_elemento.value = contenido_inicial
        semana_header.value = header_inicial
        siguiente_btn.value = texto_boton_siguiente_inicial
        anterior_btn.value = texto_boton_anterior_inicial

        siguiente_btn.click(siguiente_elemento, outputs=[contenido_elemento, semana_header, siguiente_btn, anterior_btn])
        anterior_btn.click(elemento_anterior, outputs=[contenido_elemento, semana_header, siguiente_btn, anterior_btn])
        enviar_btn.click(responder_pregunta, inputs=[mensaje, chatbot], outputs=[mensaje, chatbot])

    demo.launch(debug=True, server_name="127.0.0.1", server_port=8080)