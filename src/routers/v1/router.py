from fastapi import APIRouter
from fastapi_injector import Injected
from src.models import RequestModel, AnswerFromQA, AnswerGenerated
from src.models import FollowUpModel
from src.services import TeacherAssistantService

Router = APIRouter(prefix="/v1")


@Router.post("/predict")
async def orchestrator(
        request: RequestModel,
        teacher_assistant_service: TeacherAssistantService = Injected(TeacherAssistantService)
):

    prediction = teacher_assistant_service.predict(utterance=request.text)

    return prediction


@Router.post("/generate_question")
async def orchestrator(
        request: RequestModel,
        teacher_assistant_service: TeacherAssistantService = Injected(TeacherAssistantService)
):

    llama_generated_question = teacher_assistant_service.generate_question(material=request.text)
    return llama_generated_question


@Router.post("/answer_from_qa")
async def orchestrator(
        request: AnswerFromQA,
        teacher_assistant_service: TeacherAssistantService = Injected(TeacherAssistantService)
):

    llama_generated_answer = teacher_assistant_service.answer_from_qa(
        material=request.material,
        utterance=request.text
    )
    return llama_generated_answer


@Router.post("/answer_from_generated_question")
async def orchestrator(
        request: AnswerGenerated,
        teacher_assistant_service: TeacherAssistantService = Injected(TeacherAssistantService)
):

    llama_generated_answer = teacher_assistant_service.answer_from_generated_question(
        material=request.material,
        llama_generated_question=request.llama_generated_question,
        utterance=request.text

    )
    return llama_generated_answer


@Router.post("/answer_from_follow_up")
async def orchestrator(
        request: FollowUpModel,
        teacher_assistant_service: TeacherAssistantService = Injected(TeacherAssistantService)
):
    llama_follow_up_answer = teacher_assistant_service.answer_follow_up(
        question_key=request.question_key,
        utterance=request.text
    )
    return llama_follow_up_answer