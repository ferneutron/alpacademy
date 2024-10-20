import os
from datetime import datetime
from typing import Dict, List, Union
import openai
from openai import OpenAI
from groq import Groq
from openai.types.chat import ChatCompletion

# from src.utilities.configs.model_config import ModelConfig
from src.utilities.memory.dynamo_memory import DynamoMemory
from src.utilities.tool_calling.openai_tool_utils import (
    reloj,
    get_tool_schema,
    get_tool_call_results,
)
from src.utilities.tool_calling.openai_tool_utils import RelojSchema
from tenacity import retry, wait_fixed, stop_after_attempt


class Agent:

    def __init__(
        self, config: Dict, client: openai.OpenAI, user_id: str
    ) -> None:
        self.system_prompt = config.system_prompt
        self.user_prompt = config.user_prompt
        self.client = client
        self.temperature = config.temperature
        self.model = self.setup_model_name()
        self.max_tokens = int(os.getenv("AGENT_MAX_TOKENS"))
        self.available_tools = os.getenv("AGENT_AVAILABLE_TOOLS").split(",")
        self.max_tool_iterations = int(os.getenv("AGENT_MAX_TOOL_ITERATIONS"))
        self.tool_choice = os.getenv("AGENT_TOOL_CHOICE")
        self.tool_list = self.setup_tool_list()
        self.tool_schemas = self.setup_tool_schemas()
        self.memory = DynamoMemory(user_id=user_id)
        self.user_id = user_id

    def setup_model_name(self) -> str:
        if isinstance(self.client, OpenAI):
            return os.getenv("OPENAI_AGENT_MODEL")
        elif isinstance(self.client, Groq):
            return os.getenv("GROQ_AGENT_MODEL")
        else:
            raise ValueError(
                "Invalid client type. Please choose 'openai' or ' groq'."
            )

    def agent_call(
        self, messages: List[Dict[str, str]], model: str, temperature: float
    ) -> Union[str, ChatCompletion]:
        tool_params = {}
        try:
            if self.tool_choice != "none":
                tool_params = {
                    "tools": self.tool_schemas,
                    "tool_choice": self.tool_choice,
                }

        except Exception as e:
            print(f"Error setting tool parameters: {e}")
        try:
            return self.client.chat.completions.create(
                messages=messages,
                model=model,
                temperature=temperature,
                max_tokens=self.max_tokens,
                **tool_params,
            )
        except Exception as e:
            print(f"Error calling the agent: {e}")
            return "¡Ups! Algo salió mal. Por favor, inténtalo de nuevo."

    def setup_tool_list(self) -> List:
        tool_list = [
            reloj,
        ]
        return [
            tool for tool in tool_list if tool.__name__ in self.available_tools
        ]

    def setup_tool_schemas(self) -> None:
        tool_list = self.tool_list
        tool_schemas = []
        for tool in tool_list:
            if tool.__name__ == "reloj":
                tool_schemas.append(
                    get_tool_schema(tool=tool, model=RelojSchema)
                )

        return tool_schemas

    @retry(wait=wait_fixed(2), stop=stop_after_attempt(5))
    def answer(
        self,
        query: str,
        system_prompt_vars: Dict = None,
        user_prompt_vars: Dict = None,
    ) -> str:
        messages = []

        if self.system_prompt is not None:
            if system_prompt_vars is not None:
                self.system_prompt = self.system_prompt.format(
                    **system_prompt_vars
                )
            messages.append({"role": "system", "content": self.system_prompt})
        if self.user_prompt is not None:
            if user_prompt_vars is not None:
                query = query.format(**user_prompt_vars)
            # Check if the query has already been formatted
            if "{query}" in self.user_prompt:
                query = self.user_prompt.format(query=query)
        messages.append({"role": "user", "content": query})

        history = self.memory.get_user_history(self.user_id)
        messages = self.memory.assemble_messages(history, messages)

        response_content = self.agent_call(
            messages=messages, model=self.model, temperature=self.temperature
        )

        processed_response = get_tool_call_results(
            tool_list=self.tool_list, chat_completion_raw=response_content
        )

        iteration_count = 0
        max_iterations = self.max_tool_iterations

        tmp_tool_messages = []
        tmp_tool_messages.extend(messages)

        while (
            not isinstance(processed_response, str)
            and iteration_count < max_iterations
        ):
            tmp_tool_messages.extend(processed_response)
            response_content = self.agent_call(
                messages=tmp_tool_messages,
                model=self.model,
                temperature=self.temperature,
            )
            processed_response = get_tool_call_results(
                tool_list=self.tool_list, chat_completion_raw=response_content
            )
            iteration_count += 1

        if not isinstance(processed_response, str):
            print(
                "[TOOL ERROR] Max iterations reached without obtaining a "
                "string response."
            )
            response_str = (
                "¡Ups! Algo salió mal. Por favor, inténtalo de nuevo."
            )
        else:
            response_str = processed_response

        # Get timestamp in ISO format
        timestamp = datetime.now().isoformat()

        self.memory.update_memory(
            user_id=self.user_id,
            query=query,
            answer=response_str,
            order=timestamp,
        )
        return response_str
