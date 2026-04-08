import gradio as gr
from gtts import gTTS

# ================================
# MEDICAL RESPONSE WITH MODES
# ================================
def medical_response(text, mode):
    t = text.lower()

    if mode == "Easy":
        if "fever" in t:
            return "You may have fever. Take rest and drink water."
        elif "cough" in t:
            return "Use honey and steam inhalation."
        elif "headache" in t:
            return "Take rest and reduce screen time."

    elif mode == "Medium":
        if "fever" in t:
            return "Fever detected. Monitor temperature and stay hydrated."
        elif "cough" in t:
            return "Cough detected. Steam and warm fluids recommended."
        elif "headache" in t:
            return "Headache may be due to stress or dehydration."

    elif mode == "Hard":
        if "fever" in t:
            return "Fever may indicate infection. Consult doctor if persistent."
        elif "cough" in t:
            return "Respiratory irritation suspected. Monitor symptoms."
        elif "headache" in t:
            return "Possible migraine or tension headache."

    return "Consult a doctor for proper diagnosis."

# ================================
# VOICE
# ================================
def speak(text):
    tts = gTTS(text=text, lang='en')
    file_path = "output.mp3"
    tts.save(file_path)
    return file_path

# ================================
# BOOKING
# ================================
def book(name, age, problem, hospital):
    return f"Appointment booked for {name} at {hospital}."

# ================================
# CHAT
# ================================
def chatbot(user_input, mode):
    response = medical_response(user_input, mode)
    audio = speak(response)
    return response, audio

# ================================
# UI
# ================================
with gr.Blocks() as app:

    gr.Markdown("# MediAssist Healthcare AI")

    with gr.Tab("Chatbot"):
        mode = gr.Radio(["Easy", "Medium", "Hard"], value="Easy")
        inp = gr.Textbox(label="Enter symptoms")
        out_text = gr.Textbox()
        out_audio = gr.Audio()

        btn = gr.Button("Submit")
        btn.click(chatbot, inputs=[inp, mode], outputs=[out_text, out_audio])

    with gr.Tab("Booking"):
        name = gr.Textbox()
        age = gr.Number()
        problem = gr.Textbox()
        hospital = gr.Dropdown(["Apollo", "AIIMS", "Fortis"])

        out = gr.Textbox()
        btn2 = gr.Button("Book")
        btn2.click(book, inputs=[name, age, problem, hospital], outputs=out)

app.launch()
