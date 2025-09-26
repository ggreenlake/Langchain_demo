from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Optional
from datetime import datetime, timezone
from services.ChatService import ChatService
from acfilter.acfilter import ACDetector
import requests

chat_service = ChatService()
ac_detector = ACDetector()

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

app = FastAPI(title="Chat API", version="1.0.1")

def contains_sensitive_words(text: str) -> bool:
    """检测是否包含敏感词"""
    return ac_detector.has_sensitive_words(text)

@app.post("/chat", response_model=ChatResponse)
def chat_endpoint(req: ChatRequest):
    user_input = req.content.message  

    if contains_sensitive_words(user_input):
        raise HTTPException(
            status_code=422,  # 不合法的内容
            detail="UNSUITABLE_CONTENT",
            headers={
                "Error-Message": "Something is wrong.",
                "Timestamp":datetime.now().astimezone(timezone.utc).isoformat()

            }
        )  


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
        timestamp = datetime.now().astimezone(timezone.utc).isoformat()
    )
