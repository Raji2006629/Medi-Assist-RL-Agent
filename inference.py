 import os
import sys
import json
from datetime import datetime

# ==============================
# Environment Variables
# ==============================
API_BASE_URL = os.environ.get("API_BASE_URL", "")
MODEL_NAME = os.environ.get("MODEL_NAME", "")
HF_TOKEN = os.environ.get("HF_TOKEN", "")

# ==============================
# OpenEnv State
# ==============================
STATE = {
    "tasks_completed": 0,
    "last_response": ""
}

# ==============================
# Helper Functions
# ==============================
def log_start(task_name):
    print(f"[START] Task: {task_name} | Timestamp: {datetime.now().isoformat()}")

def log_step(step_name, reward=None):
    if reward is not None:
        print(f"[STEP] Step: {step_name} | Reward: {reward}")
    else:
        print(f"[STEP] Step: {step_name}")

def log_end(result):
    print(f"[END] Result: {result}")

# ==============================
# Reset Function (mandatory)
# ==============================
def reset():
    global STATE
    STATE = {"tasks_completed": 0, "last_response": ""}
    log_start("Reset Environment")
    log_end("Environment Reset Done")
    return {"status": "ok"}

# ==============================
# Step Function (mandatory)
# ==============================
def step(user_input, mode="Medium"):
    global STATE

    log_start("Step Execution")

    # Example: simple AI response logic
    response = ""
    if mode == "Easy":
        response = f"Easy advice for: {user_input}"
    elif mode == "Medium":
        response = f"Medium advice for: {user_input}. Please follow instructions seriously."
    elif mode == "Hard":
        response = f"Hard advice for: {user_input}. Immediate medical attention may be required."

    # Increment tasks completed
    STATE["tasks_completed"] += 1
    STATE["last_response"] = response

    # Structured logging
    log_step("Generated Response", reward=1.0)  # dummy reward
    log_end(response)

    return {"response": response, "tasks_completed": STATE["tasks_completed"]}

# ==============================
# State Function (mandatory)
# ==============================
def state():
    return STATE

# ==============================
# Main Execution (for CLI testing)
# ==============================
if __name__ == "__main__":
    reset()
    while True:
        inp = input("Enter symptom/task (or 'exit'): ")
        if inp.lower() == "exit":
            break
        out = step(inp, mode="Medium")
        print(out)
