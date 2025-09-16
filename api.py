from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, Optional
from datetime import datetime
from services.ChatService import ChatService

chat_service = ChatService()

class ChatContent(BaseModel):
    type: str
    message: str

class ChatRequest(BaseModel):
    platform: str
    userId: int
    aiCompanionId: int
    scene: int
    affectionLevel: int
    content: ChatContent
    time: Optional[str]  # 可选，若不传用当前时间

class ChatResponse(BaseModel):
    aiCompanionId: int
    role: str = "assistant"  # 新增字段，默认值为"assistant"
    content: ChatContent     # 修改reply字段为content，并使用ChatContent类型
    timestamp: str           # 新增时间戳字段

app = FastAPI(title="Chat API", version="1.0.0")

@app.post("/chat", response_model=ChatResponse)
def chat_endpoint(req: ChatRequest):
    # 调用 ChatService
    reply = chat_service.chat(
        platform=req.platform,
        user_id=req.userId,
        profile_name=req.aiCompanionId,
        scene_name=req.scene,
        affection_level=req.affectionLevel,
        user_input=req.content.message
    )

    return ChatResponse(
        aiCompanionId=req.aiCompanionId,
        role="assistant",
        content=ChatContent(type="text", message=reply),
        timestamp=datetime.now().isoformat() + "Z"
    )
