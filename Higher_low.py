import random
import streamlit as st

# --- Data ---
data = [
    {'name': 'Instagram','follower_count': 346,'description': '📱 Social media platform','country': '🇺🇸 United States'},
    {'name': 'Cristiano Ronaldo','follower_count': 215,'description': '⚽ Footballer','country': '🇵🇹 Portugal'},
    {'name': 'Ariana Grande','follower_count': 183,'description': '🎤 Musician & Actress','country': '🇺🇸 United States'},
    {'name': 'Dwayne Johnson','follower_count': 181,'description': '🎬 Actor & Wrestler','country': '🇺🇸 United States'},
    # ... keep rest of your list unchanged ...
    {'name': 'NBA','follower_count': 47,'description': '🏀 Basketball League','country': '🇺🇸 United States'}
]

st.title("🔥 Higher-Lower Followers Game")

# --- Keep A and B fixed until reset ---
if "A" not in st.session_state or "B" not in st.session_state:
    st.session_state.A, st.session_state.B = random.sample(data, 2)

A = st.session_state.A
B = st.session_state.B

# --- Show comparison ---
st.subheader("Compare A")
st.write(f"**{A['name']}** — {A['description']} ({A['country']})")

st.markdown("### 🆚")

st.subheader("Compare B")
st.write(f"**{B['name']}** — {B['description']} ({B['country']})")

# --- Buttons for user choice ---
col1, col2 = st.columns(2)

with col1:
    if st.button("Choose A"):
        if A["follower_count"] > B["follower_count"]:
            st.success(f"✅ Correct! {A['name']} ({A['follower_count']}M) > {B['name']} ({B['follower_count']}M)")
        else:
            st.error(f"❌ Wrong! {A['name']} ({A['follower_count']}M) < {B['name']} ({B['follower_count']}M)")

with col2:
    if st.button("Choose B"):
        if B["follower_count"] > A["follower_count"]:
            st.success(f"✅ Correct! {B['name']} ({B['follower_count']}M) > {A['name']} ({A['follower_count']}M)")
        else:
            st.error(f"❌ Wrong! {B['name']} ({B['follower_count']}M) < {A['name']} ({A['follower_count']}M)")

# --- Play Again button ---
if st.button("🔄 Play Again"):
    st.session_state.A, st.session_state.B = random.sample(data, 2)
    st.rerun()
