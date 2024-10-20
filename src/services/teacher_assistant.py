from src.utilities.companion_utilities import inference_pipeline
from src.utilities.rag_aux import rag_query
import yaml
class TeacherAssistantService:

    def __init__(self):

        self.language = "es"
        self.week = None
        self.material_state = None
        self.utterance = None
        self.next_material = False
        self.memory = None

        self.config = yaml.safe_load(open("src/configs/config.yml"))


    def predict(self):

        prediction = inference_pipeline(self.utterance)

        return prediction
