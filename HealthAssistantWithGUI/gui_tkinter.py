# import tkinter as tk
# from tkinter import scrolledtext, messagebox, simpledialog, ttk
# import threading
# import json
# from datetime import datetime
# from PIL import Image, ImageTk
# import io
# import os
# import time

# # 导入您的模块
# from agent import AgentService
# from history_manager import HistoryManager
# from preprocessor import InputPreprocessor
# from camel.types import RoleType

# class HealthAgentGUI:
#     def __init__(self, root, agent_service, history_manager):
#         # self.root = root
#         # root.title("健康管理助手")
#         # root.geometry("900x650")
#         # root.configure(bg="#f0f2f5")
        
#         # # 设置应用图标（可选）
#         # try:
#         #     root.iconbitmap("health_icon.ico")
#         # except:
#         #     pass
        
#         # # 初始化组件
#         # self.init_components()
        
#         # # 初始化服务
#         # self.init_services()
        
#         # # 加载历史记录
#         # self.load_history()
        
#         # # 设置关闭事件
#         # root.protocol("WM_DELETE_WINDOW", self.on_closing)
#         self.root = root
#         # 使用传入的服务而不是自己创建
#         self.agent_service = agent_service
#         self.history_manager = history_manager
        
#         # 初始化预处理器
#         self.preprocessor = InputPreprocessor()
#         self.user_id = "default_user"
#         self.is_processing = False
        
#         # 初始化UI组件
#         self.init_components()
        
#         # 加载历史记录
#         self.load_history()
        
#         # 设置关闭事件
#         root.protocol("WM_DELETE_WINDOW", self.on_closing)

#     # def init_services(self):
#     #     """初始化服务和预处理器"""
#     #     # Agent 配置
#     #     agent_config = {
#     #         "temperature": 0.7,
#     #         "max_tokens": 2048,
#     #         "top_p": 0.9,
#     #         "frequency_penalty": 0.1,
#     #         "presence_penalty": 0.1
#     #     }
        
#     #     system_prompt = (
#     #         "你是一位专业的健康管理师，你的职责是提供健康建议、疾病预防知识和生活方式的指导。"
#     #         "请确保你的回答基于科学证据，并在必要时建议用户咨询专业医生。"
#     #         "如果用户的问题超出健康管理范围，请礼貌地拒绝回答。"
#     #     )
        
#     #     # 初始化服务
#     #     self.preprocessor = InputPreprocessor()
#     #     self.agent_service = AgentService(agent_config, system_prompt)
#     #     self.history_manager = HistoryManager("chat_history.json")
        
#     #     # 设置默认用户ID
#     #     self.user_id = "default_user"
        
#     #     # 状态变量
#     #     self.is_processing = False

#     def init_components(self):
#         """初始化UI组件"""
#         # 创建主框架
#         main_frame = tk.Frame(self.root, bg="#f0f2f5")
#         main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
#         # 标题栏
#         title_frame = tk.Frame(main_frame, bg="#1a73e8", height=50)
#         title_frame.pack(fill=tk.X, pady=(0, 10))
        
#         title_label = tk.Label(
#             title_frame, 
#             text="健康管理助手", 
#             font=("Microsoft YaHei", 16, "bold"), 
#             fg="white", 
#             bg="#1a73e8"
#         )
#         title_label.pack(side=tk.LEFT, padx=20)
        
#         # 状态指示器
#         self.status_var = tk.StringVar(value="就绪")
#         status_label = tk.Label(
#             title_frame, 
#             textvariable=self.status_var, 
#             font=("Microsoft YaHei", 9), 
#             fg="white", 
#             bg="#1a73e8"
#         )
#         status_label.pack(side=tk.RIGHT, padx=20)
        
#         # 聊天历史区域
#         chat_frame = tk.Frame(main_frame, bg="white", bd=1, relief=tk.SUNKEN)
#         chat_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
#         self.chat_history = scrolledtext.ScrolledText(
#             chat_frame, 
#             state='disabled', 
#             wrap=tk.WORD, 
#             font=("Microsoft YaHei", 11),
#             padx=15,
#             pady=10,
#             bg="white",
#             fg="#333333"
#         )
#         self.chat_history.pack(fill=tk.BOTH, expand=True)
        
