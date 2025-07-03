from fastapi import APIRouter, Depends
from typing import List

from api.ai.schemas import EmailMessageSchema
from api.ai.services import generate_email_message
from .models import ChatMessagePayload, ChatMessage, ChatMessageListItem
from api.db import get_session
from sqlmodel import Session, select
router = APIRouter()


@router.get("/")
def chat_health():
    return {'status': "ok"}

# curl http://localhost:8080/api/chats/recent/
@router.get('/recent/', response_model=List[ChatMessageListItem])
def chat_list_messages(session: Session = Depends(get_session)):
    query = select(ChatMessage)
    results = session.exec(query).fetchall()[:10]
    return results

# HTTP POST => payload = {"message" : "Hello World"} => {"message": "Hello World", id: 1}
# curl -X POST -d '{"message": "Hello World"}' http://localhost:8080/api/chats/ -H "Content-Type: application/json"
# curl -X POST -d '{"message": "Hello World"}' -H "Content-Type: application/json" https://hammerhead-app-jw7do.ondigitalocean.app/api/chats/
# curl -X POST -d '{"message": "Explainme 4 benefits of Docker"}' http://localhost:8080/api/chats/ -H "Content-Type: application/json"
@router.post('/', response_model=EmailMessageSchema) 
def chat_create_message(
    payload: ChatMessagePayload,
    session: Session = Depends(get_session)
):
    """
    Create a new chat message.
    """
    data = payload.model_dump()
    print(data)
    obj = ChatMessage.model_validate(data) # here we validate the data against the ChatMessage model
    # ready to store in the database
    session.add(obj)
    session.commit()
    # session.refresh(obj)  # refresh the object to get the id and other fields populated
    response = generate_email_message(payload.message)  # Call the function to generate email message
    return response
