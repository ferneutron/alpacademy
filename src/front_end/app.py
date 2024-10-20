import gradio as gr 

if __name__ == '__main__':
    demo = gr.Blocks(theme=gr.themes.Soft())
    
    with demo:
        gr.Markdown(f"""# Alpacademy """)
        with gr.Column():
            with gr.Row():
                materia_1 = gr.Button(value="✨ Español", interactive=True)
                materia_2 = gr.Button(value="✨ Matemáticas", interactive=True)
        
            with gr.Row(visible=True) as summary_result:
                materia_3 = gr.Button(value="✨ Geografía", interactive=True)
                materia_4 = gr.Button(value="✨ Historia", interactive=True)
        with gr.Column():
            with gr.Row():
                hola_1 = gr.Button(value="Hola", interactive=True)
                hola_2 = gr.Button(value="Hello", interactive=True)
                hola_3 = gr.Button(value="Jelou", interactive=True)
                hola_4 = gr.Button(value="Jai", interactive=True)




    demo.launch(debug=True, server_name="0.0.0.0", server_port=8080)