#         # 配置标签样式
#         self.chat_history.tag_config("user", foreground="#1a73e8", lmargin1=20, lmargin2=20, spacing1=5)
#         self.chat_history.tag_config("agent", foreground="#0d652d", lmargin1=20, lmargin2=20, spacing1=5)
#         self.chat_history.tag_config("error", foreground="#e91e63", lmargin1=20, lmargin2=20)
#         self.chat_history.tag_config("system", foreground="#9c27b0", font=("Microsoft YaHei", 9, "italic"))
        
#         # 输入区域
#         input_frame = tk.Frame(main_frame, bg="#f0f2f5")
#         input_frame.pack(fill=tk.X)
        
#         self.user_input = tk.Text(
#             input_frame, 
#             height=3, 
#             font=("Microsoft YaHei", 11),
#             wrap=tk.WORD,
#             padx=10,
#             pady=8,
#             bg="white",
#             fg="#333333",
#             relief=tk.SOLID,
#             highlightthickness=1,
#             highlightbackground="#ccc",
#             highlightcolor="#1a73e8"
#         )
#         self.user_input.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
#         self.user_input.bind("<Return>", self.on_enter_pressed)
        
#         # 发送按钮
#         send_btn = tk.Button(
#             input_frame, 
#             text="发送", 
#             command=self.send_message,
#             font=("Microsoft YaHei", 10, "bold"),
#             bg="#1a73e8",
#             fg="white",
#             activebackground="#0d5fd6",
#             activeforeground="white",
#             relief=tk.FLAT,
#             padx=15
#         )
#         send_btn.pack(side=tk.RIGHT)
        
#         # 工具栏
#         toolbar = tk.Frame(main_frame, bg="#f0f2f5")
#         toolbar.pack(fill=tk.X, pady=(5, 0))
        
#         # 工具栏按钮
#         buttons = [
#             ("清除历史", self.clear_history),
#             ("保存历史", self.save_history),
#             ("加载历史", self.load_history_dialog),
#             ("设置", self.open_settings),
#             ("导出", self.export_history)
#         ]
        
#         for text, command in buttons:
#             btn = tk.Button(
#                 toolbar, 
#                 text=text, 
#                 command=command,
#                 font=("Microsoft YaHei", 9),
#                 bg="#f8f9fa",
#                 fg="#5f6368",
#                 relief=tk.FLAT
#             )
#             btn.pack(side=tk.LEFT, padx=(0, 5))

#     def display_message(self, sender, message, tag=None):
#         """在聊天历史中显示消息"""
#         self.chat_history.configure(state='normal')
        
#         # 添加发送者标签
#         self.chat_history.insert(tk.END, f"{sender}：\n", sender.lower())
        
#         # 添加消息内容
#         if tag:
#             self.chat_history.insert(tk.END, message + "\n\n", tag)
#         else:
#             self.chat_history.insert(tk.END, message + "\n\n")
        
#         # 滚动到底部
#         self.chat_history.see(tk.END)
#         self.chat_history.configure(state='disabled')

#     def on_enter_pressed(self, event):
#         """处理回车键按下事件"""
#         if event.state == 0:  # 没有Ctrl/Shift
#             self.send_message()
#             return "break"  # 阻止默认换行
#         return None  # 允许默认行为（换行）

#     def send_message(self):
#         """处理发送消息"""
#         if self.is_processing:
#             messagebox.showwarning("请稍候", "正在处理上一个请求，请稍后再试")
#             return
            
#         raw_input = self.user_input.get("1.0", tk.END).strip()
#         if not raw_input:
#             return
        
#         # 清空输入框
#         self.user_input.delete("1.0", tk.END)
        
#         # 预处理输入
#         preprocessed = self.preprocessor.preprocess(raw_input)
        
#         # 验证输入
#         is_valid, error_info = self.preprocessor.validate(preprocessed)
#         if not is_valid:
#             error_type, error_msg = error_info
#             self.display_message("系统", f"{error_type}：{error_msg}", "error")
#             return
        
#         # 显示用户消息
#         self.display_message("您", raw_input, "user")
        
#         # 保存到历史记录
#         self.save_to_history(RoleType.USER, raw_input)
        
#         # 设置处理状态
#         self.is_processing = True
#         self.status_var.set("思考中...")
        
#         # 使用新线程处理AI响应
#         threading.Thread(target=self.get_agent_response, args=(preprocessed,)).start()

#     def get_agent_response(self, preprocessed_input):
#         """获取AI助手的响应"""
#         try:
#             # 获取Agent响应
#             response = self.agent_service.chat(preprocessed_input)
            
