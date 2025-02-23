from src.utilities.companion_utilities import inference_pipeline_non_parametric
import yaml
from src.utilities.get_llms import get_llm_client
from src.utilities.llama_interaction import generate_llama_qa_response
from src.utilities.llama_interaction import get_llama_generated_question_from_material
from src.utilities.llama_interaction import generate_answer_from_generated_question
from src.services.llm_response import llm_inference_pipeline
from src.utilities.llm_call.openai_llm import Agent


class TeacherAssistantService:

    def __init__(self):

        self.language = "es"
        self.week = None
        self.material = None
        self.material_state = None #None, QA, Follow_up
        self.utterance = None #user input from text box
        self.next_material = False
        self.memory = None
        self.question = None #follow up question
        self.question_answer = None #follow_up answer
        self.material_index_position = None #material index position
        self.material = None #class material that is shown on main screen
        self.config = yaml.safe_load(open("src/configs/config.yml"))
        self.llm_client = get_llm_client(self.config)

    def predict(self, utterance):

        material_state = "QA"
        test_mat = material_1
        prediction = inference_pipeline_non_parametric(
            material_state="QA",
            material=self.material,
            question=self.question,
            question_answer=self.question_answer,
            utterance=utterance,
            config=self.config,
            llm_client=self.llm_client
        )

        return prediction

    def generate_question(self, material):

        llama_response = get_llama_generated_question_from_material(self.llm_client, self.config, material)
        return llama_response

    def answer_from_qa(self, material, utterance):

        llama_response = generate_llama_qa_response(self.llm_client, self.config, utterance, material)

        return llama_response

    def answer_from_generated_question(self, material, llama_generated_question, utterance):

        llama_response = generate_answer_from_generated_question(
            self.llm_client,
            self.config,
            material,
            llama_generated_question,
            utterance
        )
        return llama_response

    def answer_follow_up(self, question_key, utterance):
        follow_up_answer = llm_inference_pipeline(
            llm_provider="groq",
            question_id=question_key,
            query=utterance,
            model=Agent
        )
        return follow_up_answer
