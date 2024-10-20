from src.services.llm_states import proactive_llm_state


def inference_pipeline(
        material_state,
        material,
        question,
        question_answer,
        utterance,
        config,
        llm_client):

    if material_state != None and type(material_state) == str:

        if material_state == "question":

            print("en estado de pregunta")

        if material_state == "follow_up":

            print("en estado de follow_up")


    else:

        if utterance != None:

            answer = proactive_llm_state(utterance, material, config, llm_client)


            print("en estado proactivo")





    return "tu utterance es:" + utterance