#             # 解析响应
#             if isinstance(response, dict) and 'content' in response:
#                 agent_response = response['content']
#                 advice_type = response.get('advice_type', '未知')
#                 self.status_var.set(f"已生成建议 ({advice_type})")
#             else:
#                 agent_response = str(response)
#                 self.status_var.set("已生成回复")
#         except Exception as e:
#             agent_response = f"处理您的请求时出错：{str(e)}"
#             self.status_var.set("处理错误")
        
#         # 在主线程中更新UI
#         self.root.after(0, lambda: self.finalize_response(agent_response))

#     def finalize_response(self, agent_response):
#         """处理并显示最终响应"""
#         # 显示AI响应
#         self.display_message("健康助手", agent_response, "agent")
        
#         # 保存到历史记录
#         self.save_to_history(RoleType.ASSISTANT, agent_response)
        
#         # 重置处理状态
#         self.is_processing = False

#     def save_to_history(self, role, content):
#         """保存消息到历史记录"""
#         # 构建消息记录
#         timestamp = datetime.now().isoformat()
#         message_record = {
#             "role": role,
#             "content": content,
#             "timestamp": timestamp
#         }
        
#         # 获取当前历史记录
#         current_history = self.history_manager.load(self.user_id)
        
#         # 添加新记录
#         current_history.append(message_record)
        
#         # 保存历史
#         self.history_manager.save(self.user_id, current_history)

#     def load_history(self):
#         """加载历史记录并显示"""
#         history = self.history_manager.load(self.user_id)
#         for record in history:
#             role = record["role"]
#             content = record["content"]
            
#             if role == RoleType.USER:
#                 self.display_message("您", content, "user")
#             elif role == RoleType.ASSISTANT:
#                 self.display_message("健康助手", content, "agent")

#     def clear_history(self):
#         """清除当前聊天历史"""
#         if messagebox.askyesno("确认", "确定要清除所有聊天历史吗？"):
#             self.chat_history.configure(state='normal')
#             self.chat_history.delete(1.0, tk.END)
#             self.chat_history.configure(state='disabled')
            
#             # 清除历史记录
#             self.history_manager.clear(self.user_id)
#             self.status_var.set("历史记录已清除")

#     def save_history(self):
#         """保存历史记录到文件"""
#         filename = simpledialog.askstring(
#             "保存历史记录", 
#             "输入文件名：", 
#             initialvalue=f"chat_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
#         )
        
#         if filename:
#             if not filename.endswith('.json'):
#                 filename += '.json'
            
#             history = self.history_manager.load(self.user_id)
#             try:
#                 with open(filename, 'w', encoding='utf-8') as f:
#                     json.dump(history, f, ensure_ascii=False, indent=2)
#                 self.status_var.set(f"历史记录已保存到 {filename}")
#             except Exception as e:
#                 messagebox.showerror("错误", f"保存失败：{str(e)}")

#     def load_history_dialog(self):
#         """加载历史记录对话框"""
#         filename = simpledialog.askstring("加载历史记录", "输入文件名：")
#         if filename and os.path.exists(filename):
#             try:
#                 with open(filename, 'r', encoding='utf-8') as f:
#                     history = json.load(f)
                
#                 # 清除当前历史
#                 self.chat_history.configure(state='normal')
#                 self.chat_history.delete(1.0, tk.END)
#                 self.chat_history.configure(state='disabled')
                
#                 # 保存新历史
#                 self.history_manager.save(self.user_id, history)
                
#                 # 显示新历史
#                 self.load_history()
#                 self.status_var.set(f"已加载历史记录：{filename}")
#             except Exception as e:
#                 messagebox.showerror("错误", f"加载失败：{str(e)}")

#     def export_history(self):
#         """导出历史记录为文本文件"""
#         filename = simpledialog.askstring(
#             "导出历史记录", 
#             "输入文件名：", 
#             initialvalue=f"chat_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
#         )
        
#         if filename:
#             if not filename.endswith('.txt'):
#                 filename += '.txt'
            
#             try:
#                 with open(filename, 'w', encoding='utf-8') as f:
#                     # 获取历史记录
#                     history = self.history_manager.load(self.user_id)
                    
#                     for record in history:
#                         role = "您" if record["role"] == RoleType.USER else "健康助手"
#                         timestamp = record.get("timestamp", "")
                        
