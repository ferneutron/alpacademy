import logging
import sys
import uvicorn
from fastapi import FastAPI
from injector import Injector, SingletonScope
from fastapi_injector import attach_injector
from routers.v1 import Router as RouterV1
from services import TeacherAssistantService


injector = Injector()

injector.binder.bind(TeacherAssistantService, scope=SingletonScope)

app = FastAPI()
app.include_router(RouterV1)


attach_injector(app, injector)

if __name__ == "__main__":
    uvicorn.run(app=app, port=8080)