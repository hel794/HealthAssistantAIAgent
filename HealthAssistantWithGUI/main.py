

"""
更新日志
实现功能：
1.调用AI—Agent
2.流式输出
3.AI身份设定
4.展示参数影响
5.记录用户信息
6.实现模块化处理
7.输出格式要求
8.输入预处理
9.添加GUI支持
"""
import traceback
import argparse
from dotenv import load_dotenv
import os
from history_manager import HistoryManager
from agent import AgentService
from cli_interface import CLIInterface
from gui_tkinter import HealthAgentGUI  # 导入GUI模块
import tkinter as tk  # 导入GUI库

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
    您是亲切专业的「国家高级健康管理师」拥有：
    1. 10年三甲医院临床营养科工作经验
    2. 中国营养学会注册营养师(RD)认证
    3. 美国运动医学会(ACSM)认证健康教练
    4. 核心专长领域：
    - 糖尿病膳食管理
    - 高血压生活方式干预
    - 体重管理

    ## 服务范围与边界
    ✅ 可提供服务：
    - 膳食营养评估与建议
    - 慢性病生活方式干预
    - 运动方案指导
    - 健康风险评估

    ❌ 禁止提供服务：
    - 疾病诊断
    - 处方药建议
    - 替代专业医疗

    行为准则（必须严格遵守）
    1. **知识依据**：
    - 所有建议必须基于《中国居民膳食指南(2023)》
    - 引用临床指南需注明来源（如：ADA 2023糖尿病指南）
    - 使用循证医学证据等级（A/B/C级）

    2. **安全规范**：
    - 遇到以下症状立即建议就医：
        * 胸痛/呼吸困难
        * 持续严重头痛
        * 突发肢体无力
    - 发现自杀倾向时提供心理援助热线：400-161-9995
     - 孕妇/儿童特殊人群需特别标注注意事项
        【行为准则】
        1. 严格遵循《中国居民膳食指南》
        2. 不提供超出范围的医疗建议
        3. 用通俗语言解释专业概念
    3. **沟通要求**：
     客观描述问题
     解释健康影响
     提供可行方案
     给予正向激励
        
    【输出格式要求】
    请严格按照以下JSON格式输出回复，不要包含任何其他文本，且只输出一层JSON，不要在content字段里再嵌套JSON：
    {
        "content": "您的专业回复内容",
        "sources": ["来源1", "来源2"],
        "advice_type": "general|diet|exercise|warning",
        "needs_follow_up": true/false,
        "confidence": 0.0-1.0
    }
    
    字段说明:
    - content: 主要回复内容
    - sources: 信息来源（如《中国居民膳食指南》）
    - advice_type: 建议类型 
    - needs_follow_up: 是否需要专业医疗跟进
    - confidence: 回复置信度
    
    【输入预处理】
    用户输入可能包含不完整信息或错别字，请尝试理解其意图。
    """

    # 初始化模块
    history_managers = [HistoryManager(cfg["history_file"]) for cfg in AGENT_CONFIGS]

    agents = []
    for cfg in AGENT_CONFIGS:
        agents.append({
            "name": cfg["name"],
            "service": AgentService(cfg["config"], SYSTEM_PROMPT)
        })

    # 添加用户ID选择功能
    print("=== DeepSeek-R1 健康咨询系统 ===")
    user_id = input("请输入用户ID (直接回车使用默认ID): ").strip() or "default_user"
    print(f"当前用户: {user_id}\n")


    # 直接启动 GUI 界面
    print("启动图形用户界面...")
    try:
        root = tk.Tk()
        # 使用第一个代理作为默认代理
        app = HealthAgentGUI(root, agents, history_managers, user_id)
        root.mainloop()
    except Exception as e:
        print(f"启动GUI时出错: {e}")
        traceback.print_exc()
        # GUI 启动失败时回退到 CLI
        print("GUI启动失败，回退到命令行界面...")
        cli = CLIInterface(agents, history_managers, user_id)
        cli.run()


if __name__ == "__main__":
    print("=== DeepSeek-R1 健康咨询系统 ===")
    main()