import json
import os
import time
from datetime import datetime
from typing import List, Dict, Any
import traceback
from camel.types import RoleType
from dotenv import load_dotenv

class HistoryManager:
    def __init__(self, history_file: str):
        self.history_file = history_file
        self._ensure_file()

    def _ensure_file(self):
        """确保文件存在且有效"""
        if not os.path.exists(self.history_file):
            self._safe_write([])
        else:
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    json.load(f)
            except json.JSONDecodeError:
                self._safe_write([])

    def _safe_write(self, data: List[Dict]):
        """原子写入文件"""
        temp_file = self.history_file + '.tmp'
        try:
            with open(temp_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            if os.path.exists(temp_file):
                os.replace(temp_file, self.history_file)
        except Exception as e:
            print(f"⚠️ 文件写入失败: {str(e)}")

    def save(self, user_id: str, messages: List[Dict[str, Any]]) -> bool:
        """保存聊天历史"""
        try:
            # 转换枚举值为可序列化的值
            serializable = []
            for msg in messages:
                try:
                    m = msg.copy()
                    m["role"] = msg["role"].value
                    serializable.append(m)
                except Exception as e:
                    print(f"⚠️ 消息序列化失败: {str(e)}")
                    continue

            # 读取现有记录
            existing = []
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    existing = json.load(f)
            except json.JSONDecodeError:
                existing = []

            # 更新记录
            updated = False
            for record in existing:
                if isinstance(record, dict) and record.get("user_id") == user_id:
                    record["messages"] = serializable
                    record["last_updated"] = datetime.now().isoformat()
                    updated = True

            if not updated:
                existing.append({
                    "user_id": user_id,
                    "last_updated": datetime.now().isoformat(),
                    "messages": serializable
                })

            self._safe_write(existing)
            return True
        except Exception as e:
            print(f"⚠️ 保存失败: {str(e)}")
            traceback.print_exc()
            return False

    

    def load(self, user_id: str) -> List[Dict[str, Any]]:
        """加载聊天历史"""
        for _ in range(3):  # 重试机制
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    records = json.load(f)

                if not isinstance(records, list):
                    return []

                for record in records:
                    if isinstance(record, dict) and record.get("user_id") == user_id:
                        messages = []
                        for msg in record.get("messages", []):
                            try:
                                m = msg.copy()
                                m["role"] = RoleType(msg["role"])
                                messages.append(m)
                            except ValueError:
                                continue
                        return messages
                return []
            except json.JSONDecodeError:
                time.sleep(0.5)
                continue
            except Exception as e:
                print(f"⚠️ 加载失败: {str(e)}")
                return []
        return []
    
    