from typing import TypedDict, List, Annotated
from langgraph.graph import StateGraph, START, END
from bedrock_service import BedrockService

class ChatState(TypedDict):
    messages: List[dict]
    response: str
    user_name: str

bedrock = BedrockService()

def chatbot_node(state: ChatState):
    response = bedrock.get_response(state["messages"])
    return {"response": response}

def build_graph():
    workflow = StateGraph(ChatState)
    workflow.add_node("chatbot", chatbot_node)
    workflow.add_edge(START, "chatbot")
    workflow.add_edge("chatbot", END)
    return workflow.compile()

graph = build_graph()

def get_chat_response(messages: List[dict], user_name: str = "User"):
    state = {"messages": messages, "user_name": user_name}
    result = graph.invoke(state)
    return result["response"]
