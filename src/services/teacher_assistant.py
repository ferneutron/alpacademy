from src.utilities.companion_utilities import inference_pipeline


class TeacherAssistantService:

    def __init__(self):

        self.language = "es"
        self.week = None
        self.material_state = None
        self.utterance = None
        self.next_material = False
        self.memory = None

    def predict(self):

        prediction = inference_pipeline(self.utterance)

        return prediction