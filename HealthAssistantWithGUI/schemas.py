# schemas.py
from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any
from enum import Enum
import json
import re

class RoleType(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"

class HealthInputSchema(BaseModel):
    user_id: str = Field(..., description="用户唯一标识符")
    message: str = Field(..., min_length=1, max_length=1000, description="用户输入的消息内容")
    temperature: float = Field(0.7, ge=0.0, le=2.0, description="生成文本的随机性控制")
    top_p: float = Field(0.9, ge=0.0, le=1.0, description="生成文本的多样性控制")
    history: List[Dict] = Field([], description="历史对话记录")
    attachments: List[str] = Field([], description="附件列表(图片/文件等)")

    @validator('message')
    def message_contains_no_sensitive_info(cls, v):
        sensitive_keywords = ["信用卡", "密码", "身份证号", "社保号"]
        for keyword in sensitive_keywords:
            if keyword in v:
                raise ValueError(f"消息包含敏感词: {keyword}")
        return v

    @validator('history', each_item=True)
    def validate_history_format(cls, item):
        required_keys = {"role", "content", "timestamp"}
        if not all(key in item for key in required_keys):
            raise ValueError("历史记录格式错误，缺少必要字段")
        return item

class HealthOutputSchema(BaseModel):
    content: str = Field(..., description="AI生成的回复内容")
    sources: List[str] = Field([], description="信息来源引用")
    advice_type: str = Field(..., description="建议类型: general|diet|exercise|warning")
    needs_follow_up: bool = Field(False, description="是否需要跟进咨询")
    confidence: float = Field(0.8, ge=0.0, le=1.0, description="回复置信度")

    def to_json(self) -> str:
        return json.dumps(self.dict(), ensure_ascii=False)

    @validator('content')
    def content_contains_no_medical_advice(cls, v):
        if "处方药" in v or "手术" in v:
            raise ValueError("回复包含不当医疗建议")
        return v

def validate_input(input_data: dict) -> HealthInputSchema:
    return HealthInputSchema(**input_data)

def validate_output(output_data: dict) -> HealthOutputSchema:
    return HealthOutputSchema(**output_data)