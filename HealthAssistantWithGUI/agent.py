# agent_service.py
from camel.agents import ChatAgent
from camel.models import ModelFactory
from camel.types import ModelPlatformType
from camel.messages import BaseMessage
from dotenv import load_dotenv
import os
import traceback
from camel.agents import ChatAgent
from camel.models import ModelFactory
from camel.types import ModelPlatformType, RoleType
from camel.messages import BaseMessage
import time
import json
import os
from datetime import datetime
import textwrap
from typing import Union, List, Dict, Any, cast
import io
from schemas import HealthOutputSchema, validate_output


load_dotenv('API.env')

class AgentService:
    def __init__(self, config: dict, system_prompt: str):
        self.model = ModelFactory.create(
            model_platform=ModelPlatformType.OPENAI_COMPATIBLE_MODEL,
            model_type="deepseek-ai/DeepSeek-R1",
            model_config_dict=config,
            url='https://api.siliconflow.cn',
            api_key=os.getenv("SILICONFLOW_API_KEY")
        )
        self.agent = ChatAgent(
            model=self.model,
            output_language="中文",
            system_message=BaseMessage(
                role_name="system",
                role_type=RoleType.ASSISTANT,
                content=system_prompt,
                meta_dict={"身份": "健康管理师"}
            )
        )

    def chat(self, message: str) -> Union[HealthOutputSchema, str]:
        """发送消息并返回响应"""
        response = self.agent.step(input_message=message)
        raw_content = response.msgs[0].content
        
        # 尝试解析为JSON，如果失败则使用默认格式
        try:
            parsed = json.loads(raw_content)
            # 验证输出格式
            output_schema = validate_output(parsed)
            return output_schema
        except (json.JSONDecodeError, ValueError) as e:
            # 格式不符合时创建默认结构
            default_output = HealthOutputSchema(
                content=raw_content,
                advice_type="general",
                sources=["内部知识库"],
                needs_follow_up=False
            )
            print(f"⚠️ 输出格式错误，使用默认结构: {str(e)}")
            return output_schema

    # def chat(self, user_id: str, message: str, history: list) -> Union[HealthOutputSchema, str]:
    #     """发送消息并返回响应（包含完整的对话历史）"""
    #     # 构建完整的对话上下文
    #     context = self._build_context(history)
        
    #     # 添加当前消息到上下文
    #     full_message = f"{context}\n\n用户最新消息: {message}"
        
    #     response = self.agent.step(input_message=BaseMessage.make_user_message(role_name="user", content=full_message))
    #     raw_content = response.msgs[0].content
        
    #     # 尝试解析为JSON
    #     try:
    #         parsed = json.loads(raw_content)
    #         output_schema = validate_output(parsed)
    #         return output_schema
    #     except (json.JSONDecodeError, ValueError) as e:
    #         # 格式不符合时创建默认结构
    #         default_output = HealthOutputSchema(
    #             content=raw_content,
    #             advice_type="general",
    #             sources=["内部知识库"],
    #             needs_follow_up=False,
    #             confidence=0.8
    #         )
    #         print(f"⚠️ 输出格式错误，使用默认结构: {str(e)}")
    #         return default_output
    
    # def _build_context(self, history: list) -> str:
    #     """构建对话上下文"""
    #     context = "对话历史:\n"
    #     for i, msg in enumerate(history[-5:], 1):  # 只保留最近的5条对话
    #         if msg['role'] == RoleType.USER:
    #             context += f"{i}. 用户: {msg['content']}\n"
    #         else:
    #             context += f"{i}. 助手: {msg['content']}\n"
    #     return context