#                         if timestamp:
#                             try:
#                                 dt = datetime.fromisoformat(timestamp)
#                                 timestamp_str = dt.strftime("%Y-%m-%d %H:%M:%S")
#                             except:
#                                 timestamp_str = timestamp
#                         else:
#                             timestamp_str = ""
                        
#                         f.write(f"[{timestamp_str}] {role}：\n")
#                         f.write(record["content"] + "\n\n")
                
#                 self.status_var.set(f"历史记录已导出到 {filename}")
#             except Exception as e:
#                 messagebox.showerror("错误", f"导出失败：{str(e)}")

#     def open_settings(self):
#         """打开设置窗口"""
#         settings = tk.Toplevel(self.root)
#         settings.title("设置")
#         settings.geometry("400x300")
#         settings.transient(self.root)
#         settings.grab_set()
        
#         # 设置标签
#         ttk.Label(settings, text="健康助手设置", font=("Microsoft YaHei", 12, "bold")).pack(pady=10)
        
#         # 用户ID设置
#         ttk.Label(settings, text="用户ID：").pack(anchor=tk.W, padx=20, pady=(10, 0))
#         user_id_entry = ttk.Entry(settings)
#         user_id_entry.pack(fill=tk.X, padx=20, pady=5)
#         user_id_entry.insert(0, self.user_id)
        
#         # 敏感词设置
#         ttk.Label(settings, text="敏感词列表（逗号分隔）：").pack(anchor=tk.W, padx=20, pady=(10, 0))
#         sensitive_entry = ttk.Entry(settings)
#         sensitive_entry.pack(fill=tk.X, padx=20, pady=5)
#         sensitive_entry.insert(0, ", ".join(self.preprocessor.sensitive_words))
        
#         # 保存按钮
#         def save_settings():
#             self.user_id = user_id_entry.get().strip() or "default_user"
            
#             # 更新敏感词
#             sensitive_words = [w.strip() for w in sensitive_entry.get().split(",") if w.strip()]
#             self.preprocessor.sensitive_words = sensitive_words
            
#             self.status_var.set("设置已保存")
#             settings.destroy()
        
#         ttk.Button(settings, text="保存", command=save_settings).pack(pady=15)

#     def on_closing(self):
#         """关闭窗口时的处理"""
#         if messagebox.askokcancel("退出", "确定要退出健康助手吗？"):
#             # 保存当前历史
#             self.history_manager.save(self.user_id, self.history_manager.load(self.user_id))
#             self.root.destroy()

# if __name__ == "__main__":
#     root = tk.Tk()
#     app = HealthAgentGUI(root)
#     root.mainloop()

# import tkinter as tk
# from tkinter import scrolledtext, messagebox, simpledialog, ttk
# import threading
# import json
# from datetime import datetime
# from PIL import Image, ImageTk
# import io
# import os
# import time

# # 导入您的模块
# from agent import AgentService
# from history_manager import HistoryManager
# from preprocessor import InputPreprocessor
# from camel.types import RoleType

# class HealthAgentGUI:
#     def __init__(self, root, agent_service, history_manager,initial_user_id):
#         self.root = root
#         # 使用传入的服务而不是自己创建
#         self.agent_service = agent_service
#         self.history_manager = history_manager
        
#         # 初始化预处理器
#         self.preprocessor = InputPreprocessor()
#         self.user_id = initial_user_id
#         self.is_processing = False
        
#         # 设置应用图标（可选）
#         try:
#             root.iconbitmap("health_icon.ico")
#         except Exception:
#             pass  # 忽略图标加载失败
        
#         # 初始化UI组件
#         self.init_components()
        
#         # 加载历史记录
#         self.load_history()
        
#         # 设置关闭事件
#         root.protocol("WM_DELETE_WINDOW", self.on_closing)

#     def init_components(self):
#         """初始化UI组件"""
#         # 创建主框架
#         main_frame = tk.Frame(self.root, bg="#f0f2f5")
#         main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
#         # 标题栏
#         title_frame = tk.Frame(main_frame, bg="#1a73e8", height=50)
#         title_frame.pack(fill=tk.X, pady=(0, 10))
        
#         title_label = tk.Label(
#             title_frame, 
#             text="健康管理助手", 
#             font=("Microsoft YaHei", 16, "bold"), 
#             fg="white", 
#             bg="#1a73e8"
#         )
#         title_label.pack(side=tk.LEFT, padx=20)
        
