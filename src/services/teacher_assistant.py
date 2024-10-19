from injector import inject


class TeacherAssistantService:

    @inject
    def __init__(self):
        pass
    def predict(self, raw_utterance):

        return "test prediction"

