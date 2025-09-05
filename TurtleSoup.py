import os
from dotenv import load_dotenv
import asyncio

load_dotenv()
API_KEY=os.getenv("API_KEY")

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import Swarm
from autogen_agentchat.conditions import HandoffTermination, TextMentionTermination
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.messages import HandoffMessage

# 创建一个简单的模型客户端
model_client = OpenAIChatCompletionClient(
    model="deepseek-chat", 
    api_key=API_KEY,
    base_url="https://api.deepseek.com",
    model_info={
        "family": "unknown",
        "function_calling": True,
        "json_output": False,
        "multiple_system_messages": True,
        "structured_output": True,
        "vision": False,
    },
)