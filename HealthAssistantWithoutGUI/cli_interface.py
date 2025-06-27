import time
import textwrap
from typing import List
from datetime import datetime
from camel.types import RoleType
from history_manager import HistoryManager
from schemas import HealthInputSchema, HealthOutputSchema, validate_input, validate_output
import json
from preprocessor import InputPreprocessor  # 引入预处理模块
import re
import ast
import operator as op

class CLIInterface:
    def __init__(self, agents: List[dict], history_managers: List[HistoryManager]):
        """
        agents: [{"name": str, "service": AgentService}, ...]
        history_managers: [HistoryManager, ...]
        """
        self.agents = agents
        self.history_managers = history_managers
        self.preprocessor = InputPreprocessor()
        self.security_log = []  # 安全日志
        self.security_log_file = "security_events.log"  # 新增日志文件
        self.SECURITY_THRESHOLD = 5  # 5次安全事件后触发终止
    
    def safe_execute(self, func, *args, **kwargs):
        """安全执行函数，限制潜在危险操作"""
        try:
            return func(*args, **kwargs)
        except Exception as e:
            # 记录详细错误但只返回通用信息
            error_msg = f"安全执行错误: {type(e).__name__}: {str(e)}"
            self.log_security_event("执行错误", str(args), error_msg)
            return "抱歉，处理您的请求时遇到问题"
    
    def log_security_event(self, event_type: str, user_input: str, details: str):
        """记录安全事件到日志文件和内存"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {event_type}: {details}\nUser Input: '{user_input}'\n"
        
        # 添加到内存日志
        self.security_log.append(log_entry)
        
        # 写入文件
        try:
            with open(self.security_log_file, "a", encoding="utf-8") as f:
                f.write(log_entry + "\n")
        except Exception as e:
            print(f"⚠️ 安全日志写入失败: {str(e)}")

    # def simulate_streaming(self, text: str, speed: float = 0.03):
    #     """模拟流式输出"""
    #     for line in textwrap.wrap(text, width=80):
    #         for char in line:
    #             print(char, end='', flush=True)
    #             time.sleep(speed)
    #         print()
    #         time.sleep(speed * 2)

    #模拟流式输出，支持换行符
    def simulate_streaming(self, text: str, speed: float = 0.03):
        """模拟流式输出，支持换行符"""
        # 先按换行符分割成多个段落
        paragraphs = text.split('\n')
        for para in paragraphs:
            # 对每个段落进行自动换行处理
            wrapped_lines = textwrap.wrap(para, width=80)
            if not wrapped_lines:  # 空段落，输出空行
                print()
                time.sleep(speed * 2)
                continue
            for line in wrapped_lines:
                for char in line:
                    print(char, end='', flush=True)
                    time.sleep(speed)
                print()  # 结束一行
                time.sleep(speed * 2)

    # def display_output(self, output: HealthOutputSchema):
    #     """完整显示自然文本格式"""
    #     # 创建自然语言格式回复
    #     full_response = f"{output.content}\n\n"
    
    #     if output.sources:
    #         full_response += f"🔍 信息来源: {', '.join(output.sources)}\n"
    
    #     advice_types = {
    #         "general": "💡 一般建议",
    #         "diet": "🍎 饮食建议",
    #         "exercise": "🏃 运动建议",
    #         "warning": "⚠️ 重要提示"
    #     }
    #     full_response += f"{advice_types.get(output.advice_type, '💡 建议')}\n"
    #     if output.needs_follow_up:
    #         full_response += "❗ 建议: 请尽快咨询专业医生\n"
    
    #         full_response += f"📊 置信度: {output.confidence*100:.1f}%"
    
    #     # 流式输出完整内容
    #     self.simulate_streaming(full_response)

    #模拟流式输出，支持换行符
    def display_output(self, output: HealthOutputSchema):
        """完整显示自然文本格式，支持换行"""
        # 创建自然语言格式回复
        full_response = output.content  # 直接使用可能包含换行的内容
        
        # 添加换行分隔的其他信息
        full_response += "\n\n"
        
        if output.sources:
            full_response += f"🔍 信息来源: {', '.join(output.sources)}\n"
        
        advice_types = {
            "general": "💡 一般建议",
            "diet": "🍎 饮食建议",
            "exercise": "🏃 运动建议",
            "warning": "⚠️ 重要提示"
        }
        full_response += f"{advice_types.get(output.advice_type, '💡 建议')}\n"
        
        if output.needs_follow_up:
            full_response += "❗ 建议: 请尽快咨询专业医生\n"
        
        full_response += f"📊 置信度: {output.confidence*100:.1f}%"
        
        # 流式输出完整内容
        self.simulate_streaming(full_response)

    def show_welcome_messages(self, user_id: str, histories: list):
        """显示欢迎消息"""
        for i, agent_info in enumerate(self.agents):
            print(f"\n🤖 {agent_info['name']}: ", end='')
            start_time = time.time()

            prompt = (
                f"用户上次讨论: {histories[i][-1]['content'][:30]}..."
                if histories[i] and histories[i][-1].get('content')
                else "请向新用户问好"
            )

            try:
                response = agent_info["service"].chat(prompt)

                # 处理不同类型的响应
                if isinstance(response, HealthOutputSchema):
                    self.display_output(response)
                    assistant_msg = response.content
                else:
                    self.simulate_streaming(response)
                    assistant_msg = response
                
                # 保存到历史记录
                new_msg = {
                    "role": RoleType.ASSISTANT,
                    "content": assistant_msg,
                    "timestamp": datetime.now().isoformat()
                }
                if not histories[i]:
                    histories[i] = [new_msg]
                else:
                    histories[i].append(new_msg)
                
                self.history_managers[i].save(user_id, histories[i])
                print(f"⏱️ 耗时: {time.time() - start_time:.2f}s")
            except Exception as e:
                print(f"⚠️ 错误: {str(e)}")

    # def process_user_input(self, user_id: str, user_input: str, histories: list):
    #     """处理用户输入并获取AI响应"""
    #     # 构建符合Schema的输入
    #     input_data = {
    #         "user_id": user_id,
    #         "message": user_input,
    #         "temperature": 0.7,  # 默认值
    #         "top_p": 0.9,  # 默认值
    #         "history": [],
    #         "attachments": [] 
    #     }
    
    # # 添加历史记录（如果存在）
    #     for i in range(len(histories)):
    #         if histories[i]:
    #             input_data["history"] = histories[i][-5:]
    #             break
    
    #     try:
    #         # 验证输入格式
    #         validated_input = validate_input(input_data)
    #     except Exception as e:
    #         print(f"⚠️ 输入格式错误: {str(e)}")
    #         return

    #     # 处理每个Agent的响应
    #     for i, agent_info in enumerate(self.agents):
    #         # 添加用户消息
    #         user_msg = {
    #             "role": RoleType.USER,
    #             "content": user_input,
    #             "timestamp": datetime.now().isoformat()
    #         }
    #         histories[i].append(user_msg)

    #         # 构建上下文
    #         context = "\n".join(
    #             f"{'用户' if m['role'] == RoleType.USER else '助手'}: {m['content']}"
    #             for m in histories[i][-6:]
    #         )
    #         full_input = f"对话上下文:\n{context}\n\n请回复: {user_input}"

    #     # 获取回复
    #         print(f"\n🤖 {agent_info['name']}: ", end='')
    #         start_time = time.time()
    #         try:
    #             response = agent_info["service"].chat(full_input)
            
    #             # 处理不同类型的响应
    #             if isinstance(response, HealthOutputSchema):
    #                 self.display_output(response)
    #                 assistant_msg = response.content
    #             else:
    #                 self.simulate_streaming(response)
    #                 assistant_msg = response

    #             # 保存回复
    #             histories[i].append({
    #                 "role": RoleType.ASSISTANT,
    #                 "content": assistant_msg,
    #                 "timestamp": datetime.now().isoformat()
    #             })
    #             self.history_managers[i].save(user_id, histories[i])
    #             print(f"⏱️ 耗时: {time.time() - start_time:.2f}s")
            
    #         except Exception as e:
    #             print(f"⚠️ 请求失败: {str(e)}")
    def process_user_input(self, user_id: str, user_input: str, histories: list):
        """处理用户输入并获取AI响应"""
        
        
        # 处理每个Agent的响应
        for i, agent_info in enumerate(self.agents):
            # 跳过无效代理
            if agent_info.get("service") is None:
                print(f"\n⚠️ {agent_info['name']} 服务不可用")
                continue
            # 添加用户消息
            user_msg = {
                "role": RoleType.USER,
                "content": user_input,
                "timestamp": datetime.now().isoformat()
            }
            histories[i].append(user_msg)

            # 构建上下文
            context = "\n".join(
                f"{'用户' if m['role'] == RoleType.USER else '助手'}: {m['content']}"
                for m in histories[i][-6:]
            )
            full_input = f"对话上下文:\n{context}\n\n请回复: {user_input}"

            # 获取回复
            print(f"\n🤖 {agent_info['name']}: ", end='')
            start_time = time.time()
            try:
                response = agent_info["service"].chat(full_input)
                
                # 处理不同类型的响应
                # if isinstance(response, HealthOutputSchema):
                #     self.display_output(response)
                #     assistant_msg = response.content
                # else:
                #     self.simulate_streaming(response)
                #     assistant_msg = response

                if isinstance(response, HealthOutputSchema):
                    # 检查是否是错误响应
                    if response.advice_type == "warning" and "系统错误" in response.sources:
                        print("⚠️ 检测到API错误响应")
                    
                    self.display_output(response)
                    assistant_msg = response.content
                else:
                    self.simulate_streaming(response)
                    assistant_msg = response

                # 保存回复
                histories[i].append({
                    "role": RoleType.ASSISTANT,
                    "content": assistant_msg,
                    "timestamp": datetime.now().isoformat()
                })
                self.history_managers[i].save(user_id, histories[i])
                print(f"⏱️ 耗时: {time.time() - start_time:.2f}s")
            
            except Exception as e:
                # API调用失败时处理
                error_msg = f"请求失败: {str(e)}"
                print(f"❌ {error_msg}")
                #traceback.print_exc()
                
                # 创建错误响应并显示
                error_response = HealthOutputSchema(
                    content="服务暂时不可用，请稍后再试",
                    advice_type="warning",
                    sources=["系统错误"],
                    needs_follow_up=False,
                    confidence=0.0
                )
                self.display_output(error_response)
                
                # 保存错误响应到历史记录
                histories[i].append({
                    "role": RoleType.ASSISTANT,
                    "content": error_response.content,
                    "timestamp": datetime.now().isoformat()
                })
                self.history_managers[i].save(user_id, histories[i])

    def adjust_parameters(self):
        """调整参数（示例）"""
        print("\n=== 参数调整 ===")
        print("当前不支持调整参数，将在后续版本添加")

    # def show_help(self):
    #     """显示帮助信息"""
    #     help_text = """
    #     === 健康咨询系统帮助 ===
    #     可用命令:
    #       /help 或 帮助 - 显示此帮助信息
    #       /history 或 查看历史 - 显示当前会话的历史记录
    #       /clear 或 清除 - 清除当前会话的历史记录
    #       /params 或 参数 - 调整系统参数
    #       /exit 或 退出 - 退出系统
          
    #     系统说明:
    #     1. 本系统提供两位AI健康管理师咨询服务
    #     2. 第一位AI使用温和参数 (temperature: 0.7)
    #     3. 第二位AI使用创意参数 (temperature: 1.2)
    #     4. 所有对话记录会自动保存
    #     """
    #     self.simulate_streaming(help_text.strip())

    # def show_history(self, histories: list):
    #     """显示当前会话的历史记录"""
    #     if not any(hist for hist in histories):
    #         self.simulate_streaming("当前会话没有历史记录")
    #         return
        
    #     history_text = "=== 当前会话历史记录 ===\n"
        
    #     for i, hist in enumerate(histories):
    #         if hist:
    #             agent_name = self.agents[i]["name"]
    #             history_text += f"\n🤖 {agent_name} 对话记录:\n"
                
    #             for j, msg in enumerate(hist):
    #                 speaker = "👤 你" if msg["role"] == RoleType.USER else "🤖 AI"
    #                 # 格式化时间
    #                 timestamp = datetime.fromisoformat(msg["timestamp"]).strftime("%H:%M:%S")
    #                 # 截断过长的消息
    #                 content = msg["content"]
    #                 if len(content) > 100:
    #                     content = content[:97] + "..."
                    
    #                 history_text += f"{timestamp} {speaker}: {content}\n"
        
    #     self.simulate_streaming(history_text.strip())

    #以下换行
    def show_help(self):
        """显示帮助信息，使用换行符格式化"""
        help_text = """
=== 健康咨询系统帮助 ===

可用命令:

  /help 或 帮助 - 显示此帮助信息
  /history 或 查看历史 - 显示当前会话的历史记录
  /clear 或 清除 - 清除当前会话的历史记录
  /params 或 参数 - 调整系统参数
  /exit 或 退出 - 退出系统

系统说明:

1. 本系统提供两位AI健康管理师咨询服务
2. 第一位AI使用温和参数 (temperature: 0.7)
3. 第二位AI使用创意参数 (temperature: 1.2)
4. 所有对话记录会自动保存
        """.strip()
        self.simulate_streaming(help_text)
    
    def show_history(self, histories: list):
        """显示当前会话的历史记录，使用换行符格式化"""
        if not any(hist for hist in histories):
            self.simulate_streaming("当前会话没有历史记录")
            return
        
        history_text = "=== 当前会话历史记录 ===\n"
        
        for i, hist in enumerate(histories):
            if hist:
                agent_name = self.agents[i]["name"]
                history_text += f"\n🤖 {agent_name} 对话记录:\n"
                
                for j, msg in enumerate(hist):
                    speaker = "👤 你" if msg["role"] == RoleType.USER else "🤖 AI"
                    # 格式化时间
                    timestamp = datetime.fromisoformat(msg["timestamp"]).strftime("%H:%M:%S")
                    # 截断过长的消息
                    content = msg["content"]
                    if len(content) > 100:
                        content = content[:97] + "..."
                    
                    # 添加换行符
                    history_text += f"{timestamp} {speaker}: {content}\n"
        
        self.simulate_streaming(history_text.strip())

    def run(self):
        """主交互循环"""
        print("\n=== 健康管理师咨询系统 ===")
        #print("可用指令:\n  /params - 调整参数\n  /exit - 退出\n  /clear - 清除历史记录")
        print("可用指令:\n  /help - 帮助\n  /history - 查看历史\n  /params - 调整参数\n  /exit - 退出\n  /clear - 清除历史记录")
        user_id = input("请输入用户ID: ").strip() or "default_user"

        # 初始化安全计数器
        security_count = 0  #  每个会话独立的计数器

     # 初始化历史记录
        histories = []
        for i, manager in enumerate(self.history_managers):
            history = manager.load(user_id)
            histories.append(history)
            print(f"{self.agents[i]['name']} 加载历史记录: {len(history)}条")
    

        # 主对话循环
        while True:
            # 如果是新会话，显示欢迎消息
            if not any(hist for hist in histories if hist):
                self.show_welcome_messages(user_id, histories)
        
            try:
                user_input = input("\n👤 你: ").strip()

                original_input = user_input  # 保存原始输入用于日志记录
            
                if not user_input:
                    continue
                
                # 1. 预处理用户输入 - 新增
                processed_input = self.preprocessor.preprocess(user_input)
                
                # 2. 验证预处理结果 - 新增
                is_valid, error_info = self.preprocessor.validate(processed_input)
                #error_type,error_msg=error_info
                if not is_valid:
                    if isinstance(error_info, tuple) and len(error_info) == 2:
                        error_type, error_msg = error_info
                    else:
                    # 处理其他类型的错误信息
                        error_type = "验证错误"
                        error_msg = str(error_info)
                    print(f"⚠️ {error_msg}")
                    if error_type in ["安全防护", "敏感内容过滤"]:
                        self.log_security_event(
                        event_type=error_type,
                        user_input=original_input,
                        details=error_msg
                    )
                        security_count += 1
                        
                        # 检查是否达到阈值 ✅ 使用类属性
                        if security_count >= self.SECURITY_THRESHOLD:
                            print("⛔ 检测到多次安全违规，会话已终止")
                            self.log_security_event(
                                "会话终止", 
                                "多次违规", 
                                f"累计安全事件: {security_count}"
                            )
                            break  # 终止会话
                    continue
                 # 使用处理后的输入
                user_input = processed_input

                if user_input.lower() == '/help':
                    self.show_help()
                    continue
                
                elif user_input.lower() == '/history':
                    self.show_history(histories)
                    continue

                if user_input.lower() in ['/exit', '退出']:
                    for i, manager in enumerate(self.history_managers):
                        manager.save(user_id, histories[i])
                    print("对话已保存，再见！")
                    break

                elif user_input.lower() == '/clear':
                    for manager in self.history_managers:
                        manager.clear(user_id)
                    print("✅ 历史记录已清除")
                    # 重新加载空历史
                    histories = []
                    for i, manager in enumerate(self.history_managers):
                        histories.append(manager.load(user_id))
                    continue
                
                elif user_input.lower() == '/params':
                    self.adjust_parameters()
                    continue
                
                # 处理用户输入
                self.process_user_input(user_id, user_input, histories)
            
            except KeyboardInterrupt:
                print("\n⚠️ 中断检测，正在保存历史记录...")
                for i, manager in enumerate(self.history_managers):
                    manager.save(user_id, histories[i])
                break
            except Exception as e:
                print(f"\n⚠️ 系统错误: {str(e)}")

    