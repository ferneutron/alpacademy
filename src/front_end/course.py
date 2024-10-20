import gradio as gr 

clase = f"""
## Mesopotamia: La tierra entre ríos

### ¿Qué es Mesopotamia?

Mesopotamia, la "tierra entre ríos" en griego, fue una de las primeras civilizaciones en surgir en el planeta. Ubicada entre los ríos Tigris y Éufrates, en lo que hoy es Irak, Irán, Siria y Turquía, esta región se convirtió en el crisol de muchas innovaciones que marcarían el rumbo de la humanidad. Los sumerios, acadios, babilonios y asirios fueron algunas de las civilizaciones que florecieron en Mesopotamia, dejando un legado invaluable en diversos campos.

### Importancia histórica

Gracias a las fértiles tierras de los valles fluviales, los habitantes de Mesopotamia desarrollaron una agricultura próspera y establecieron complejas sociedades urbanas. Construyeron grandes ciudades amuralladas, zigurats (templos escalonados) y sistemas de riego ingeniosos. Además, fueron pioneros en el desarrollo de la escritura cuneiforme, la cual les permitió registrar sus conocimientos, leyes y relatos históricos. Esta invención revolucionaria sentó las bases para el surgimiento de la escritura en otras partes del mundo.

### La vida en Mesopotamia

El legado de Mesopotamia es vasto y perdurable. Sus avances en matemáticas, astronomía, medicina y leyes influyeron en civilizaciones posteriores como la egipcia y la griega. El Código de Hammurabi, una de las primeras recopilaciones de leyes escritas, es un ejemplo de la sofisticación jurídica alcanzada por los babilonios. Asimismo, los mitos y leyendas mesopotámicas, como el de Gilgamesh, han cautivado a la humanidad durante milenios y continúan siendo objeto de estudio y fascinación.

"""

css = """
h1 {
    text-align: center;
    display:block;
}
"""

if __name__ == '__main__':
    demo = gr.Blocks(theme=gr.themes.Soft(), css=css)
    
    with demo:
        gr.Markdown(f""" """)
        gr.Markdown(f"""# Alpacademy """)
        gr.Markdown(f"""## Semana 1""")
        gr.Markdown(f""" """)

        with gr.Column():
            gr.Markdown(f"""-------------------------------------------- """)
            gr.Markdown(clase)
            gr.Markdown(f"""-------------------------------------------- """)
            with gr.Row():
                with gr.Column():
                    gr.Markdown()
                with gr.Column():
                    hola_1 = gr.Button(value="⏩ Siguiente ⏩", interactive=True)
                with gr.Column():
                    gr.Markdown()

            agent = gr.Textbox(lines=7, label="Agente")
            student = gr.Textbox(lines=1, label="Pregúntame", autofocus=True)

    demo.launch(debug=True, server_name="0.0.0.0", server_port=8080)