import uuid
from src.configs.openai_model_config import ModelConfig
from src.utilities.clients.openai_client import get_openai_client
from src.utilities.clients.groq_client import get_groq_client
from src.utilities.rag_aux import rag_query
from src.utilities.get_configs import get_config


def llm_inference_pipeline(
    llm_provider: str,
    question_id: str,
    query: str,
    model,
    config_path: str = "src/configs/openai_config.json",
):
    try:
        if llm_provider == "openai":
            client = get_openai_client()
        elif llm_provider == "groq":
            client = get_groq_client()
        else:
            raise ValueError(
                "Invalid LLM provider. Please choose 'openai' or 'groq'."
            )

        # Generate a random user ID to avoid reading from the persistent memory
        # every time the inference pipeline is called
        user_id = str(uuid.uuid4())

        config = ModelConfig(config_path)
        model = model(config=config, client=client, user_id=user_id)
        context = get_rag_context(query)
        questions = config.load_config("src/data/question_answer_pairs.json")
        question = questions[question_id]["question"]
        answer = questions[question_id]["answer"]
        return model.answer(
            query,
            system_prompt_vars={
                "context": context,
                "question": question,
                "answer": answer,
            },
        )
    except Exception as e:
        print(f"Error in inference pipeline: {e}")
        return "¡Ups! Algo salió mal. Por favor, inténtalo de nuevo."


def concatenate_texts(data):
    results = data.get("results", [])
    if not results:
        return ""

    concatenated_text = "\n\n".join(
        result["text"] for result in results if "text" in result
    )
    return concatenated_text


def get_rag_context(utterance: str) -> str:
    try:
        config = get_config()
        response = rag_query(context=utterance, config=config)
        return concatenate_texts(response)
    except Exception as e:
        print(f"Error in RAG context retrieval: {e}")
        return ""


# ###USAGE###

# from src.services.llm_response import llm_inference_pipeline
# from src.utilities.llm_call.openai_llm import Agent

# def get_response(query: str) -> str:
#     return llm_inference_pipeline(
#         llm_provider="openai", # or "groq"
#         query=query,
#         model=Agent,
#         user_id="123",
#     )
# response = get_response(query="Hola")
