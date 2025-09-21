import streamlit as st
import random

# 🎨 Logo / Banner
logo = r''' 
                         ___________
                         \         /
                          )_______(
                          |"""""""|_.-._,.---------.,_.-._
                          |       | | |               | | ''-.
                          |       |_| |_             _| |_..-'
                          |_______| '-' `'---------'` '-'
                          )"""""""(
                         /_________\\
                       .-------------.
                      /_______________\\
'''

st.markdown(f"<pre>{logo}</pre>", unsafe_allow_html=True)
st.title("🎉 Kids Auction Game 🏆")

# Auction Bids Dictionary (stored in session state so it persists)
if "bids" not in st.session_state:
    st.session_state.bids = {}

# --- Input Section ---
with st.form("auction_form"):
    name = st.text_input("👤 Enter your name:")
    bid = st.number_input("💰 Enter your bid:", min_value=0.0, step=10.0)
    competitors = st.radio("🤔 Are there any other bidders?", ["yes", "no"])
    submitted = st.form_submit_button("Place Bid")

if submitted and name and bid > 0:
    # Save bid
    st.session_state.bids[name] = bid

    # Random competitor bid
    competitor_bid = random.randint(0, 100000) * 100

    # Show results
    st.subheader("📢 Auction Result:")
    if competitors == "yes":
        st.write(f"👨‍👩‍👧 Your competitor’s bid is: **${competitor_bid:.2f}**")

        if competitor_bid > bid:
            st.error("❌ You lose the bid. Their bid is higher.")
        elif competitor_bid < bid:
            st.success("✅ You win! Your bid is higher.")
        else:
            st.info("🤝 It's a tie. Both bids are equal.")
    else:
        st.success("🎉 You win by default. No other bidders!")

# --- Summary Section ---
if st.session_state.bids:
    st.subheader("📜 Auction Summary")
    for bidder, bidding_amount in st.session_state.bids.items():
        st.write(f"👉 **{bidder}**: ${bidding_amount:.2f}")

    winner = max(st.session_state.bids, key=st.session_state.bids.get)

    st.success(f"🏆 The winner is **{winner}** with a bid of ${st.session_state.bids[winner]:.2f}")
