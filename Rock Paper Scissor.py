import streamlit as st
import random

# ASCII art
rock = '''
    _______
---'   ____)
      (_____)
      (_____)
      (____)
---.__(___)
'''

paper = '''
    _______
---'   ____)____
          ______)
          _______)
         _______)
---.__________)
'''

scissors = '''
    _______
---'   ____)____
          ______)
       __________)
      (____)
---.__(___)
'''

choices = [rock, paper, scissors]
choice_names = ["Rock", "Paper", "Scissors"]

st.title("✊✋✌ Rock, Paper, Scissors")
st.write("First to reach 5 points wins!")

# Initialize scores in session state
if "user_score" not in st.session_state:
    st.session_state.user_score = 0
if "computer_score" not in st.session_state:
    st.session_state.computer_score = 0
if "game_over" not in st.session_state:
    st.session_state.game_over = False

# User selection
user_input = st.radio("What do you choose?", [0, 1, 2], format_func=lambda x: choice_names[x])

if st.button("Play Round") and not st.session_state.game_over:
    computer_choice = random.randint(0, 2)

    st.subheader("You chose:")
    st.text(choices[user_input])
    st.subheader("Computer chose:")
    st.text(choices[computer_choice])

    # Determine winner
    if user_input == computer_choice:
        st.info("It's a tie!")
    elif (user_input == 0 and computer_choice == 2) or \
         (user_input == 1 and computer_choice == 0) or \
         (user_input == 2 and computer_choice == 1):
        st.success("You win this round!")
        st.session_state.user_score += 1
    else:
        st.error("Computer wins this round!")
        st.session_state.computer_score += 1

    # Show current scores
    st.write(f"### Score → You: {st.session_state.user_score} | Computer: {st.session_state.computer_score}")

    # Check if game over
    if st.session_state.user_score == 5:
        st.balloons()
        st.success("🎉 You reached 5 points first. You win the game!")
        st.session_state.game_over = True
    elif st.session_state.computer_score == 5:
        st.error("💻 Computer reached 5 points first. You lose the game!")
        st.session_state.game_over = True

# Restart button
if st.session_state.game_over:
    if st.button("Restart Game"):
        st.session_state.user_score = 0
        st.session_state.computer_score = 0
        st.session_state.game_over = False