#         # 状态指示器
#         self.status_var = tk.StringVar(value="就绪")
#         status_label = tk.Label(
#             title_frame, 
#             textvariable=self.status_var, 
#             font=("Microsoft YaHei", 9), 
#             fg="white", 
#             bg="#1a73e8"
#         )
#         status_label.pack(side=tk.RIGHT, padx=20)
        
#         # 聊天历史区域
#         chat_frame = tk.Frame(main_frame, bg="white", bd=1, relief=tk.SUNKEN)
#         chat_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
#         self.chat_history = scrolledtext.ScrolledText(
#             chat_frame, 
#             state='disabled', 
#             wrap=tk.WORD, 
#             font=("Microsoft YaHei", 11),
#             padx=15,
#             pady=10,
#             bg="white",
#             fg="#333333"
#         )
#         self.chat_history.pack(fill=tk.BOTH, expand=True)
        
#         # 配置标签样式
#         self.chat_history.tag_config("user", foreground="#1a73e8", lmargin1=20, lmargin2=20, spacing1=5)
#         self.chat_history.tag_config("agent", foreground="#0d652d", lmargin1=20, lmargin2=20, spacing1=5)
#         self.chat_history.tag_config("error", foreground="#e91e63", lmargin1=20, lmargin2=20)
#         self.chat_history.tag_config("system", foreground="#9c27b0", font=("Microsoft YaHei", 9, "italic"))
        
#         # 输入区域
#         input_frame = tk.Frame(main_frame, bg="#f0f2f5")
#         input_frame.pack(fill=tk.X)
        
#         self.user_input = tk.Text(
#             input_frame, 
#             height=3, 
#             font=("Microsoft YaHei", 11),
#             wrap=tk.WORD,
#             padx=10,
#             pady=8,
#             bg="white",
#             fg="#333333",
#             relief=tk.SOLID,
#             highlightthickness=1,
#             highlightbackground="#ccc",
#             highlightcolor="#1a73e8"
#         )
#         self.user_input.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
#         self.user_input.bind("<Return>", self.on_enter_pressed)
        
#         # 发送按钮
#         send_btn = tk.Button(
#             input_frame, 
#             text="发送", 
#             command=self.send_message,
#             font=("Microsoft YaHei", 10, "bold"),
#             bg="#1a73e8",
#             fg="white",
#             activebackground="#0d5fd6",
#             activeforeground="white",
#             relief=tk.FLAT,
#             padx=15
#         )
#         send_btn.pack(side=tk.RIGHT)
        
#         # 工具栏
#         toolbar = tk.Frame(main_frame, bg="#f0f2f5")
#         toolbar.pack(fill=tk.X, pady=(5, 0))
        
#         # 工具栏按钮
#         buttons = [
#             ("清除历史", self.clear_history),
#             ("保存历史", self.save_history),
#             ("加载历史", self.load_history_dialog),
#             ("设置", self.open_settings),
#             ("导出", self.export_history)
#         ]
        
#         for text, command in buttons:
#             btn = tk.Button(
#                 toolbar, 
#                 text=text, 
#                 command=command,
#                 font=("Microsoft YaHei", 9),
#                 bg="#f8f9fa",
#                 fg="#5f6368",
#                 relief=tk.FLAT
#             )
#             btn.pack(side=tk.LEFT, padx=(0, 5))

#     def display_message(self, sender, message, tag=None):
#         """在聊天历史中显示消息"""
#         self.chat_history.configure(state='normal')
        
#         # 添加发送者标签
#         self.chat_history.insert(tk.END, f"{sender}：\n", sender.lower())
        
#         # 添加消息内容
#         if tag:
#             self.chat_history.insert(tk.END, message + "\n\n", tag)
#         else:
#             self.chat_history.insert(tk.END, message + "\n\n")
        
#         # 滚动到底部
#         self.chat_history.see(tk.END)
#         self.chat_history.configure(state='disabled')

#     def on_enter_pressed(self, event):
#         """处理回车键按下事件"""
#         if event.state == 0:  # 没有Ctrl/Shift
#             self.send_message()
#             return "break"  # 阻止默认换行
#         return None  # 允许默认行为（换行）

#     def send_message(self):
#         """处理发送消息"""
#         if self.is_processing:
#             messagebox.showwarning("请稍候", "正在处理上一个请求，请稍后再试")
#             return
            
