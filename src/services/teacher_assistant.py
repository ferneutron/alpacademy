from src.utilities.companion_utilities import inference_pipeline

# from src.utilities.rag_aux import rag_query
import yaml
from src.utilities.get_llms import get_llm_client



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


    def predict(self):

        prediction = inference_pipeline(
            material_state=self.material_state,
            material=self.material,
            question=self.question,
            question_answer=self.question_answer,
            utterance=self.utterance,
            config=self.config,
            llm_client=self.llm_client
        )

        return prediction
