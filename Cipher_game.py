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

print(logo)

print("🔐 Welcome to the Caesar Cipher Tool!")

while True:
    encryption_input = input("Type 'encode' to encrypt, type 'decode' to decrypt:\n").lower()
    text = input("Type your message:\n").lower()
    shift = int(input("Type the shift number:\n"))

    word = ''
    for char in text:
        if (encryption_input == 'encode') and ('a' <= char <= 'z'):
            word += chr((ord(char) - ord('a') + shift) % 26 + ord('a'))
        elif (encryption_input == 'decode') and ('a' <= char <= 'z'):
            word += chr((ord(char) - ord('a') - shift) % 26 + ord('a'))
        else:
            word += char

    print("🔁 Result:", word)

    new_input = input("Type 'yes' to go again. Otherwise type 'no':\n").lower()
    if new_input != 'yes':
        break

print("👋 Goodbye! Thanks for using the Caesar Cipher Tool.")