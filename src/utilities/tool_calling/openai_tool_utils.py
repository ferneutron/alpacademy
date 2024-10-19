import json
from pydantic import BaseModel, Field
from typing import Callable, Dict, Any, List, Union
from openai.types.chat import ChatCompletion
from datetime import datetime
from enum import Enum


def get_tool_schema(tool: Callable, model: BaseModel) -> Dict[str, Any]:
    param_schema = model.model_json_schema()
    properties = param_schema.get("properties")
    required = param_schema.get("required")

    for property in properties.values():
        property.pop("title")

    schema = {
        "type": "function",
        "function": {
            "name": tool.__name__,
            "description": tool.__doc__.strip(),
            "parameters": {
                "type": "object",
                "properties": properties,
                "required": required,
            },
        },
    }
    return schema


def get_tool_call_results(
    tool_list: List[Callable], chat_completion_raw: ChatCompletion
) -> Union[List[Dict[str, Any]], str]:
    if isinstance(chat_completion_raw, str):
        return chat_completion_raw
    chat_completion = chat_completion_raw.choices[0].message
    if chat_completion.tool_calls is None:
        return chat_completion_raw.choices[0].message.content
    tool_call_results = []
    tool_call_results.append(chat_completion_raw.choices[0].message)
    for tool_call in chat_completion.tool_calls:
        try:
            for tool in tool_list:
                if tool.__name__ == tool_call.function.name:
                    print("Calling tool: ", tool.__name__)
                    result = tool(**json.loads(tool_call.function.arguments))
                    tool_call_results.append(
                        {
                            "tool_call_id": tool_call.id,
                            "role": "tool",
                            "name": tool.__name__,
                            "content": str(result),
                        }
                    )
        except Exception as e:
            print(
                "[TOOL ERROR]: An error occurred while calling the tool: ",
                tool.__name__,
                f"Error: {e}",
            )
    return tool_call_results


def reloj(formato: str) -> str:
    """
    Devuelve la hora actual en formato HH:MM.

    Args:
    - formato: str, formato de la hora a devolver (12 o 24 horas).

    Returns:
    - str, hora actual en formato HH:MM.
    """
    if formato == "12":
        return datetime.now().strftime("%I:%M %p")
    elif formato == "24":
        return datetime.now().strftime("%H:%M")
    else:
        return "¡Ups! Algo salió mal. Por favor, inténtalo de nuevo."


class FormatoHora(str, Enum):
    doce_horas = "12"
    veinticuatro_horas = "24"


class RelojSchema(BaseModel):
    formato: str = Field(
        ...,
        title="Formato",
        description="Formato de la hora a devolver.",
        json_schema_extra={"enum": [e.value for e in FormatoHora]},
    )
