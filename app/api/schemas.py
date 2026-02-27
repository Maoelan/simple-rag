class QuestionRequest(BaseModel):
    question: str

class DocumentRequest(BaseModel):
    text: str