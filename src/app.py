import uvicorn
from fastapi import FastAPI
from injector import Injector, SingletonScope
from fastapi_injector import attach_injector
from src.routers.v1.router import Router as RouterV1
from src.services.teacher_assistant import TeacherAssistantService


injector = Injector()

injector.binder.bind(TeacherAssistantService, scope=SingletonScope)

app = FastAPI()
app.include_router(RouterV1)


attach_injector(app, injector)

if __name__ == "__main__":
    uvicorn.run(app=app, port=8080)