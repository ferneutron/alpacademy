from src.configs.openai_model_config import ModelConfig
from src.utilities.clients.openai_client import get_openai_client
from src.utilities.clients.groq_client import get_groq_client


def llm_inference_pipeline(
    llm_provider: str,
    query: str,
    model,
    config_path: str = r"src\configs\openai_config.json",
    user_id: str = "test_user",
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
        config = ModelConfig(config_path)
        model = model(config=config, client=client, user_id=user_id)
        return model.answer(query)
    except Exception as e:
        print(f"Error in inference pipeline: {e}")
        return "¡Ups! Algo salió mal. Por favor, inténtalo de nuevo."


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
