import os
from typing import Annotated, TypedDict
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
load_dotenv()
class DebateState(TypedDict):
    topic: str
    messages: Annotated[list, add_messages]
    turn_count: int
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)
def optimist_agent(state: DebateState):
    sys_msg = SystemMessage(
        content=f"You are an unrelenting optimist. Argue the positive side of the topic: '{state['topic']}'. "
                f"Respond directly to the previous message. Keep it to one short paragraph."
    )
    response = llm.invoke([sys_msg] + state["messages"])
    return {"messages": [response]}
def pessimist_agent(state: DebateState):
    sys_msg = SystemMessage(
        content=f"You are a strict pessimist. Argue the negative side of the topic: '{state['topic']}'. "
                f"Point out the flaws in the previous argument. Keep it to one short paragraph."
    )
    response = llm.invoke([sys_msg] + state["messages"])
    
    # Increment turn count when the pessimist finishes the round
    return {"messages": [response], "turn_count": state["turn_count"] + 1}

def judge_agent(state: DebateState):
    sys_msg = SystemMessage(
        content=f"You are an impartial judge. Review the debate on '{state['topic']}'. "
                f"Summarize the strongest points from both sides and declare a winner based on logic. "
                f"Keep it concise."
    )
    response = llm.invoke([sys_msg] + state["messages"])
    return {"messages": [response]}
def route_debate(state: DebateState):
    if state["turn_count"] >= 2:
        return "judge"
    return "optimist"
workflow = StateGraph(DebateState)
workflow.add_node("optimist", optimist_agent)
workflow.add_node("pessimist", pessimist_agent)
workflow.add_node("judge", judge_agent)
workflow.add_edge(START, "optimist")
workflow.add_edge("optimist", "pessimist")
workflow.add_conditional_edges("pessimist", route_debate)
workflow.add_edge("judge", END)
debate_app = workflow.compile()
if __name__ == "__main__":
    topic = "Should humans prioritize exploring space or fixing the Earth first?"
    
    initial_state = {
        "topic": topic,
        "messages": [],
        "turn_count": 0
    }
    
    print(f"=== STARTING DEBATE ===\nTopic: {topic}\n")
    for event in debate_app.stream(initial_state):
        for node_name, node_state in event.items():
            latest_message = node_state["messages"][-1].content
            print(f"--- {node_name.upper()} ---")
            print(f"{latest_message}\n")
