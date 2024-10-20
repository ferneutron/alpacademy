import gradio as gr 

from semanas import Semana1

css = """
h1 {
    text-align: center;
    display:block;
}
"""

semana = Semana1()


def validate_interaction(student_input: str):

    if student_input == "" and semana.interaccion == False:
        return (
            gr.Markdown(semana.material[semana.actual]),
            gr.Textbox(lines=7, label="Agente", value="¿En qué año se fundó Mesopotamia?"),
            gr.Textbox(lines=1, label="Pregúntame", autofocus=True)
            )
    else:
        semana.actual += 1
        return (
            gr.Markdown(semana.material[semana.actual]),
            gr.Textbox(lines=7, label="Agente", value=""),
            gr.Textbox(lines=1, label="Pregúntame", autofocus=True, value="")
            )
    
def request_from_student(query: str, context: str):
    # call LLAMA
    # response = LLama.request(query, context)
    response = "Mesopotamia fue una civilización antigua y bla bla bla"
    semana.interaccion = True
    return (
        gr.Textbox(lines=7, label="Agente", value=response),
        gr.Textbox(lines=1, label="Pregúntame", autofocus=True, value="")
    )

if __name__ == '__main__':

    demo = gr.Blocks(theme=gr.themes.Soft(), css=css)
    
    with demo:
        gr.Markdown(f""" """)
        gr.Markdown(f"""# Alpacademy """)
        gr.Markdown(f"""## Semana 1""")
        gr.Markdown(f""" """)

        with gr.Column():
            gr.Markdown(f"""-------------------------------------------- """)
            clase_content = gr.Markdown(semana.material[semana.actual])
            gr.Markdown(f"""-------------------------------------------- """)
            with gr.Row():
                with gr.Column():
                    gr.Markdown()
                with gr.Column():
                    siguiente = gr.Button(value="⏩ Siguiente ⏩", interactive=True)
                with gr.Column():
                    gr.Markdown()

            agent = gr.Textbox(lines=7, label="Agente")
            student = gr.Textbox(lines=1, label="Pregúntame", autofocus=True)

        siguiente.click(fn=validate_interaction, inputs=[student], outputs=[clase_content, agent, student])
        student.submit(fn=request_from_student, inputs=[student, clase_content], outputs=[agent, student])

    demo.launch(debug=True, server_name="0.0.0.0", server_port=8080)