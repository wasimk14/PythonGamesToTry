import random
import streamlit as st

cards = [11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]
dealer_threshold = 17
blackjack = 21

# --- SESSION STATE ---
if "player_total" not in st.session_state:
    st.session_state.player_total = []
if "dealer_total" not in st.session_state:
    st.session_state.dealer_total = []
if "game_over" not in st.session_state:
    st.session_state.game_over = False
if "message" not in st.session_state:
    st.session_state.message = ""

# --- START GAME ---
if not st.session_state.player_total and not st.session_state.dealer_total:
    st.session_state.player_total = [random.choice(cards), random.choice(cards)]
    st.session_state.dealer_total = [random.choice(cards), random.choice(cards)]

st.write(f"Your cards: {st.session_state.player_total}, current score: {sum(st.session_state.player_total)}")
st.write(f"Dealer's first card: {st.session_state.dealer_total[0]}")

# --- PLAYER MOVE ---
if not st.session_state.game_over:
    move = st.radio("Do you want another card?", ("Hit", "Stand"))

    if move == "Hit":
        st.session_state.player_total.append(random.choice(cards))
        st.write(f"Your cards: {st.session_state.player_total}, current score: {sum(st.session_state.player_total)}")

        if sum(st.session_state.player_total) > blackjack:
            st.session_state.message = "Player Busted! Score exceeded 21."
            st.session_state.game_over = True

    elif move == "Stand":
        st.write("Player stands. Now dealer plays...")
        st.write(f"Dealer's starting hand: {st.session_state.dealer_total}, current score: {sum(st.session_state.dealer_total)}")

        while sum(st.session_state.dealer_total) < dealer_threshold:
            st.session_state.dealer_total.append(random.choice(cards))
            st.write(f"Dealer hits: {st.session_state.dealer_total}, current score: {sum(st.session_state.dealer_total)}")

            if sum(st.session_state.dealer_total) > blackjack:
                st.session_state.message = "Dealer Busted! You win!"
                st.session_state.game_over = True
                break

        if not st.session_state.game_over:
            st.write(f"Final Player score: {sum(st.session_state.player_total)}")
            st.write(f"Final Dealer score: {sum(st.session_state.dealer_total)}")

            if sum(st.session_state.player_total) > sum(st.session_state.dealer_total):
                st.session_state.message = "Player wins!"
            elif sum(st.session_state.player_total) < sum(st.session_state.dealer_total):
                st.session_state.message = "Dealer wins!"
            else:
                st.session_state.message = "It's a draw!"
            st.session_state.game_over = True

# --- DISPLAY RESULT ---
if st.session_state.message:
    st.write(st.session_state.message)

# --- RESET GAME ---
if st.session_state.game_over:
    if st.button("Play Again"):
        st.session_state.player_total = []
        st.session_state.dealer_total = []
        st.session_state.game_over = False
        st.session_state.message = ""
