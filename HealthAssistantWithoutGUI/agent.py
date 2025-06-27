# agent.py
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
#from utils.retry import retry_on_exception
import logging

load_dotenv('API.env')
# 抑制 camel 和 openai 的详细错误日志
logging.getLogger("camel").setLevel(logging.CRITICAL)
logging.getLogger("openai").setLevel(logging.CRITICAL)

class AgentService:
    def __init__(self, config: dict, system_prompt: str):
        api_key = os.getenv("SILICONFLOW_API_KEY")
        if not api_key:
            raise ValueError("SILICONFLOW_API_KEY环境变量未设置，请检查API.env文件")
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

    # def chat(self, message: str) -> Union[HealthOutputSchema, str]:
    #     """发送消息并返回响应"""
    #     # 如果是系统命令，直接返回空响应
    #     if message.strip().lower() in ['/help', '/history', '/clear', '/params', '/exit']:
    #         return HealthOutputSchema(
    #             content="",
    #             advice_type="general",
    #             sources=[],
    #             needs_follow_up=False,
    #             confidence=1.0
    #         )
        

    #     response = self.agent.step(input_message=message)
    #     raw_content = response.msgs[0].content
        
    #     # 尝试解析为JSON，如果失败则使用默认格式
    #     try:
    #         parsed = json.loads(raw_content)

    #         # 在content中添加换行符处理
    #         if 'content' in parsed and isinstance(parsed['content'], str):
    #             # 将\n转换为实际的换行符
    #             parsed['content'] = parsed['content'].replace('\\n', '\n')

    #         # 验证输出格式
    #         output_schema = validate_output(parsed)
    #         return output_schema
    #     except (json.JSONDecodeError, ValueError) as e:
    #         # 格式不符合时创建默认结构
    #         default_output = HealthOutputSchema(
    #             content=raw_content.replace('\\n', '\n'),  # 添加换行符处理
    #             advice_type="general",
    #             sources=["内部知识库"],
    #             needs_follow_up=False
    #         )
    #         print(f"⚠️ 输出格式错误，使用默认结构: {str(e)}")
    #         return default_output
    def chat(self, message: str) -> Union[HealthOutputSchema, str]:
        """发送消息并返回响应"""
        # 如果是系统命令，直接返回空响应
        if message.strip().lower() in ['/help', '/history', '/clear', '/params', '/exit']:
            return HealthOutputSchema(
                content="",
                advice_type="general",
                sources=[],
                needs_follow_up=False,
                confidence=1.0
            )
        
        try:
            # API调用尝试
            response = self.agent.step(input_message=message)
            raw_content = response.msgs[0].content
            
            # 尝试解析为JSON
            try:
                parsed = json.loads(raw_content)

                # 在content中添加换行符处理
                if 'content' in parsed and isinstance(parsed['content'], str):
                    parsed['content'] = parsed['content'].replace('\\n', '\n')

                # 验证输出格式
                output_schema = validate_output(parsed)
                return output_schema
            except (json.JSONDecodeError, ValueError) as e:
                # 格式不符合时创建默认结构
                default_output = HealthOutputSchema(
                    content=raw_content.replace('\\n', '\n'),
                    advice_type="general",
                    sources=["内部知识库"],
                    needs_follow_up=False
                )
                print(f"⚠️ 输出格式错误，使用默认结构: {str(e)}")
                return default_output
        
        except Exception as e:
            # API调用失败时的异常处理
            print(f"❌ API调用异常: {str(e)}")
            # traceback.print_exc()  # 调试时取消注释
            
            # 返回错误响应
            return HealthOutputSchema(
                content="服务暂时不可用，请稍后再试",
                advice_type="warning",
                sources=["系统错误"],
                needs_follow_up=False,
                confidence=0.0
            )