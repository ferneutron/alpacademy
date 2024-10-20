from groq import Groq


def get_llm_client(config):

    client = Groq(api_key=config["GROQ_API_KEY"])

    return client