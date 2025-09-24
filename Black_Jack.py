import random
import streamlit as st

# --- CONFIG ---
cards = [11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]
dealer_threshold = 17
blackjack = 21

# Card suits for fun display
suits = ["♥️", "♠️", "♦️", "♣️"]

def draw_card():
    """Pick a random card with a random suit."""
    value = random.choice(cards)
    suit = random.choice(suits)
    return f"{value}{suit}", value  # return pretty + numeric

# --- GAME TITLE / LOGO ---
st.title("♠️♥️ Blackjack Game ♦️♣️")

st.markdown("""
| __ )| | __ _ | | _____| | ___ | | __
| _ | |/ ` |/ __| |/ / _ \ |/ _ \ / __| |/ /
| |) | | (| | (| < __/ | () | (| <
|/||_,_|_||____||_/ _|_|_\
""")


# --- SESSION STATE TO STORE GAME PROGRESS ---
if "player_cards" not in st.session_state:
    st.session_state.player_cards = []
    st.session_state.player_total = 0
if "dealer_cards" not in st.session_state:
    st.session_state.dealer_cards = []
    st.session_state.dealer_total = 0
if "game_over" not in st.session_state:
    st.session_state.game_over = False
if "message" not in st.session_state:
    st.session_state.message = ""

# --- DEAL INITIAL CARDS ---
if not st.session_state.player_cards and not st.session_state.dealer_cards:
    # player
    c1, v1 = draw_card()
    c2, v2 = draw_card()
    st.session_state.player_cards = [c1, c2]
    st.session_state.player_total = v1 + v2

    # dealer
    d1, v3 = draw_card()
    d2, v4 = draw_card()
    st.session_state.dealer_cards = [d1, d2]
    st.session_state.dealer_total = v3 + v4

    st.write(f"🎴 Your cards: {' , '.join(st.session_state.player_cards)}, current score: {st.session_state.player_total}")
    st.write(f"🤖 Dealer's first card: {st.session_state.dealer_cards[0]}")

# --- PLAYER MOVE ---
if not st.session_state.game_over:
    move = st.radio("Do you want another card?", ("Hit", "Stand"))

    if move == "Hit":
        c, v = draw_card()
        st.session_state.player_cards.append(c)
        st.session_state.player_total += v
        st.write(f"🎴 Your cards: {' , '.join(st.session_state.player_cards)}, current score: {st.session_state.player_total}")

        if st.session_state.player_total > blackjack:
            st.session_state.message = f"💥 Player Busted! Final score: {st.session_state.player_total}"
            st.session_state.game_over = True

    elif move == "Stand":
        st.write("✋ Player stands. Now dealer plays...")
        st.write(f"🤖 Dealer's starting hand: {' , '.join(st.session_state.dealer_cards)}, current score: {st.session_state.dealer_total}")

        # Dealer turn
        while st.session_state.dealer_total < dealer_threshold:
            c, v = draw_card()
            st.session_state.dealer_cards.append(c)
            st.session_state.dealer_total += v
            st.write(f"🤖 Dealer hits: {' , '.join(st.session_state.dealer_cards)}, current score: {st.session_state.dealer_total}")

            if st.session_state.dealer_total > blackjack:
                st.session_state.message = f"💥 Dealer Busted! Dealer score: {st.session_state.dealer_total} — You win!"
                st.session_state.game_over = True
                break

        if not st.session_state.game_over:
            st.write(f"🎴 Final Player score: {st.session_state.player_total}")
            st.write(f"🤖 Final Dealer score: {st.session_state.dealer_total}")

            if st.session_state.player_total > st.session_state.dealer_total:
                st.session_state.message = "🎉 Player wins!"
            elif st.session_state.player_total < st.session_state.dealer_total:
                st.session_state.message = "🤖 Dealer wins!"
            else:
                st.session_state.message = "🤝 It's a draw!"
            st.session_state.game_over = True

# --- DISPLAY RESULT ---
if st.session_state.message:
    st.success(st.session_state.message)

# --- RESET GAME ---
if st.session_state.game_over:
    if st.button("🔄 Play Again"):
        for key in ["player_cards", "player_total", "dealer_cards", "dealer_total", "game_over", "message"]:
            st.session_state[key] = [] if "cards" in key else 0 if "total" in key else False if key == "game_over" else ""
