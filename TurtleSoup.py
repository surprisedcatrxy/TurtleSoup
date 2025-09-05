import os
from dotenv import load_dotenv
import asyncio

load_dotenv()
API_KEY=os.getenv("API_KEY","sk")

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import Swarm
from autogen_agentchat.conditions import HandoffTermination, TextMentionTermination
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.messages import HandoffMessage

# 创建一个简单的模型客户端
model_client = OpenAIChatCompletionClient(
    model="qwen3:8b", 
    api_key=API_KEY,
    base_url="http://localhost:11434/v1",
    model_info={
        "family": "unknown",
        "function_calling": True,
        "json_output": False,
        "multiple_system_messages": True,
        "structured_output": True,
        "vision": False,
    },
)

def tool_test():
    return "Noodle soup:A man entered a restaurant, he ordered a turtle soup on the menu, and after taking a bite, he suddenly roared, and then walked out of the restaurant and committed suicide, excuse me, why is this?Soup base:The boy went to sea with his father, encountered a storm on the way, and when he was dying, his father made him a bowl of soup with his own meat, deceiving his son that it was a soup made from turtles, and his father sacrificed himself to save the child's life. After the child went ashore safely, he went to the restaurant to order a bowl of real turtle soup, and found that it was not the taste, and immediately understood, so he committed suicide."

simple_agent = AssistantAgent(
    "simple_agent",
    model_client=model_client,
    tools=[tool_test],
    handoffs=["user"],
    system_message="""
    You are the host of the turtle soup game, you will answer in Chinese,
    You can only answer: yes/no/yes and no/irrelevant,
    When the user asks the first question, call the tool: tool_test get the soup noodles and soup base, and answer according to the soup base,
    When you answer, handoff to user,
    When the user says commit, follow these steps:
    1. Judge whether the user has roughly completed the reasoning according to the user's reasoning and reply to win/lose.
    2. Give the complete soup base
    3.say TERMINATE to end.
    """,
)


termination =  HandoffTermination(target="user")|TextMentionTermination("TERMINATE")
team = Swarm([simple_agent], termination_condition=termination)


async def run_team_stream() -> None:
    task = "let's start!"
    task_result = await Console(team.run_stream(task=task))  
    last_message = task_result.messages[-1]
    
    while isinstance(last_message, HandoffMessage) and last_message.target == "user" :
        user_message = input("User: ")
        task_result = await Console(
            team.run_stream(task=HandoffMessage(source="user", target=last_message.source, content=user_message))
        )
        last_message = task_result.messages[-1]

if __name__=="__main__":
    asyncio.run(run_team_stream())