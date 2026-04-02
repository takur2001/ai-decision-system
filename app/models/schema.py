from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str
    service: str
    message: str


class UploadResponse(BaseModel):
    message: str
    filename: str
    saved_to: str