# preprocessor.py
import re

class InputPreprocessor:
    def __init__(self):
        # 初始化预处理配置
        self.max_length = 500
        self.sensitive_words = ["暴力", "色情", "政治敏感词"]  # 示例敏感词列表

        self.spelling_corrections = {
            "健慷": "健康", "咨洵": "咨询", "营奍": "营养", 
            "锻练": "锻炼", "保建": "保健", "药勿": "药物"
        }
        
        self.medical_terms = {
            "心跳": "心率", "血压高": "高血压", "血糖高": "高血糖",
            "头疼": "头痛", "拉肚子": "腹泻", "感冒了": "感冒症状",
            "流鼻涕": "鼻溢", "发烧": "发热"
        }
        
        self.sensitive_words = ["自杀", "自残", "暴力", "谋杀", "非法药物", "色情内容", "政治","赌博", 
                                "诈骗", "恐怖主义", "极端主义","仇恨言论", "种族歧视", "性别歧视", "宗教歧视", "网络暴力", "侵犯隐私", "泄露个人信息","假药","毒品"]
        
        # 命令映射
        self.command_mapping = {
            "参数": "/params",
            "退出": "/exit",
            "清除": "/clear",
            "帮助": "/help",
            "保存": "/save",
            "历史": "/history"
        }
        # 指令注入防护配置
        self.command_blacklist = [
            "sudo", "rm", "del", "shutdown", "reboot", "format", 
            "chmod", "chown", "cat", "echo", "wget", "curl",
            "|", "&", ";", "`", "$", ">", "<", "(", ")"
        ]
        self.injection_patterns = [
            r"system\s*\(", r"exec\s*\(", r"os\.", r"subprocess\.",
            r"eval\s*\(", r"execfile\s*\(", r"__import__\s*\(",
            r"pickle\.load", r"yaml\.load", r"json\.loads"
        ]

    def preprocess(self, user_input: str) -> str:
        """
        输入预处理函数
        1. 清理多余空格和特殊字符
        2. 处理常见拼写错误
        3. 标准化医疗术语
        4. 敏感词过滤
        5. 输入长度检查
        6. 命令映射
        """
        # 0. 基本清理
        processed = re.sub(r'\s+', ' ', user_input).strip()

        # 1. 输入长度检查
        if len(processed) > self.max_length:
            return f"[输入错误] 输入过长（{len(processed)}字符），请控制在{self.max_length}字符内"
        
        # 2. 检查是否为命令
        if processed.startswith('/'):
            return processed
        
        # 3. 映射常见命令
        for chinese_cmd, english_cmd in self.command_mapping.items():
            if processed == chinese_cmd:
                return english_cmd
        
        # 4. 替换常见拼写错误
        for wrong, correct in self.spelling_corrections.items():
            processed = processed.replace(wrong, correct)
        
        # 5. 标准化医疗术语
        for term, standard in self.medical_terms.items():
            processed = processed.replace(term, standard)
        
        # 6. 敏感词过滤
        for word in self.sensitive_words:
            if word in processed:
                return f"[敏感内容过滤] 您的问题包含不适当内容，请重新表述"
    
        # 7. 指令注入防护
        # 检查黑名单命令
        for cmd in self.command_blacklist:
            if cmd in processed.lower():
                return f"[安全防护] 检测到潜在危险命令 '{cmd}'，已阻止执行"
        
        # 检查注入模式
        for pattern in self.injection_patterns:
            if re.search(pattern, processed, re.IGNORECASE):
                return f"[安全防护] 检测到潜在代码注入模式，已阻止执行"
        
        # 8. SQL注入防护
        sql_injection_patterns = [
            r"[\s;]--", r"[\s;]#", r"[\s;]/\*", r"union[\s]+select",
            r"drop[\s]+table", r"delete[\s]+from", r"insert[\s]+into",
            r"update[\s]+\w+[\s]+set", r"xp_cmdshell", r"waitfor[\s]+delay"
        ]
        for pattern in sql_injection_patterns:
            if re.search(pattern, processed, re.IGNORECASE):
                return f"[安全防护] 检测到SQL注入尝试，已阻止执行"
        
        return processed

    # def validate(self, text: str) -> tuple:
    #     """统一验证输入，返回 (是否有效, 错误信息)"""
    #     # 检查预处理阶段标记的错误
    #     if text.startswith("[输入错误]") or text.startswith("[敏感内容过滤]"):
    #         # 提取错误信息（去掉前缀）
    #         error_msg = text.split("] ", 1)[-1] if "] " in text else text
    #         return False, error_msg
        
    #     # 检查输入长度（即使预处理已检查，这里作为双重保障）
    #     if len(text) > self.max_length:
    #         return False, f"输入过长（{len(text)}字符），请控制在{self.max_length}字符内"
        
    #     # 检查敏感词（即使预处理已检查，这里作为双重保障）
    #     for word in self.sensitive_words:
    #         if word in text:
    #             return False, f"输入包含敏感词'{word}'，请修改后重试"
        
    #     # 其他可能的验证规则...
    #     return True, ""



    
    def validate(self, text: str) -> tuple:
        """统一验证输入，返回 (是否有效, 错误信息)"""
        # 检查预处理阶段标记的错误
        if text.startswith(("[输入错误]", "[敏感内容过滤]", "[安全防护]")):
            error_type = text.split("]", 1)[0][1:]  # 提取错误类型
            error_msg = text.split("] ", 1)[-1]
            return False, (error_type, error_msg)
    
        # 双重检查敏感词（简化版）
        for word in self.sensitive_words:
            if word in text:
                return False, ("敏感内容过滤", f"输入包含敏感词'{word}'")
        
        # 检查输入长度（即使预处理已检查，这里作为双重保障）
        if len(text) > self.max_length:
            return False, ("输入错误", f"输入过长（{len(text)}字符），请控制在{self.max_length}字符内")
        # 其他验证规则...
        return True, ""

    # def load_config(self, config: dict):
    #     """动态加载配置"""
    #     if 'spelling_corrections' in config:
    #         self.spelling_corrections.update(config['spelling_corrections'])
    #     if 'medical_terms' in config:
    #         self.medical_terms.update(config['medical_terms'])
    #     if 'sensitive_words' in config:
    #         self.sensitive_words.extend(config['sensitive_words'])
    #     if 'command_mapping' in config:
    #         self.command_mapping.update(config['command_mapping'])
    
    