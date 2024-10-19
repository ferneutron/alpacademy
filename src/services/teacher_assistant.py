from src.utilities.companion_utilities import inference_pipeline


class TeacherAssistantService:

    def __init__(self):

        self.language = None
        self.week = None
        self.material_state = None
        self.week = None
        self.utterance = None

    def predict(self):

        prediction = inference_pipeline(self.utterance)

        return prediction