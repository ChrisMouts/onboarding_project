from pydantic import BaseModel, Field
from typing import Optional

class ChatRequest(BaseModel):
    message: str = Field(..., description="Το ερώτημα ή η εντολή του χρήστη")
    thread_id: Optional[str] = Field("default", description="Αναγνωριστικό για τη μνήμη της συνομιλίας")