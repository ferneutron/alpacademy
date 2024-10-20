from src.utilities.llama_interaction import get_llama_generated_question_from_material
from src.utilities.llama_interaction import generate_llama_qa_response
from src.services.llm_response import llm_inference_pipeline
from src.utilities.llm_call.openai_llm import Agent


def inference_pipeline_non_parametric(
        material_state,
        material,
        question,
        question_answer,
        utterance,
        config,
        llm_client):

    if material_state == "proactive":
        print("entra")
        llama_generated_question = get_llama_generated_question_from_material(llm_client, config)
        response = llm_inference_pipeline(
            llm_provider="groq",
            question_id="Pregunta 4",
            query="a la caza",
            model=Agent
        )
        return response

    elif material_state == "Follow_up":
        pass

    elif material_state == "QA":
        print("utterance")
        print(utterance)
        response = generate_llama_qa_response(llm_client, config, utterance)

        return response


def inference_pipeline():

    pass
