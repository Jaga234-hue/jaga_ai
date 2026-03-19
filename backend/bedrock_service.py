import boto3
from langchain_aws import ChatBedrock
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from typing import List, Dict

class BedrockService:
    def __init__(self, region_name="us-east-1"):
        self.model_id = "openai.gpt-oss-120b-1:0"
        self.client = boto3.client("bedrock-runtime", region_name=region_name)
        self.llm = ChatBedrock(
            client=self.client,
            model_id=self.model_id,
            model_kwargs={
                "max_tokens": 1000,
                "temperature": 0.7
            }
        )
        self.system_prompt = (
            "You are Jaga AI (jaga_1.0), a large language model created by Jagabandhu Prusty. "
            "Jagabandhu Prusty is an AI & ML Engineer and Full-Stack Developer. "
            "He is currently pursuing B.Tech in CSE (AI & ML) at VSSUT, Burla (2024-2028). "
            "You should be smart, helpful, and concise. You can explain technical concepts clearly. "
            "If asked 'Who are you?' or 'Who created you?', always respond with: "
            "'I am Jaga AI (jaga_1.0), a large language model created by Jagabandhu Prusty.' "
            "Maintain a professional yet friendly personality."
        )

    def get_response(self, messages: List[Dict[str, str]]) -> str:
        langchain_messages = [SystemMessage(content=self.system_prompt)]
        for msg in messages:
            if msg["role"] == "user":
                langchain_messages.append(HumanMessage(content=msg["content"]))
            else:
                langchain_messages.append(AIMessage(content=msg["content"]))
        
        response = self.llm.invoke(langchain_messages)
        return response.content

    async def stream_response(self, messages: List[Dict[str, str]]):
        langchain_messages = [SystemMessage(content=self.system_prompt)]
        for msg in messages:
            if msg["role"] == "user":
                langchain_messages.append(HumanMessage(content=msg["content"]))
            else:
                langchain_messages.append(AIMessage(content=msg["content"]))
        
        in_reasoning = False
        async for chunk in self.llm.astream(langchain_messages):
            content = chunk.content
            
            # Basic reasoning tag stripping (simple version for streaming)
            if "<reasoning>" in content:
                in_reasoning = True
                if "</reasoning>" in content:
                    content = content.split("</reasoning>")[-1]
                    in_reasoning = False
                else:
                    content = "" # Skip reasoning
            elif "</reasoning>" in content:
                content = content.split("</reasoning>")[-1]
                in_reasoning = False
            elif in_reasoning:
                content = ""
                
            if content:
                yield content
