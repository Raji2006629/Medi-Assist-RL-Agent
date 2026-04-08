 # inference.py
import os
from app import chatbot  # assuming your app.py is in root

# Mandatory for Hackathon OpenEnv
def reset():
    # Reset any states or variables your app uses
    return {"status": "reset done"}

def step(user_input, mode="Easy"):
    response, audio = chatbot(user_input, mode)
    return {"response": response, "audio": audio}

# Optional main for testing locally
if __name__ == "__main__":
    print(reset())
    print(step("I have fever", "Medium"))
