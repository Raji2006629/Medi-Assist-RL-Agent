import os
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from gtts import gTTS
import tempfile

# ================================
# Structured stdout logging
def start(msg):
    print(f"START: {msg}")

def step(msg):
    print(f"STEP: {msg}")

def end(msg):
    print(f"END: {msg}")

# ================================
# Environment variables
API_BASE_URL = os.environ.get("API_BASE_URL", "https://api.openai.com")
MODEL_NAME = os.environ.get("MODEL_NAME", "microsoft/DialoGPT-medium")
HF_TOKEN = os.environ.get("HF_TOKEN", None)

start("Initializing environment variables and RL model")

if not HF_TOKEN:
    raise ValueError("HF_TOKEN is not set in environment variables.")

step(f"Loading tokenizer and model: {MODEL_NAME}")
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)

# ================================
# Symptom database and modes
step("Setting up symptom knowledge and modes")
modes = ["easy", "medium", "hard"]
medical_knowledge = {
    "fever": "You may have a fever. Drink warm water, rest. Medicine: Paracetamol.",
    "throat": "It may be throat infection. Warm salt water gargle, honey. Consult doctor if severe.",
    "headache": "Headache detected. Rest, hydration, reduce screen time. Medicine: Paracetamol or ibuprofen.",
    "cough": "You may have cough. Honey, steam inhalation. Medicine: Cough syrup.",
    "chest pain": "⚠️ Serious symptom. Seek immediate medical help.",
}
hospitals = ["City Hospital", "Green Clinic", "Sunrise Medical Center"]

# ================================
# OpenEnv functions
state_data = {}

def reset():
    global state_data
    state_data = {}
    step("State reset")

def step_fn(symptom, mode="easy", book_hospital=False):
    global state_data
    step(f"Received symptom: {symptom}, mode: {mode}, book_hospital: {book_hospital}")
    
    response = medical_knowledge.get(symptom.lower(), "Symptom info not available.")
    
    if book_hospital:
        hospital = hospitals[0]
        response += f" You can book an appointment at {hospital}."
    
    if mode not in modes:
        mode = "easy"
    if mode == "medium":
        response += " Please take additional care and consult a doctor if symptoms persist."
    elif mode == "hard":
        response += " Immediate medical attention is advised. Contact emergency services if severe."
    
    state_data[symptom] = response
    return response

def voice_speak(text):
    tts = gTTS(text=text, lang="en")
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    tts.save(temp_file.name)
    os.system(f"start {temp_file.name}" if os.name=="nt" else f"mpg123 {temp_file.name}")
    return text

# ================================
# Sample inference run (3 tasks)
start("Running sample inference tasks")
reset()
tasks = [
    {"symptom": "fever", "mode": "easy", "book_hospital": True},
    {"symptom": "cough", "mode": "medium", "book_hospital": False},
    {"symptom": "chest pain", "mode": "hard", "book_hospital": True}
]

for t in tasks:
    res = step_fn(t["symptom"], t["mode"], t["book_hospital"])
    step(f"Task result: {res}")
    voice_speak(res)
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# ================================
# OpenEnv Models
# ================================
class Action(BaseModel):
    action: str

# ================================
# OpenEnv Endpoints
# ================================
@app.post("/reset")
def reset():
    return {"status": "OK", "message": "Environment reset successful"}

@app.post("/step")
def step(action: Action):
    print("[START] Step execution")
    print("[STEP] Received action:", action.action)
    # Example response
    result = {"reward": 1.0, "done": False, "info": "Step completed"}
    print("[END] Step execution")
    return result

@app.get("/state")
def state():
    return {"state": "Idle", "message": "Waiting for input"}

end("Sample inference tasks completed successfully")
 
