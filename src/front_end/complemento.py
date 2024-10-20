import gradio as gr 

from student import Student

css = """
h1 {
    text-align: center;
    display:block;
}
"""

student = Student()


def update_header():
    print(f"before header: {student.header}")
    if student.actual_material == "lecciones":
        student.header = f"## Clase {student.actual + 1}"
    elif student.actual_material == "preguntas":
        student.header = f"## Pregunta {student.actual + 1}"
    elif student.actual_material == "examen":
        student.header = f"## Quiz {student.actual + 1}"

    print(f"after header: {student.header}")


def get_content():
    if student.actual_material == "lecciones":
        student.content = student.lecciones
    elif student.actual_material == "preguntas":
        student.content = student.preguntas
    elif student.actual_material == "examen":
        student.content = student.examen

    return student.content


def next_content():
    print(f"Curr content: {student.actual_material}")
    if student.actual_material == "lecciones":
        student.actual_material = "preguntas"
        student.content = student.preguntas
    elif student.actual_material == "preguntas":
        student.actual_material = "examen"
        student.content = student.examen

    print(f"New content: {student.actual_material}")


def validate_interaction():

    if student.interaccion == False:
        # Traer pregunta generada por el agente
        # Ej: response = AgentCall(query)
        response = "¿En qué año se fundó Mesopotamia?"
        content = get_content()
        return (
            gr.Markdown(student.content[student.actual]["pregunta"]),
            gr.Textbox(lines=7, label="Agente", value=response),
            gr.Textbox(lines=1, label="Pregúntame", autofocus=True),
            gr.Markdown(f"""{student.header}""")
            )
    else:
        student.actual += 1
        print(f"Actual: {student.actual}")
        if student.actual == len(student.content):
            student.actual = 0
            print(f"Update actual: {student.actual}")
            next_content()
        
        update_header()

        return (
            gr.Markdown(student.content[student.actual]["pregunta"]),
            gr.Textbox(lines=7, label="Agente", value=""),
            gr.Textbox(lines=1, label="Pregúntame", autofocus=True, value=""),
            gr.Markdown(f"""{student.header}""")
            )
    
def request_from_student(query: str, context: str):
    
    if query == "":
        return (
            gr.Textbox(lines=7, label="Agente", value="¿Quieres saber algo más?"),
            gr.Textbox(lines=1, label="Pregúntame", autofocus=True, value="")
        )
    else:
        # call LLAMA
        # response = LLama.request(query, context)
        response = "Mesopotamia fue una civilización antigua y bla bla bla"
        student.interaccion = True
        return (
            gr.Textbox(lines=7, label="Agente", value=response),
            gr.Textbox(lines=1, label="Pregúntame", autofocus=True, value="")
        )

if __name__ == '__main__':

    demo = gr.Blocks(theme=gr.themes.Soft(), css=css)
    
    with demo:
        gr.Markdown(f""" """)
        gr.Markdown(f"""# Alpacademy """)
        gr.Markdown(f""" """)
        with gr.Row():
            with gr.Column():
                gr.Markdown(f"""## Semana 1""")
                gr.Markdown(f""" """)
            with gr.Column():
                gr.Markdown()
            with gr.Column():
                gr.Markdown()
            with gr.Column():
                header = gr.Markdown(f"""{student.header}""")
                gr.Markdown(f""" """)
        gr.Markdown(f""" """)

        with gr.Column():
            gr.Markdown(f"""-------------------------------------------- """)
            clase_content = gr.Markdown(student.content[student.actual]["pregunta"])
            gr.Markdown(f"""-------------------------------------------- """)
            with gr.Row():
                with gr.Column():
                    gr.Markdown()
                with gr.Column():
                    siguiente = gr.Button(value="⏩ Siguiente ⏩", interactive=True)
                with gr.Column():
                    gr.Markdown()

            agente = gr.Textbox(lines=7, label="Agente")
            alumno = gr.Textbox(lines=1, label="Pregúntame", autofocus=True)

        siguiente.click(fn=validate_interaction, inputs=[], outputs=[clase_content, agente, alumno, header])
        alumno.submit(fn=request_from_student, inputs=[alumno, clase_content], outputs=[agente, alumno])

    demo.launch(debug=True, server_name="0.0.0.0", server_port=8080)