from fastapi import APIRouter
from fastapi_injector import Injected
from src.models import RequestModel
from src.services import TeacherAssistantService

Router = APIRouter(prefix="/v1")


@Router.post("/predict")
async def orchestrator(
        request: RequestModel,
        teacher_assistant_service: Injected(TeacherAssistantService)
):

    prediction = teacher_assistant_service.predict(text=request.text)

    return prediction
