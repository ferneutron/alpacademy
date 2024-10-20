from src.utilities.rag_aux import rag_query


def extract_question_from_material(material, llm_client, config):

    system_prompt = config["LLM_GET_QUESTION_PROMPT"]
    user_prompt = config["LLM_GET_QUESTION_USER_PROMPT"]
    parametrized_user_prompt = user_prompt.format(context=material)

    completion = llm_client.chat.completions.create(
        model="llama-3.1-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": parametrized_user_prompt
            }
        ],
        temperature=0.1,
        max_tokens=300,
        top_p=1,
        stream=False,
        stop=None,
    )

    return completion


def proactive_llm_state_backup(utterance, material, config, llm_client, n=3):

    rag_response = rag_query(material, config)

    if rag_response != None:

        results = rag_response["results"]
        top_results = results[:n]
        context = ''.join(top_results['text'] for result in top_results)


    else:
        print("error proactive_llm_state")
        return "ERORR!"