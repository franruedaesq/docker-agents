from fastapi import APIRouter, Depends, HTTPException
from typing import List

from api.ai.schemas import EmailMessageSchema, SupervisorMessageSchema
from api.ai.services import generate_email_message
from api.ai.agents import get_supervisor
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
# curl -X POST -d '{"message": "Explainme 4 benefits of Docker"}' https://hammerhead-app-jw7do.ondigitalocean.app/api/chats/ -H "Content-Type: application/json"
# curl -X POST -d '{"message": "Research why it is good to wake up early and go outside and email me the results to franchy008@gmail.com"}' https://hammerhead-app-jw7do.ondigitalocean.app/api/chats/ -H "Content-Type: application/json"
# curl -X POST -d '{"message": "Research why it is good to wake up early and go outside and email me the results to franchy008@gmail.com"}' http://localhost:8080/api/chats/ -H "Content-Type: application/json"
@router.post('/', response_model=SupervisorMessageSchema) 
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
    # response = generate_email_message(payload.message)  # Call the function to generate email message
    supe = get_supervisor()
    msg_data = {
        "messages": [
            {"role": "user", 
             "content": payload.message
             }
        ]
    }
    result = supe.invoke(msg_data)
    if not result:
        raise HTTPException(
            status_code=400,
            detail="Failed to generate response from the supervisor."
        )
    messages = result.get("messages", [])
    if not messages:
        raise HTTPException(
            status_code=400,
            detail="No messages returned from the supervisor."
        )
    return messages[-1]