#         raw_input = self.user_input.get("1.0", tk.END).strip()
#         if not raw_input:
#             return
        
#         # 清空输入框
#         self.user_input.delete("1.0", tk.END)
        
#         # 预处理输入
#         preprocessed = self.preprocessor.preprocess(raw_input)
        
#         # 验证输入
#         is_valid, error_info = self.preprocessor.validate(preprocessed)
#         if not is_valid:
#             error_type, error_msg = error_info
#             self.display_message("系统", f"{error_type}：{error_msg}", "error")
#             return
        
#         # 显示用户消息
#         self.display_message("您", raw_input, "user")
        
#         # 保存到历史记录
#         self.save_to_history(RoleType.USER, raw_input)
        
#         # 设置处理状态
#         self.is_processing = True
#         self.status_var.set("思考中...")
        
#         # 使用新线程处理AI响应
#         threading.Thread(target=self.get_agent_response, args=(preprocessed,)).start()

#     def get_agent_response(self, preprocessed_input):
#         """获取AI助手的响应"""
#         try:
#             # 获取Agent响应
#             response = self.agent_service.chat(preprocessed_input)
            
#             # 解析响应
#             if isinstance(response, dict) and 'content' in response:
#                 agent_response = response['content']
#                 advice_type = response.get('advice_type', '未知')
#                 self.status_var.set(f"已生成建议 ({advice_type})")
#             else:
#                 agent_response = str(response)
#                 self.status_var.set("已生成回复")
#         except Exception as e:
#             agent_response = f"处理您的请求时出错：{str(e)}"
#             self.status_var.set("处理错误")
        
#         # 在主线程中更新UI
#         self.root.after(0, lambda: self.finalize_response(agent_response))

#     def finalize_response(self, agent_response):
#         """处理并显示最终响应"""
#         # 显示AI响应
#         self.display_message("健康助手", agent_response, "agent")
        
#         # 保存到历史记录
#         self.save_to_history(RoleType.ASSISTANT, agent_response)
        
#         # 重置处理状态
#         self.is_processing = False

#     def save_to_history(self, role, content):
#         """保存消息到历史记录"""
#         # 构建消息记录
#         timestamp = datetime.now().isoformat()
#         message_record = {
#             "role": role,
#             "content": content,
#             "timestamp": timestamp
#         }
        
#         # 获取当前历史记录
#         current_history = self.history_manager.load(self.user_id)
        
#         # 添加新记录
#         current_history.append(message_record)
        
#         # 保存历史
#         self.history_manager.save(self.user_id, current_history)

#     def load_history(self):
#         """加载当前用户的历史记录并显示"""
#         history = self.history_manager.load(self.user_id)
#         for record in history:
#             role = record["role"]
#             content = record["content"]
            
#             if role == RoleType.USER:
#                 self.display_message("您", content, "user")
#             elif role == RoleType.ASSISTANT:
#                 self.display_message("健康助手", content, "agent")

    


#     def clear_history(self):
#         """清除当前聊天历史"""
#         if messagebox.askyesno("确认", "确定要清除所有聊天历史吗？"):
#             self.chat_history.configure(state='normal')
#             self.chat_history.delete(1.0, tk.END)
#             self.chat_history.configure(state='disabled')
            
#             # 清除历史记录
#             self.history_manager.clear(self.user_id)
#             self.status_var.set("历史记录已清除")

#     def save_history(self):
#         """保存历史记录到文件"""
#         filename = simpledialog.askstring(
#             "保存历史记录", 
#             "输入文件名：", 
#             initialvalue=f"chat_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
#         )
        
#         if filename:
#             if not filename.endswith('.json'):
#                 filename += '.json'
            
#             history = self.history_manager.load(self.user_id)
#             try:
#                 with open(filename, 'w', encoding='utf-8') as f:
#                     json.dump(history, f, ensure_ascii=False, indent=2)
#                 self.status_var.set(f"历史记录已保存到 {filename}")
#             except Exception as e:
#                 messagebox.showerror("错误", f"保存失败：{str(e)}")

#     def load_history_dialog(self):
#         """加载历史记录对话框"""
#         filename = simpledialog.askstring("加载历史记录", "输入文件名：")
#         if filename and os.path.exists(filename):
#             try:
#                 with open(filename, 'r', encoding='utf-8') as f:
#                     history = json.load(f)
                
