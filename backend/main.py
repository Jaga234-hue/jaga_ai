from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
import uuid
from typing import List, Optional
from pydantic import BaseModel
from database import get_db, init_db, Conversation, Message
from bedrock_service import BedrockService
import datetime

app = FastAPI(title="Jaga AI Chatbot API")

# Add CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

bedrock = BedrockService()

# Initialize DB on startup
@app.on_event("startup")
def startup_event():
    init_db()

class ChatRequest(BaseModel):
    conversation_id: str
    message: str
    user_name: Optional[str] = "User"

class MessageSchema(BaseModel):
    role: str
    content: str
    timestamp: datetime.datetime

    class Config:
        from_attributes = True

class ConversationSchema(BaseModel):
    id: str
    title: str
    user_name: str
    created_at: datetime.datetime

    class Config:
        from_attributes = True

@app.post("/chat")
async def chat(request: ChatRequest, db: Session = Depends(get_db)):
    # 1. Get or create conversation
    conv = db.query(Conversation).filter(Conversation.id == request.conversation_id).first()
    if not conv:
        conv = Conversation(id=request.conversation_id, title=request.message[:30], user_name=request.user_name)
        db.add(conv)
        db.commit()

    # 2. Save user message
    user_msg = Message(conversation_id=request.conversation_id, role="user", content=request.message)
    db.add(user_msg)
    db.commit()

    # 3. Get history for context
    history = db.query(Message).filter(Message.conversation_id == request.conversation_id).order_by(Message.timestamp.asc()).all()
    messages_payload = [{"role": m.role, "content": m.content} for m in history]

    # 4. Stream response
    async def event_generator():
        full_response = ""
        async for chunk in bedrock.stream_response(messages_payload):
            full_response += chunk
            yield chunk
        
        # Save assistant message once streaming is done
        assistant_msg = Message(conversation_id=request.conversation_id, role="assistant", content=full_response)
        db.add(assistant_msg)
        db.commit()

    return StreamingResponse(event_generator(), media_type="text/plain")

@app.get("/history", response_model=List[ConversationSchema])
def get_history(user_name: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(Conversation)
    if user_name:
        query = query.filter(Conversation.user_name == user_name)
    return query.order_by(Conversation.created_at.desc()).all()

@app.get("/history/{conversation_id}", response_model=List[MessageSchema])
def get_conversation_messages(conversation_id: str, db: Session = Depends(get_db)):
    messages = db.query(Message).filter(Message.conversation_id == conversation_id).order_by(Message.timestamp.asc()).all()
    return messages

@app.post("/conversations/new")
def create_new_conversation(user_name: str, db: Session = Depends(get_db)):
    conv_id = str(uuid.uuid4())
    conv = Conversation(id=conv_id, title="New Chat", user_name=user_name)
    db.add(conv)
    db.commit()
    return {"conversation_id": conv_id}

@app.get("/about")
def get_about():
    with open("aboutme.txt", "r") as f:
        return {"about": f.read()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
