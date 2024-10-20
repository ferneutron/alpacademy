import gradio as gr

# Función que simula la respuesta de una LLM
def simulate_llm(input_text):
    return f"Respuesta de la LLM para: {input_text}"

# Interfaz de Gradio
def gradio_interface():
    with gr.Blocks() as demo:
        # Caja simulada usando gr.Group para organizar visualmente
        with gr.Group():
            gr.Markdown("## Aquí se muestra un contenido inicial")

        # Espacio para el output de la LLM
        output_text = gr.Textbox(label="Respuesta de LLM", lines=5, interactive=False)

        # Input del usuario
        input_text = gr.Textbox(label="Escribe algo aquí")

        # Botón "Avanza" alineado a la derecha
        with gr.Row():
            avanzar_button = gr.Button("Avanza", variant="primary")

        # Acción del botón: enviar el input del usuario a la LLM y mostrar la respuesta
        avanzar_button.click(simulate_llm, inputs=input_text, outputs=output_text)

    return demo

# Correr la interfaz con opción 'share=True' para generar URL pública
demo = gradio_interface()
demo.launch(share=True)
