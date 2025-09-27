import random
import streamlit as st

# --- CONFIG ---
cards = [11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]
dealer_threshold = 17
blackjack = 21
suits = ["♥️", "♠️", "♦️", "♣️"]

def draw_card():
    """Pick a random card with a random suit."""
    value = random.choice(cards)
    suit = random.choice(suits)
    return f"{value}{suit}", value

# --- GAME TITLE ---
st.title("♠️ ♥️ Blackjack Game ♦️ ♣️")

# --- INIT SESSION STATE ---
for key, val in {
    "player_cards": [],
    "player_total": 0,
    "dealer_cards": [],
    "dealer_total": 0,
    "game_over": False,
    "message": "",
    "started": False,
}.items():
    if key not in st.session_state:
        st.session_state[key] = val

# --- START GAME ---
if not st.session_state.started:
    if st.button("▶️ Start Game"):
        # Deal cards
        c1, v1 = draw_card()
        c2, v2 = draw_card()
        st.session_state.player_cards = [c1, c2]
        st.session_state.player_total = v1 + v2

        d1, v3 = draw_card()
        d2, v4 = draw_card()
        st.session_state.dealer_cards = [d1, d2]
        st.session_state.dealer_total = v3 + v4

        st.session_state.started = True
        st.rerun()

# --- MAIN GAME ---
if st.session_state.started and not st.session_state.game_over:
    st.write(f"🎴 Your cards: {', '.join(st.session_state.player_cards)}, current score: {st.session_state.player_total}")
    st.write(f"🤖 Dealer's first card: {st.session_state.dealer_cards[0]}")

    move = st.radio("Do you want another card?", ("Hit", "Stand"), key="move")

    if move == "Hit" and st.button("Draw Card"):
        c, v = draw_card()
        st.session_state.player_cards.append(c)
        st.session_state.player_total += v

        if st.session_state.player_total > blackjack:
            st.session_state.message = f"💥 Player Busted! Final score: {st.session_state.player_total}"
            st.session_state.game_over = True
        st.rerun()

    elif move == "Stand" and st.button("Confirm Stand"):
        st.write("✋ Player stands. Now dealer plays...")
        st.write(f"🤖 Dealer's starting hand: {', '.join(st.session_state.dealer_cards)}, current score: {st.session_state.dealer_total}")

        while st.session_state.dealer_total < dealer_threshold:
            c, v = draw_card()
            st.session_state.dealer_cards.append(c)
            st.session_state.dealer_total += v

            if st.session_state.dealer_total > blackjack:
                st.session_state.message = f"💥 Dealer Busted! Dealer score: {st.session_state.dealer_total} — You win!"
                st.session_state.game_over = True
                break

        if not st.session_state.game_over:
            if st.session_state.player_total > st.session_state.dealer_total:
                st.session_state.message = f"🎉 Player wins! {st.session_state.player_total} vs {st.session_state.dealer_total}"
            elif st.session_state.player_total < st.session_state.dealer_total:
                st.session_state.message = f"🤖 Dealer wins! {st.session_state.player_total} vs {st.session_state.dealer_total}"
            else:
                st.session_state.message = f"🤝 It's a draw! {st.session_state.player_total} vs {st.session_state.dealer_total}"
            st.session_state.game_over = True
        st.rerun()

# --- DISPLAY RESULT ---
if st.session_state.message:
    st.success(st.session_state.message)

# --- RESET GAME ---
if st.session_state.game_over:
    if st.button("🔄 Play Again"):
        for key in ["player_cards", "player_total", "dealer_cards", "dealer_total", "game_over", "message", "started"]:
            st.session_state[key] = [] if "cards" in key else 0 if "total" in key else False if key in ["game_over", "started"] else ""
        st.rerun()
