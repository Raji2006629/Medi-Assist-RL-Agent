 # inference.py
import os
from fastapi import FastAPI
from pydantic import BaseModel
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
# FastAPI Setup
# ==============================
app = FastAPI(title="MediAssistRL OpenEnv API")

# ==============================
# Request Models
# ==============================
class StepRequest(BaseModel):
    user_input: str
    mode: str = "Medium"

class BookRequest(BaseModel):
    name: str
    age: int
    problem: str
    hospital: str

# ==============================
# Logging Helpers
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
# Reset Endpoint
# ==============================
@app.post("/reset")
def reset():
    global STATE
    STATE = {"tasks_completed": 0, "last_response": ""}
    log_start("Reset Environment")
    log_end("Environment Reset Done")
    return {"status": "ok"}

# ==============================
# Step Endpoint
# ==============================
@app.post("/step")
def step(req: StepRequest):
    global STATE
    log_start("Step Execution")

    # ==============================
    # AI Response Logic (replace with real AI)
    # ==============================
    t = req.user_input.lower()
    mode = req.mode

    if mode == "Easy":
        if "fever" in t:
            response = "You may have fever. Take rest and hydrate."
        elif "cough" in t:
            response = "Use honey and steam inhalation."
        else:
            response = "Take rest and monitor symptoms."
    elif mode == "Medium":
        if "fever" in t:
            response = "Fever detected. Monitor temperature and stay hydrated. Consider OTC meds."
        elif "cough" in t:
            response = "Cough detected. Steam inhalation and warm fluids recommended."
        else:
            response = "Serious advice: consult doctor if symptoms persist."
    elif mode == "Hard":
        response = f"Critical advice: Immediate medical attention may be required for '{t}'."

    STATE["tasks_completed"] += 1
    STATE["last_response"] = response

    log_step("Generated Response", reward=1.0)
    log_end(response)

    return {"response": response, "tasks_completed": STATE["tasks_completed"]}

# ==============================
# State Endpoint
# ==============================
@app.get("/state")
def state():
    return STATE

# ==============================
# Booking Endpoint (dummy)
# ==============================
@app.post("/book")
def book(req: BookRequest):
    return {"message": f"Appointment booked for {req.name} at {req.hospital}"}
