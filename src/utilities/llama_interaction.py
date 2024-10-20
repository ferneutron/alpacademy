from src.utilities.rag_aux import rag_query

material = '**La Era de la Prehistoria**\n\n* La prehistoria es el período de tiempo que comprende desde la aparición del primer ser humano hasta la invención de la escritura.\n* Durante la prehistoria, los seres humanos se desarrollaron y se extendieron por todo el mundo, lo que se conoce como el poblamiento de los continentes.\n* La prehistoria se divide en tres grandes periodos: Paleolítico (hace 2,5 millones de años hasta hace 10.000 años), Mesolítico (hace 10.000 años hasta hace 5.000 años) y Neolítico (hace 5.000 años hasta hace 2.000 años).\n* Durante la prehistoria, los seres humanos se dedicaron a la caza y la recolección de alimentos, hasta que se desarrolló la agricultura y la ganadería.\n* La domesticación de plantas y animales permitió a los seres humanos establecerse en un lugar y formar comunidades más grandes.\n* La prehistoria nos deja un legado en forma de herramientas de piedra, pinturas rupestres y otros objetos que nos ayudan a entender cómo vivían nuestros antepasados.\n\n'


def get_llama_generated_question_from_material(llm_client, config, mater=material):
    system_prompt = config["LLM_GET_QUESTION_PROMPT"]
    user_prompt = config["LLM_GET_QUESTION_USER_PROMPT"]
    parametrized_user_prompt = user_prompt.format(context=mater)
    response = None
    try:
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
            temperature=0.8,
            max_tokens=300,
            top_p=1,
            stream=False,
            stop=None,
        )

        response = completion.choices[0].message.content

    except Exception as e:
        print("error groq api")
        return response

    return response


def generate_llama_qa_response(llm_client, config, utterance, mater, n=1):
    system_prompt = config["LLM_ANSWER_QUESTION_PROMPT"]
    user_prompt = config["LLM_ANSWER_QUESTION_USER_PROMPT"]

    parametrized_user_prompt = user_prompt.format(context=mater, student_question=utterance)
    response = None

    try:
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

        response = completion.choices[0].message.content

    except Exception as e:
        print("error groq api")
        return response

    return response


def generate_answer_from_generated_question(llm_client, config, material, llama_generated_question, utterance):

    system_prompt = config["LLM_ANSWER_FROM_GENERATED_QUESTION_PROMPT"]
    user_prompt = config["LLM_ANSWER_FROM_GENERATED_QUESTION_USER_PROMPT"]


    parametrized_user_prompt = user_prompt.format(
        context=material,
        generated_question=llama_generated_question,
        student_answer=utterance
    )

    response = None
    try:
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

        response = completion.choices[0].message.content

    except Exception as e:
        print("error groq api")
        return response

    return response


def generate_llama_qa_response_wo_material(llm_client, config, utterance, mater=material, n=1):
    system_prompt = config["LLM_ANSWER_QUESTION_PROMPT"]
    user_prompt = config["LLM_ANSWER_QUESTION_USER_PROMPT"]

    parametrized_user_prompt = user_prompt.format(context=mater, student_question=utterance)
    response = None

    try:
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

        response = completion.choices[0].message.content

    except Exception as e:
        print("error groq api")
        return response

    return response

