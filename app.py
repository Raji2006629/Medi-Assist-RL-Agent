 import gradio as gr
from gtts import gTTS
import tempfile
import sys

# ================================
# Structured logging helper
# ================================
def log_step(step_name, details=""):
    print(f"[STEP] {step_name} - {details}", flush=True)

def log_start(task_name):
    print(f"[START] {task_name}", flush=True)

def log_end(task_name):
    print(f"[END] {task_name}", flush=True)

# ================================
# MEDICAL RESPONSE
# ================================
def medical_response(text, mode):
    log_step("Medical response", f"Mode: {mode}, Input: {text}")
    t = text.lower()

    if mode.lower() == "easy":
        if "fever" in t:
            return "You may have fever. Take rest and drink water."
        elif "cough" in t:
            return "Use honey and steam inhalation."
        elif "headache" in t:
            return "Take rest and reduce screen time."

    elif mode.lower() == "medium":
        if "fever" in t:
            return "Fever detected. Monitor temperature and stay hydrated. OTC medicines like paracetamol can help."
        elif "cough" in t:
            return "Cough detected. Steam, warm fluids, and cough syrup may help."
        elif "headache" in t:
            return "Headache may be due to stress or dehydration. Take mild analgesics if necessary."

    elif mode.lower() == "hard":
        if "fever" in t:
            return "Fever may indicate infection. Consult a doctor if persistent. Consider full checkup and prescribed antibiotics if advised."
        elif "cough" in t:
            return "Respiratory irritation suspected. Monitor symptoms. Visit doctor for proper diagnosis."
        elif "headache" in t:
            return "Possible migraine or tension headache. Consult a neurologist if frequent or severe."

    return "Consult a doctor for proper diagnosis."

# ================================
# VOICE
# ================================
def speak(text):
    log_step("Voice generation", text)
    tts = gTTS(text=text, lang='en')
    tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    tts.save(tmp_file.name)
    return tmp_file.name

# ================================
# BOOKING
# ================================
def book(name, age, problem, hospital):
    log_step("Booking", f"{name}, {age}, {problem}, {hospital}")
    return f"Appointment booked for {name} at {hospital}."

# ================================
# CHAT FUNCTION
# ================================
def chatbot(user_input, mode):
    log_start("Chatbot Query")
    response = medical_response(user_input, mode)
    audio_file = speak(response)
    log_end("Chatbot Query")
    return response, audio_file

# ================================
# GRADIO INTERFACE
# ================================
with gr.Blocks() as app:
    gr.Markdown("## MediAssist Healthcare AI")

    with gr.Tab("Chatbot"):
        mode = gr.Radio(["Easy", "Medium", "Hard"], value="Easy", label="Select Mode")
        inp = gr.Textbox(label="Enter your symptoms")
        out_text = gr.Textbox(label="AI Response")
        out_audio = gr.Audio(label="Voice Guidance", type="filepath")
        btn = gr.Button("Submit")
        btn.click(chatbot, inputs=[inp, mode], outputs=[out_text, out_audio])

    with gr.Tab("Booking"):
        name = gr.Textbox(label="Your Name")
        age = gr.Number(label="Age")
        problem = gr.Textbox(label="Problem Description")
        hospital = gr.Dropdown(["Apollo", "AIIMS", "Fortis"], label="Select Hospital")
        out = gr.Textbox(label="Booking Status")
        btn2 = gr.Button("Book Appointment")
        btn2.click(book, inputs=[name, age, problem, hospital], outputs=out)

if __name__ == "__main__":
    log_start("App Launch")
    app.launch()
    log_end("App Launch")
