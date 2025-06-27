"""
更新日志
6.22 19:35
实现功能：
1.调用AI—Agent
2.流式输出
3.AI身份设定
4.展示参数影响
5.记录用户信息
6.实现模块化处理
7.输出格式要求
8.输入预处理

待实现功能
1.GUI（待定）

"""
import traceback
from camel.agents import ChatAgent
from camel.models import ModelFactory
from dotenv import load_dotenv
import os
from history_manager import HistoryManager
from agent import AgentService
from cli_interface import CLIInterface

load_dotenv('API.env')

def main():
    # 配置
    AGENT_CONFIGS = [
        {
            "name": "AI健康管理师1号(温和)(temperature: 0.7, top_p: 0.9)",
            "config": {"temperature": 0.7, "top_p": 0.9},
            "history_file": "chat_history_1.json"
        },
        {
            "name": "AI健康管理师2号(创意)(temperature: 1.2, top_p: 0.8)",
            "config": {"temperature": 1.2, "top_p": 0.8},
            "history_file": "chat_history_2.json"
        }
    ]

    SYSTEM_PROMPT = """健康管理师身份设定：
    您是国家认证的高级健康管理师，拥有：
    - 10年三甲医院临床营养科经验
    - 中国营养学会注册营养师(RD)
    - 擅长糖尿病/高血压膳食管理

    【行为准则】
    1. 严格遵循《中国居民膳食指南》
    2. 不提供超出范围的医疗建议
    3. 用通俗语言解释专业概念
    
    【输出格式要求】
    请严格按照以下JSON格式输出回复，不要包含任何其他文本，且只输出一层JSON，不要在content字段里再嵌套JSON：
    {
        "content": "您的专业回复内容",
        "sources": ["来源1", "来源2"],
        "advice_type": "general|diet|exercise|warning",
        "needs_follow_up": true/false,
        "confidence": 0.0-1.0
    }

    【内容格式要求】
    1. 在content字段中可以使用\\n表示换行
    2. 建议将内容分段，每段不超过3-4个句子
    3. 重要信息前使用空行分隔
    
    字段说明:
    - content: 主要回复内容
    - sources: 信息来源（如《中国居民膳食指南》）
    - advice_type: 建议类型 
    - needs_follow_up: 是否需要专业医疗跟进
    - confidence: 回复置信度
    
    【输入预处理】
    用户输入可能包含不完整信息或错别字，请尝试理解其意图。

    【系统命令说明】
    用户可以使用以下命令：
    - /help 或 "帮助": 查看可用命令和系统信息
    - /history 或 "查看历史": 显示当前会话的历史记录
    - /clear 或 "清除": 清除当前会话的历史记录
    - /params 或 "参数": 调整系统参数
    - /exit 或 "退出": 退出系统
    
    当用户使用这些命令时，请勿生成任何回复内容，直接返回空JSON。
    """

    API_KEY = os.getenv("SILICONFLOW_API_KEY") # 替换为实际API密钥
    if not API_KEY:
        print("❌ 错误: 未找到SILICONFLOW_API_KEY环境变量")
        print("请检查API.env文件是否包含有效的API密钥")
        return
    
    # 初始化模块
    history_managers = [HistoryManager(cfg["history_file"]) for cfg in AGENT_CONFIGS]

    agents = []
    for cfg in AGENT_CONFIGS:
        agents.append({
            "name": cfg["name"],
            "service": AgentService(cfg["config"], SYSTEM_PROMPT)
        })

    # 启动界面
    cli = CLIInterface(agents, history_managers)
    cli.run()


if __name__ == "__main__":
    print("=== DeepSeek-R1 健康咨询系统 ===")
    main()





"""
更新日志
6.24 添加GUI支持
"""
# import traceback
# import argparse
# from dotenv import load_dotenv
# import os
# from history_manager import HistoryManager
# from agent import AgentService
# from cli_interface import CLIInterface
# from gui_tkinter import HealthAgentGUI  # 导入GUI模块
# import tkinter as tk  # 导入GUI库

# load_dotenv('API.env')

# def main():
#     # 配置
#     AGENT_CONFIGS = [
#         {
#             "name": "AI健康管理师1号(温和)(temperature: 0.7, top_p: 0.9)",
#             "config": {"temperature": 0.7, "top_p": 0.9},
#             "history_file": "chat_history_1.json"
#         },
#         {
#             "name": "AI健康管理师2号(创意)(temperature: 1.2, top_p: 0.8)",
#             "config": {"temperature": 1.2, "top_p": 0.8},
#             "history_file": "chat_history_2.json"
#         }
#     ]

#     SYSTEM_PROMPT = """健康管理师身份设定：
#     您是国家认证的高级健康管理师，拥有：
#     - 10年三甲医院临床营养科经验
#     - 中国营养学会注册营养师(RD)
#     - 擅长糖尿病/高血压膳食管理

#     【行为准则】
#     1. 严格遵循《中国居民膳食指南》
#     2. 不提供超出范围的医疗建议
#     3. 用通俗语言解释专业概念
    
#     【输出格式要求】
#     请严格按照以下JSON格式输出回复，不要包含任何其他文本，且只输出一层JSON，不要在content字段里再嵌套JSON：
#     {
#         "content": "您的专业回复内容",
#         "sources": ["来源1", "来源2"],
#         "advice_type": "general|diet|exercise|warning",
#         "needs_follow_up": true/false,
#         "confidence": 0.0-1.0
#     }
    
#     字段说明:
#     - content: 主要回复内容
#     - sources: 信息来源（如《中国居民膳食指南》）
#     - advice_type: 建议类型 
#     - needs_follow_up: 是否需要专业医疗跟进
#     - confidence: 回复置信度
    
#     【输入预处理】
#     用户输入可能包含不完整信息或错别字，请尝试理解其意图。
#     """

#     # 初始化模块
#     history_managers = [HistoryManager(cfg["history_file"]) for cfg in AGENT_CONFIGS]

#     agents = []
#     for cfg in AGENT_CONFIGS:
#         agents.append({
#             "name": cfg["name"],
#             "service": AgentService(cfg["config"], SYSTEM_PROMPT)
#         })

#     # 添加用户ID选择功能
#     print("=== DeepSeek-R1 健康咨询系统 ===")
#     user_id = input("请输入用户ID (直接回车使用默认ID): ").strip() or "default_user"
#     print(f"当前用户: {user_id}\n")


#     # 直接启动 GUI 界面
#     print("启动图形用户界面...")
#     try:
#         root = tk.Tk()
#         # 使用第一个代理作为默认代理
#         app = HealthAgentGUI(root, agents[0]["service"], history_managers[0], user_id)
#         root.mainloop()
#     except Exception as e:
#         print(f"启动GUI时出错: {e}")
#         traceback.print_exc()
#         # GUI 启动失败时回退到 CLI
#         print("GUI启动失败，回退到命令行界面...")
#         cli = CLIInterface(agents, history_managers, user_id)
#         cli.run()


# if __name__ == "__main__":
#     print("=== DeepSeek-R1 健康咨询系统 ===")
#     main()