from pydantic import BaseModel


class RequestModel(BaseModel):

    text: str
    unique_id: str | None = "-"
    call_id: str | None = "-"