import os
import json
from typing import List, Dict, Any
import boto3
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError, BotoCoreError
from dotenv import load_dotenv


load_dotenv()


class DynamoMemory:
    def __init__(self, user_id: str) -> None:
        self.memory_type = os.getenv("MEMORY_TYPE")
        self.table_name = os.getenv("AWS_DYNAMODB_TABLE_NAME")
        self.query_key = os.getenv("AWS_DYNAMODB_QUERY_KEY")
        self.answer_key = os.getenv("AWS_DYNAMODB_ANSWER_KEY")
        self.user_id_key = os.getenv("AWS_DYNAMODB_USER_ID_KEY")
        self.order_key = os.getenv("AWS_DYNAMODB_ORDER_KEY")
        self.n_interactions = int(os.getenv("AWS_DYNAMODB_N_INTERACTIONS"))
        self.openai_json_memory = os.getenv("JSON_MEMORY_PATH")
        self.user_id = user_id

        if self.memory_type == "dynamodb":
            self.dynamodb = self.get_dynamodb_resource()
            self.table = self.dynamodb.Table(self.table_name)
            self.check_table_exists(self.table)

    def get_dynamodb_resource(self) -> boto3.resource:
        RESOURCE = "dynamodb"
        AWS_REGION = os.getenv("AWS_DYNAMODB_REGION")
        AWS_DYNAMODB_ENDPOINT_URL = os.getenv("AWS_DYNAMODB_ENDPOINT_URL")
        try:
            if AWS_REGION == "localhost":
                dynamodb = boto3.resource(
                    RESOURCE,
                    endpoint_url=AWS_DYNAMODB_ENDPOINT_URL,
                    region_name=AWS_REGION,
                )
            else:
                dynamodb = boto3.resource(RESOURCE, region_name=AWS_REGION)

            print("DynamoDB resource created successfully")
            return dynamodb
        except Exception as e:
            print(f"Error creating DynamoDB resource: {e}")
            return None

    def check_table_exists(self, table) -> None:
        try:
            table.load()
            print(f"Table {self.table_name} exists")
        except ClientError as e:
            if e.response["Error"]["Code"] == "ResourceNotFoundException":
                print(f"Table {self.table_name} does not exist")
            else:
                print(f"Error checking table {self.table_name}: {e}")

    def get_user_history(self, user_id: str) -> List[Dict[str, str]]:
        if self.memory_type == "dynamodb":
            try:
                condition = Key(self.user_id_key).eq(user_id)
                response = self.table.query(
                    KeyConditionExpression=condition,
                    ScanIndexForward=False,
                    Limit=self.n_interactions,
                )
                items = response["Items"][::-1]
                print("User history retrieved successfully.")
                return items
            except (BotoCoreError, ClientError) as e:
                print(f"Error getting user history: {e}")
                return []
        elif self.memory_type == "json":
            try:
                if not os.path.exists(self.openai_json_memory):
                    print(
                        "JSON memory file does not exist. Returning empty "
                        "history."
                    )
                    return []
                with open(self.openai_json_memory, "r") as file:
                    data = json.load(file)
                user_history = [
                    item for item in data if item[self.user_id_key] == user_id
                ]
                print("User history retrieved successfully from JSON.")
                return user_history[: self.n_interactions]
            except Exception as e:
                print(f"Error getting user history from JSON: {e}")
                return []

    def write_interaction(self, interaction: Dict[str, str]) -> None:
        if self.memory_type == "dynamodb":
            try:
                self.table.put_item(Item=interaction)
                print("Interaction written successfully.")
            except (BotoCoreError, ClientError) as e:
                print(f"Error writing interaction: {e}")
            except Exception as e:
                print(f"Unexpected error writing interaction: {e}")
        elif self.memory_type == "json":
            try:
                # Ensure the directory exists
                os.makedirs(
                    os.path.dirname(self.openai_json_memory), exist_ok=True
                )

                if os.path.exists(self.openai_json_memory):
                    with open(self.openai_json_memory, "r") as file:
                        data = json.load(file)
                else:
                    data = []
                data.append(interaction)
                with open(self.openai_json_memory, "w") as file:
                    json.dump(data, file, indent=4)
                print("Interaction written successfully to JSON.")
            except Exception as e:
                print(f"Error writing interaction to JSON: {e}")

    def assemble_messages(
        self,
        messages_history: List[Dict[str, str]],
        current_messages: List[Dict[str, str]],
    ) -> List[Dict[str, Any]]:
        try:
            history = []
            for message in messages_history:
                query = message[self.query_key]
                answer = message[self.answer_key]
                user_content = {"role": "user", "content": query}
                assistant_content = {"role": "assistant", "content": answer}
                history.extend([user_content, assistant_content])
            messages = current_messages[:1] + history + current_messages[-1:]
            print("Messages assembled successfully.")
            return messages
        except Exception as e:
            print(f"Error assembling messages: {e}")
            return []

    def update_memory(
        self,
        user_id: str,
        query: str,
        answer: str,
        order: int,
    ) -> None:
        try:
            current_interaction = {
                self.user_id_key: user_id,
                self.query_key: query,
                self.answer_key: answer,
                self.order_key: order,
            }
            self.write_interaction(current_interaction)
        except Exception as e:
            print(f"Error updating memory: {e}")
