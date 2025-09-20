import streamlit as st

logo = """           
 ,adPPYba, ,adPPYYba,  ,adPPYba, ,adPPYba, ,adPPYYba, 8b,dPPYba,  
a8"     "" ""     `Y8 a8P_____88 I8[    "" ""     `Y8 88P'   "Y8  
8b         ,adPPPPP88 8PP"""""""  `"Y8ba,  ,adPPPPP88 88          
"8a,   ,aa 88,    ,88 "8b,   ,aa aa    ]8I 88,    ,88 88          
 `"Ybbd8"' `"8bbdP"Y8  `"Ybbd8"' `"YbbdP"' `"8bbdP"Y8 88   
            88             88                                 
           ""             88                                 
                          88                                 
 ,adPPYba, 88 8b,dPPYba,  88,dPPYba,   ,adPPYba, 8b,dPPYba,  
a8"     "" 88 88P'    "8a 88P'    "8a a8P_____88 88P'   "Y8  
8b         88 88       d8 88       88 8PP""""""" 88          
"8a,   ,aa 88 88b,   ,a8" 88       88 "8b,   ,aa 88          
 `"Ybbd8"' 88 88`YbbdP"'  88       88  `"Ybbd8"' 88          
              88                                             
              88           
"""

# Display logo
st.text(logo)
st.title("🔐 Welcome to the Caesar Cipher Tool!")

# User inputs
encryption_input = st.radio("Choose an option:", ["encode", "decode"])
text = st.text_area("Type your message:")
shift = st.number_input("Type the shift number:", min_value=0, step=1)

# Caesar cipher logic
def caesar_cipher(text, shift, mode):
    word = ''
    for char in text:
        if mode == 'encode' and ('a' <= char <= 'z'):
            word += chr((ord(char) - ord('a') + shift) % 26 + ord('a'))
        elif mode == 'decode' and ('a' <= char <= 'z'):
            word += chr((ord(char) - ord('a') - shift) % 26 + ord('a'))
        else:
            word += char
    return word

# Button to run cipher
if st.button("🔁 Run Cipher"):
    result = caesar_cipher(text.lower(), shift, encryption_input)
    st.success(f"Result: {result}")

st.caption("👋 Goodbye! Thanks for using the Caesar Cipher Tool.")