#                 # 清除当前历史
#                 self.chat_history.configure(state='normal')
#                 self.chat_history.delete(1.0, tk.END)
#                 self.chat_history.configure(state='disabled')
                
#                 # 保存新历史
#                 self.history_manager.save(self.user_id, history)
                
#                 # 显示新历史
#                 self.load_history()
#                 self.status_var.set(f"已加载历史记录：{filename}")
#             except Exception as e:
#                 messagebox.showerror("错误", f"加载失败：{str(e)}")

#     def export_history(self):
#         """导出历史记录为文本文件"""
#         filename = simpledialog.askstring(
#             "导出历史记录", 
#             "输入文件名：", 
#             initialvalue=f"chat_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
#         )
        
#         if filename:
#             if not filename.endswith('.txt'):
#                 filename += '.txt'
            
#             try:
#                 with open(filename, 'w', encoding='utf-8') as f:
#                     # 获取历史记录
#                     history = self.history_manager.load(self.user_id)
                    
#                     for record in history:
#                         role = "您" if record["role"] == RoleType.USER else "健康助手"
#                         timestamp = record.get("timestamp", "")
                        
#                         if timestamp:
#                             try:
#                                 dt = datetime.fromisoformat(timestamp)
#                                 timestamp_str = dt.strftime("%Y-%m-%d %H:%M:%S")
#                             except:
#                                 timestamp_str = timestamp
#                         else:
#                             timestamp_str = ""
                        
#                         f.write(f"[{timestamp_str}] {role}：\n")
#                         f.write(record["content"] + "\n\n")
                
#                 self.status_var.set(f"历史记录已导出到 {filename}")
#             except Exception as e:
#                 messagebox.showerror("错误", f"导出失败：{str(e)}")

#     def open_settings(self):
#         """打开设置窗口"""
#         settings = tk.Toplevel(self.root)
#         settings.title("设置")
#         settings.geometry("400x300")
#         settings.transient(self.root)
#         settings.grab_set()
        
#         # 设置标签
#         ttk.Label(settings, text="健康助手设置", font=("Microsoft YaHei", 12, "bold")).pack(pady=10)
        
#         # 用户ID设置
#         ttk.Label(settings, text="用户ID：").pack(anchor=tk.W, padx=20, pady=(10, 0))
#         user_id_entry = ttk.Entry(settings)
#         user_id_entry.pack(fill=tk.X, padx=20, pady=5)
#         user_id_entry.insert(0, self.user_id)
        
#         # # 敏感词设置
#         # ttk.Label(settings, text="敏感词列表（逗号分隔）：").pack(anchor=tk.W, padx=20, pady=(10, 0))
#         # sensitive_entry = ttk.Entry(settings)
#         # sensitive_entry.pack(fill=tk.X, padx=20, pady=5)
#         # sensitive_entry.insert(0, ", ".join(self.preprocessor.sensitive_words))
        
#         # 保存按钮
#         def save_settings():
#             new_user_id = user_id_entry.get().strip() or "default_user"
#             #self.user_id = user_id_entry.get().strip() or "default_user"
#             # 更新敏感词
#             # sensitive_words = [w.strip() for w in sensitive_entry.get().split(",") if w.strip()]
#             # self.preprocessor.sensitive_words = sensitive_words
            
#             # self.status_var.set("设置已保存")
#             # 如果用户ID发生变化
#             if new_user_id != self.user_id:
#                 # 保存当前用户的历史记录
#                 self.history_manager.save(self.user_id, self.history_manager.load(self.user_id))
                
#                 # 更新用户ID
#                 self.user_id = new_user_id
                
#                 # 清除当前聊天显示
#                 self.chat_history.configure(state='normal')
#                 self.chat_history.delete(1.0, tk.END)
#                 self.chat_history.configure(state='disabled')
                
#                 # 加载新用户的历史记录
#                 self.load_history()
#                 self.status_var.set(f"已切换到用户: {self.user_id}")
#             else:
#                 self.status_var.set("设置已保存")
#             settings.destroy()
        
#         ttk.Button(settings, text="保存", command=save_settings).pack(pady=15)

#     def on_closing(self):
#         """关闭窗口时的处理"""
#         if messagebox.askokcancel("退出", "确定要退出健康助手吗？"):
#             # 保存当前历史
#             self.history_manager.save(self.user_id, self.history_manager.load(self.user_id))
#             self.root.destroy()