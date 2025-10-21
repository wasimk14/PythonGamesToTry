import streamlit as st
import time

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"

WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 10
Repeat = [WORK_MIN, SHORT_BREAK_MIN, LONG_BREAK_MIN]

# ---------------------------- SESSION STATE INIT ------------------------------- #
if "index" not in st.session_state:
    st.session_state.index = 0
if "remaining_time" not in st.session_state:
    st.session_state.remaining_time = Repeat[0] * 60
if "is_paused" not in st.session_state:
    st.session_state.is_paused = True
if "is_running" not in st.session_state:
    st.session_state.is_running = False
if "log" not in st.session_state:
    st.session_state.log = []

# ---------------------------- FUNCTIONS ------------------------------- #
def start_timer():
    st.session_state.is_running = True
    st.session_state.is_paused = False

def pause_timer():
    st.session_state.is_paused = True

def resume_timer():
    st.session_state.is_paused = False
    st.session_state.is_running = True

def reset_timer():
    st.session_state.is_running = False
    st.session_state.is_paused = True
    st.session_state.remaining_time = Repeat[st.session_state.index] * 60

def next_timer():
    st.session_state.index = (st.session_state.index + 1) % len(Repeat)
    st.session_state.remaining_time = Repeat[st.session_state.index] * 60
    st.session_state.log.append(f"Session complete → moved to stage {st.session_state.index + 1}")
    reset_timer()

def format_time(seconds):
    mins = seconds // 60
    secs = seconds % 60
    return f"{mins:02}:{secs:02}"

def get_stage_name(index):
    if index == 0:
        return ("Work", GREEN)
    elif index == 1:
        return ("Short Break", RED)
    else:
        return ("Long Break", PINK)

# ---------------------------- STREAMLIT UI ------------------------------- #
st.set_page_config(page_title="Pomodoro Timer", page_icon="🍅", layout="centered")
st.markdown(f"<h1 style='text-align: center; color:{GREEN};'>🍅 Pomodoro Timer</h1>", unsafe_allow_html=True)

stage_name, stage_color = get_stage_name(st.session_state.index)
st.markdown(f"<h2 style='text-align:center; color:{stage_color};'>{stage_name}</h2>", unsafe_allow_html=True)

# Timer display
timer_placeholder = st.empty()
timer_placeholder.markdown(f"<h1 style='text-align:center; color:white; background-color:#333; padding:15px; border-radius:10px;'>{format_time(st.session_state.remaining_time)}</h1>", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)
with col1:
    if st.button("▶️ Start", use_container_width=True):
        start_timer()
with col2:
    if st.button("⏸ Pause", use_container_width=True):
        pause_timer()
with col3:
    if st.button("🔁 Resume", use_container_width=True):
        resume_timer()
with col4:
    if st.button("🔄 Reset", use_container_width=True):
        reset_timer()

# ---------------------------- TIMER LOOP ------------------------------- #
if st.session_state.is_running and not st.session_state.is_paused:
    if st.session_state.remaining_time > 0:
        time.sleep(1)
        st.session_state.remaining_time -= 1
        st.experimental_rerun()
    else:
        next_timer()
        st.experimental_rerun()

# ---------------------------- LOG & STATUS ------------------------------- #
st.markdown("---")
st.subheader("🕒 Session Log")
for entry in reversed(st.session_state.log):
    st.write(f"• {entry}")

st.markdown("---")
st.caption("Tip: Use 'Pause' and 'Resume' to control your focus time.")
