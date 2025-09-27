import random
import streamlit as st

# --- Data ---
data = [
    {'name': 'Instagram','follower_count': 346,'description': '📱 Social media platform','country': '🇺🇸 United States'},
    {'name': 'Cristiano Ronaldo','follower_count': 215,'description': '⚽ Footballer','country': '🇵🇹 Portugal'},
    {'name': 'Ariana Grande','follower_count': 183,'description': '🎤 Musician & Actress','country': '🇺🇸 United States'},
    {'name': 'Dwayne Johnson','follower_count': 181,'description': '🎬 Actor & Wrestler','country': '🇺🇸 United States'},
    {'name': 'Selena Gomez','follower_count': 174,'description': '🎶 Musician & Actress','country': '🇺🇸 United States'},
    {'name': 'Kylie Jenner','follower_count': 172,'description': '💄 TV Personality & Businesswoman','country': '🇺🇸 United States'},
    {'name': 'Kim Kardashian','follower_count': 167,'description': '💄 TV Personality & Businesswoman','country': '🇺🇸 United States'},
    {'name': 'Lionel Messi','follower_count': 149,'description': '⚽ Footballer','country': '🇦🇷 Argentina'},
    {'name': 'Beyoncé','follower_count': 145,'description': '🎤 Musician','country': '🇺🇸 United States'},
    {'name': 'Neymar','follower_count': 138,'description': '⚽ Footballer','country': '🇧🇷 Brazil'},
    {'name': 'National Geographic','follower_count': 135,'description': '📖 Magazine','country': '🇺🇸 United States'},
    {'name': 'Justin Bieber','follower_count': 133,'description': '🎤 Musician','country': '🇨🇦 Canada'},
    {'name': 'Taylor Swift','follower_count': 131,'description': '🎶 Musician','country': '🇺🇸 United States'},
    {'name': 'Kendall Jenner','follower_count': 127,'description': '💄 TV Personality & Model','country': '🇺🇸 United States'},
    {'name': 'Jennifer Lopez','follower_count': 119,'description': '🎤 Musician & Actress','country': '🇺🇸 United States'},
    {'name': 'Nicki Minaj','follower_count': 113,'description': '🎤 Musician','country': '🇹🇹 Trinidad & Tobago'},
    {'name': 'Nike','follower_count': 109,'description': '👟 Sportswear Brand','country': '🇺🇸 United States'},
    {'name': 'Khloé Kardashian','follower_count': 108,'description': '💄 TV Personality','country': '🇺🇸 United States'},
    {'name': 'Miley Cyrus','follower_count': 107,'description': '🎤 Musician & Actress','country': '🇺🇸 United States'},
    {'name': 'Katy Perry','follower_count': 94,'description': '🎶 Musician','country': '🇺🇸 United States'},
    {'name': 'Kourtney Kardashian','follower_count': 90,'description': '💄 TV Personality','country': '🇺🇸 United States'},
    {'name': 'Kevin Hart','follower_count': 89,'description': '🎭 Comedian & Actor','country': '🇺🇸 United States'},
    {'name': 'Ellen DeGeneres','follower_count': 87,'description': '🎭 Comedian','country': '🇺🇸 United States'},
    {'name': 'Real Madrid CF','follower_count': 86,'description': '⚽ Football Club','country': '🇪🇸 Spain'},
    {'name': 'FC Barcelona','follower_count': 85,'description': '⚽ Football Club','country': '🇪🇸 Spain'},
    {'name': 'Rihanna','follower_count': 81,'description': '🎶 Musician & Businesswoman','country': '🇧🇧 Barbados'},
    {'name': 'Demi Lovato','follower_count': 80,'description': '🎤 Musician & Actress','country': '🇺🇸 United States'},
    {'name': "Victoria's Secret",'follower_count': 69,'description': '👗 Fashion Brand','country': '🇺🇸 United States'},
    {'name': 'Zendaya','follower_count': 68,'description': '🎬 Actress & Musician','country': '🇺🇸 United States'},
    {'name': 'Shakira','follower_count': 66,'description': '🎶 Musician','country': '🇨🇴 Colombia'},
    {'name': 'Drake','follower_count': 65,'description': '🎤 Musician','country': '🇨🇦 Canada'},
    {'name': 'Chris Brown','follower_count': 64,'description': '🎤 Musician','country': '🇺🇸 United States'},
    {'name': 'LeBron James','follower_count': 63,'description': '🏀 Basketball Player','country': '🇺🇸 United States'},
    {'name': 'Vin Diesel','follower_count': 62,'description': '🎬 Actor','country': '🇺🇸 United States'},
    {'name': 'Cardi B','follower_count': 67,'description': '🎤 Musician','country': '🇺🇸 United States'},
    {'name': 'David Beckham','follower_count': 82,'description': '⚽ Footballer','country': '🇬🇧 United Kingdom'},
    {'name': 'Billie Eilish','follower_count': 61,'description': '🎶 Musician','country': '🇺🇸 United States'},
    {'name': 'Justin Timberlake','follower_count': 59,'description': '🎤 Musician & Actor','country': '🇺🇸 United States'},
    {'name': 'UEFA Champions League','follower_count': 58,'description': '⚽ Football Tournament','country': '🇪🇺 Europe'},
    {'name': 'NASA','follower_count': 56,'description': '🚀 Space Agency','country': '🇺🇸 United States'},
    {'name': 'Emma Watson','follower_count': 56,'description': '🎬 Actress','country': '🇬🇧 United Kingdom'},
    {'name': 'Shawn Mendes','follower_count': 57,'description': '🎶 Musician','country': '🇨🇦 Canada'},
    {'name': 'Virat Kohli','follower_count': 55,'description': '🏏 Cricketer','country': '🇮🇳 India'},
    {'name': 'Gigi Hadid','follower_count': 54,'description': '👗 Model','country': '🇺🇸 United States'},
    {'name': 'Priyanka Chopra Jonas','follower_count': 53,'description': '🎬 Actress & Musician','country': '🇮🇳 India'},
    {'name': '9GAG','follower_count': 52,'description': '😂 Meme Platform','country': '🇨🇳 China'},
    {'name': 'Ronaldinho','follower_count': 51,'description': '⚽ Footballer','country': '🇧🇷 Brazil'},
    {'name': 'Maluma','follower_count': 50,'description': '🎶 Musician','country': '🇨🇴 Colombia'},
    {'name': 'Camila Cabello','follower_count': 49,'description': '🎤 Musician','country': '🇨🇺 Cuba'},
    {'name': 'NBA','follower_count': 47,'description': '🏀 Basketball League','country': '🇺🇸 United States'}
]

# --- Title ---
st.title("🔥 Higher-Lower Followers Game")

# --- Pick two random entries ---
A, B = random.sample(data, 2)

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
            st.success(f"✅ Correct! {A['name']} has {A['follower_count']}M vs {B['name']} {B['follower_count']}M")
        else:
            st.error(f"❌ Wrong! {A['name']} has {A['follower_count']}M vs {B['name']} {B['follower_count']}M")

with col2:
    if st.button("Choose B"):
        if B["follower_count"] > A["follower_count"]:
            st.success(f"✅ Correct! {B['name']} has {B['follower_count']}M vs {A['name']} {A['follower_count']}M")
        else:
            st.error(f"❌ Wrong! {B['name']} has {B['follower_count']}M vs {A['name']} {A['follower_count']}M")
