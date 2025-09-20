import streamlit as st
import random

# -----------------------------
# Data
# -----------------------------
letters = list('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')
numbers = list('0123456789')
symbols = list('!#$%&()*+')

# -----------------------------
# UI
# -----------------------------
st.title("🔐 PyPassword Generator")

nr_letters = st.number_input("How many letters would you like?", min_value=0, max_value=50, value=4)
nr_symbols = st.number_input("How many symbols would you like?", min_value=0, max_value=20, value=2)
nr_numbers = st.number_input("How many numbers would you like?", min_value=0, max_value=20, value=2)

# -----------------------------
# Generate password
# -----------------------------
if st.button("Generate Password"):
    word = "".join(random.choice(letters) for _ in range(nr_letters))
    symb = "".join(random.choice(symbols) for _ in range(nr_symbols))
    num = "".join(random.choice(numbers) for _ in range(nr_numbers))

    chosen = list(word + symb + num)
    random.shuffle(chosen)
    password = "".join(chosen)

    st.success(f"✅ Your generated password: **{password}**")
