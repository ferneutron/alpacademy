import requests


def rag_query(context, config):

    url = config["RAG_URL"]
    json = {"query": context}
    rag_api_response = requests.post(url, json=json)

    if rag_api_response.status_code == 200:

        response_content = rag_api_response.json()

        return response_content
    else:
        rag_api_response.raise_for_status()
        return None

