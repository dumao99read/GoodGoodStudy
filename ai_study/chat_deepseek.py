import os

import requests
import json
from typing import List, Dict

from tools.file_setting import get_project_root
from tools.read_config import read_body_para


class DeepSeekChat:
    def __init__(self, api_key: str, base_url: str = "https://api.deepseek.com"):
        """
        初始化DeepSeek聊天客户端

        Args:
            api_key: DeepSeek API密钥
            base_url: API基础URL，默认为官方地址
        """
        self.api_key = api_key
        self.base_url = base_url
        self.conversation_history: List[Dict] = []

    def add_message(self, role: str, content: str):
        """添加消息到对话历史"""
        self.conversation_history.append({
            "role": role,
            "content": content
        })

    def chat(self, user_input: str, model: str = "deepseek-chat", max_tokens: int = 2048,
             temperature: float = 0.7) -> str:
        """
        发送消息并获取回复

        Args:
            user_input: 用户输入
            model: 使用的模型
            max_tokens: 最大token数
            temperature: 温度参数

        Returns:
            AI的回复内容
        """
        # 添加用户消息到历史
        self.add_message("user", user_input)

        # 准备请求数据
        url = f"{self.base_url}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        data = {
            "model": model,
            "messages": self.conversation_history,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "stream": False
        }

        try:
            # 发送请求
            response = requests.post(url, headers=headers, json=data, timeout=30)
            response.raise_for_status()

            # 解析响应
            result = response.json()
            ai_response = result["choices"][0]["message"]["content"]

            # 添加AI回复到历史
            self.add_message("assistant", ai_response)

            return ai_response

        except requests.exceptions.RequestException as e:
            return f"请求出错: {str(e)}"
        except KeyError as e:
            return f"解析响应出错: {str(e)}"
        except Exception as e:
            return f"未知错误: {str(e)}"

    def clear_history(self):
        """清空对话历史"""
        self.conversation_history = []

    def get_history(self) -> List[Dict]:
        """获取当前对话历史"""
        return self.conversation_history.copy()

    def save_history(self, filepath: str):
        """保存对话历史到文件"""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.conversation_history, f, ensure_ascii=False, indent=2)

    def load_history(self, filepath: str):
        """从文件加载对话历史"""
        with open(filepath, 'r', encoding='utf-8') as f:
            self.conversation_history = json.load(f)


def main():
    # 配置你的API密钥
    project_base = get_project_root()
    config_file = os.path.join(project_base, 'config/config.json')
    temp_dict = read_body_para(config_file)
    API_KEY = temp_dict.get("apiKey")

    # 创建聊天客户端
    chat_client = DeepSeekChat(api_key=API_KEY)

    print("=" * 50)
    print("DeepSeek 聊天助手")
    print("输入 'quit' 或 'exit' 退出")
    print("输入 'clear' 清空对话历史")
    print("输入 'history' 查看对话历史")
    print("=" * 50)

    while True:
        try:
            # 获取用户输入
            user_input = input("\n你: ").strip()

            # 退出命令
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("再见！")
                break

            # 清空历史命令
            elif user_input.lower() == 'clear':
                chat_client.clear_history()
                print("对话历史已清空")
                continue

            # 查看历史命令
            elif user_input.lower() == 'history':
                history = chat_client.get_history()
                if not history:
                    print("对话历史为空")
                else:
                    print("\n对话历史:")
                    for i, msg in enumerate(history, 1):
                        role = "用户" if msg["role"] == "user" else "助手"
                        print(f"{i}. [{role}]: {msg['content'][:100]}...")
                continue

            # 空输入处理
            elif not user_input:
                print("请输入内容")
                continue

            # 发送消息并获取回复
            print("\n思考中...", end="", flush=True)
            response = chat_client.chat(user_input)
            print("\r" + " " * 20 + "\r", end="")  # 清除"思考中..."提示
            print(f"助手: {response}")

        except KeyboardInterrupt:
            print("\n\n程序被中断")
            break
        except Exception as e:
            print(f"\n发生错误: {e}")


if __name__ == "__main__":
    main()