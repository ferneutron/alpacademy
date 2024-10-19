from src.configs.openai_model_config import ModelConfig
from src.utilities.clients.openai_client import get_openai_client


def llm_inference_pipeline(
    query: str,
    model,
    config_path: str = r"src\configs\openai_config.json",
    user_id: str = "test_user",
):
    try:
        client = get_openai_client()
        config = ModelConfig(config_path)
        model = model(config=config, client=client, user_id=user_id)
        return model.answer(query)
    except Exception as e:
        print(f"Error in inference pipeline: {e}")
        return "¡Ups! Algo salió mal. Por favor, inténtalo de nuevo."


# ###USAGE###

# from src.services.llm_response import llm_inference_pipeline
# from src.utilities.llm_call.openai_llm import OpenaiAgent

# def get_response(query: str) -> str:
#     return llm_inference_pipeline(
#         query=query,
#         model=OpenaiAgent,
#         user_id="123",
#     )
