import uuid
from langchain.messages import HumanMessage

from agents import agent

# Configuration de la session
thread_id = str(uuid.uuid4())
config = {"configurable": {"thread_id": thread_id}}

print("Type 'q' or 'Q' to quit.")
user_input = input("User:")
while user_input != "q":
    if user_input.lower() == "q":
        print("Ending Test")
        break
    result = agent.invoke(
        input={
            "messages": [HumanMessage(content=user_input)]
        },
        config=config
    )
    
    print(result["messages"][-1].content)  # .text is only for gemini 3
    print(f"Current step: {result.get('current_step')}")
    print(f"Policy: {result.get('policy_type')}")
    user_input = input("User:")