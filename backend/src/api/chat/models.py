from datetime import datetime, timezone
from sqlmodel import SQLModel, Field, DateTime

def get_utc_now():
    # Get the current UTC time
    return datetime.now().replace(tzinfo=timezone.utc)

class ChatMessagePayload(SQLModel):
    # pydantic model
    # for validation of incoming data
    message: str

class ChatMessage(SQLModel, table=True):
    # database table model
    #  for saving, retrieving, and manipulating chat messages
    # serialization
    id: int | None = Field(default=None, primary_key=True)
    message: str
    created_at: datetime = Field(default_factory=get_utc_now, sa_type=DateTime(timezone=True), primary_key=False, nullable=False)
    
class ChatMessageListItem(SQLModel):
    id: int | None = Field(default=None,)  
    message: str
    created_at: datetime = Field(default=None)
