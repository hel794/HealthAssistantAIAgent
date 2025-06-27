# HealthAssistantAIAgent

2025北京大学人工智能基础大作业

HealthAssistant智能健康管理师

基于DeepSeek-R1 AI的多代理健康咨询系统，提供专业健康管理建议，支持GUI和CLI两种交互模式。

目录

核心功能
系统架构
安装指南
使用说明
安全机制
输出规范
免责声明
核心功能

双种交互模式

图形界面(GUI)：可视化聊天窗口，支持历史记录管理

命令行界面(CLI)：流式输出模拟，适合快速咨询

专业健康顾问

2个特化AI代理：

温和型：保守建议（temperature=0.7）

创意型：创新方案（temperature=1.2）

健康服务范围

✅ 可提供

膳食营养评估
慢性病生活方式干预
运动处方建议
健康风险评估
❌ 禁止

疾病诊断
处方药建议
替代专业医疗
系统架构

关键模块

模块 功能

agent_service.py 代理服务核心

cli_interface.py 命令行交互逻辑

gui_tkinter.py 图形界面实现

history_manager.py 对话历史存储

preprocessor.py 输入安全过滤

安装指南

1.克隆仓库： 见cores

2.配置环境： 在API.env文件中填入自己的API

SILICONFLOW_API_KEY=您的API密钥

使用说明

1.启动系统 bash python main.py

2.常用命令

命令&功能

/exit 退出系统

/clear 清除当前对话

/switch 切换用户

/params 调整参数

安全机制

三级防护体系：

1.输入过滤

敏感词检测（如医疗禁忌词）
指令注入防护
SQL注入阻断
2.会话监控

安全事件日志
5次违规自动终止会话
3.输出控制

响应内容审查
紧急症状预警
输出规范

系统响应严格遵循JSON格式：

json

{

"content": "回复内容",

"sources": ["《中国居民膳食指南》"],

"advice_type": "general/diet/exercise/warning",

"needs_follow_up": false,

"confidence": 0.95
}

免责声明

本系统提供的健康信息仅供参考，不能替代专业医疗建议。
