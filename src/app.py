import streamlit as st
from chatbot import get_technical_questions
from utils import check_exit, display_message
from prompts import questions, field_keys, exit_keywords

# --------------------------- CONFIG ---------------------------
st.set_page_config(page_title="Hiring Assistant Chatbot")
st.title("🤖 TalentScout Hiring Assistant")
st.markdown("Welcome! I'll help screen candidates based on their info and tech stack.")
st.markdown("---")

# --------------------------- SESSION INIT ---------------------------
for key, default in {
    'messages': [],
    'step': -1,
    'user_inputs': {},
    'tech_questions': [],
    'tech_answers': [],
    'tech_index': 0,
    'tech_stage': False,
    'conversation_started': False,
    'waiting_for_greeting': True,
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

# --------------------------- VALIDATION FUNCTION ---------------------------
def validate_response(prompt_key, user_input):
    if prompt_key == "email":
        return "@" in user_input and "." in user_input
    elif prompt_key == "phone":
        return user_input.replace(" ", "").isdigit() and len(user_input) >= 7
    elif prompt_key == "years_of_experience":
        return user_input.isdigit() and 0 <= int(user_input) <= 50
    elif prompt_key == "tech_stack":
        return len(user_input.strip()) > 0 and any(char.isalpha() for char in user_input)
    elif prompt_key == "full_name":
        return len(user_input.split()) >= 2
    elif prompt_key in ["desired_position", "location"]:
        return len(user_input.strip()) > 1
    return True

# --------------------------- DISPLAY CHAT HISTORY ---------------------------
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --------------------------- FIRST BOT MESSAGE ---------------------------
if st.session_state.step == -1 and not st.session_state.conversation_started:
    display_message("assistant", "Hey there! 👋 I’m your hiring assistant.\n\nSay hi to begin!")
    st.session_state.step = 0
    # st.stop()  ❌ REMOVE THIS LINE COMPLETELY


# --------------------------- USER INPUT FIELD ---------------------------
user_input = st.chat_input("Say hi to begin...")

if user_input:
    if user_input.strip() == "":
        display_message("assistant", "Hmm, I didn’t catch that. Could you rephrase?")
        st.stop()

    if check_exit(user_input):
        display_message("assistant", "Thanks for chatting! 👋 We'll be in touch soon.")
        st.stop()

    display_message("user", user_input)

    # ---------------------- WAITING FOR GREETING ----------------------
    if st.session_state.waiting_for_greeting:
        greetings = ["hi", "hello", "hey", "yo", "sup", "good morning", "good evening", "good afternoon"]
        if any(greet in user_input.lower() for greet in greetings):
            display_message("assistant",
                "Nice to meet you! 😊\n\nI'll ask you a few basic questions — like your name, contact info, job role you're applying for, and your experience.\n\n"
                "👉 Please respond clearly and correctly so we can proceed smoothly.\n\nThen, I'll ask a few technical questions based on your skills. Ready? Let's start!"
            )
            st.session_state.conversation_started = True
            st.session_state.waiting_for_greeting = False
            st.session_state.step = 0
            display_message("assistant", questions[0])
        else:
            display_message("assistant", "Please say hi or hello to begin! 👋")
        st.stop()

    # ---------------------- PERSONAL QUESTIONS ----------------------
    if not st.session_state.tech_stage:
        step = st.session_state.step
        if step < len(field_keys):
            key = field_keys[step]
            if validate_response(key, user_input):
                st.session_state.user_inputs[key] = user_input
                st.session_state.step += 1
            else:
                display_message("assistant", f"Hmm, that doesn't seem like a valid {key.replace('_', ' ')}. Could you try again?")
                st.stop()

        if st.session_state.step < len(questions):
            display_message("assistant", questions[st.session_state.step])
        else:
            st.session_state.tech_stage = True
            tech_stack = st.session_state.user_inputs.get("tech_stack", "")
            display_message("assistant", "Awesome, thanks! Now let me ask you a few technical questions based on your tech stack...")
            st.session_state.tech_questions = get_technical_questions(tech_stack)

            if st.session_state.tech_questions:
                display_message("assistant", st.session_state.tech_questions[0])

    # ---------------------- TECHNICAL QUESTIONS ----------------------
    else:
        st.session_state.tech_answers.append(user_input)
        st.session_state.tech_index += 1
        idx = st.session_state.tech_index

        if idx < len(st.session_state.tech_questions):
            display_message("assistant", st.session_state.tech_questions[idx])
        else:
            display_message("assistant", "✅ Thanks for your answers! We'll review everything and reach out soon. All the best! 🍀")
            print("CANDIDATE INFO:", st.session_state.user_inputs)
            for q, a in zip(st.session_state.tech_questions, st.session_state.tech_answers):
                print(f"Q: {q}\nA: {a}\n")

st.markdown("---")
st.caption("Powered by LLaMA | TalentScout AI Assistant")




