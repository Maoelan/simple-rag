from pydantic import BaseModel

class QuestionRequest(BaseModel):
    question: str

class DocumentRequest(BaseModel):
    text: str