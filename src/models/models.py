from pydantic import BaseModel


class RequestModel(BaseModel):

    text: str
    unique_id: str | None = "-"
    call_id: str | None = "-"


class AnswerFromQA(BaseModel):
    text: str
    material: str
    unique_id: str | None = "-"
    call_id: str | None = "-"


class AnswerGenerated(BaseModel):
    text: str
    material: str
    llama_generated_question: str


class FollowUpModel(BaseModel):
    text: str
    question_key: str
