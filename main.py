import streamlit as st
import requests
import re
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from PIL import Image
import io
import base64

# Configure Streamlit page
st.set_page_config(
    page_title="✨ Enchanted Lyrics ✨",
    page_icon="💜",
    layout="wide"
)

# Custom CSS for Taylor Swift themed styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Dancing+Script:wght@400;600;700&family=Playfair+Display:wght@400;600;700&family=Poppins:wght@300;400;500;600&display=swap');
    .stTextInput input {
    color: #000 !important;
}
.stTextInput input::placeholder {
    color: #000 !important;
    opacity: 0.5 !important;
}
    /* Main background with dreamy gradient */
    .stApp {
        background: linear-gradient(135deg, 
            #FF00E2 0%, 
            #FF70FD 25%, 
            #C787FF 50%, 
            #B2B2FA 75%, 
            #ffeaa7 100%);
        background-attachment: fixed;
    }
    
    /* Sparkling header */
    .main-header {
        text-align: center;
        background: linear-gradient(45deg, #ff6b6b, #4ecdc4, #45b7d1, #96ceb4, #ffd93d);
        background-size: 400% 400%;
        animation: gradient 4s ease infinite;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-family: 'Dancing Script', cursive;
        font-size: 4rem;
        font-weight: 700;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .subtitle {
        text-align: center;
        font-family: 'Playfair Display', serif;
        font-size: 1.4rem;
        color: #8B5A83;
        font-style: italic;
        margin-bottom: 2rem;
    }
    
    /* Magical sparkles */
    .sparkle {
        position: relative;
        display: inline-block;
    }
    
    .sparkle::before,
    .sparkle::after {
        content: '✨';
        position: absolute;
        animation: sparkle 2s infinite;
    }
    
    .sparkle::before {
        left: -30px;
        animation-delay: 0s;
    }
    
    .sparkle::after {
        right: -30px;
        animation-delay: 1s;
    }
    
    @keyframes sparkle {
        0%, 100% { opacity: 0; transform: scale(0.5); }
        50% { opacity: 1; transform: scale(1); }
    }
    
    /* Dreamy lyrics container */
    .lyrics-container {
        background: linear-gradient(135deg, rgba(255,182,193,0.3), rgba(221,160,221,0.3));
        padding: 25px;
        border-radius: 20px;
        border: 2px solid #ffd1dc;
        margin: 20px 0;
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
    }
    
    /* Styled text areas */
    .stTextArea textarea {
        font-family: 'Poppins', sans-serif;
        font-size: 16px;
        line-height: 1.8;
        background: rgba(255,255,255,0.9) !important;
        border: 2px solid #ffd1dc !important;
        border-radius: 15px !important;
        color: #8B5A83 !important;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(45deg, #ff6b6b, #4ecdc4);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.5rem 2rem;
        font-family: 'Poppins', sans-serif;
        font-weight: 600;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.3);
    }
    
    /* Input styling */
    .stTextInput input {
        border: 2px solid #ffd1dc;
        border-radius: 15px;
        font-family: 'Poppins', sans-serif;
        font-size: 1.1rem;
        padding: 0.8rem;
        background: rgba(255,255,255,0.9);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #f8e8ff, #e6f3ff);
        border-radius: 20px;
        margin: 10px;
    }
    
    /* Card styling */
    .taylor-card {
        background: linear-gradient(135deg, rgba(255,255,255,0.9), rgba(248,232,255,0.9));
        padding: 20px;
        border-radius: 20px;
        border: 2px solid #ffd1dc;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        margin: 15px 0;
        backdrop-filter: blur(10px);
        color : black;
    }
    
    /* Metric styling */
    .metric-container {
        background: linear-gradient(45deg, rgba(255,182,193,0.3), rgba(221,160,221,0.3));
        padding: 15px;
        border-radius: 15px;
        text-align: center;
        border: 1px solid #ffd1dc;
        color:black;
    }
    
    /* Heart decorations */
    .heart-decoration {
        display: inline-block;
        animation: heartbeat 1.5s ease-in-out infinite;
        color: #ff69b4;
        font-size: 1.2rem;
        margin: 0 10px;
    }
    
    @keyframes heartbeat {
        0% { transform: scale(1); }
        50% { transform: scale(1.1); }
        100% { transform: scale(1); }
    }
    
    /* Success/Error message styling */
    .stSuccess {
        background: linear-gradient(45deg, rgba(152,251,152,0.8), rgba(144,238,144,0.8));
        border-radius: 15px;
        border: 2px solid #90EE90;
    }
    
    .stError {
        background: linear-gradient(45deg, rgba(255,182,193,0.8), rgba(255,160,160,0.8));
        border-radius: 15px;
        border: 2px solid #FFB6C1;
    }
    
    /* Custom headers */
    h1, h2, h3 {
        font-family: 'Playfair Display', serif;
        color: #8B5A83;
    }
    
    /* Floating elements */
    .floating {
        animation: floating 3s ease-in-out infinite;
    }
    
    @keyframes floating {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
        100% { transform: translateY(0px); }
    }
</style>
""", unsafe_allow_html=True)

def get_genius_access_token():
    """
    You'll need to get your access token from Genius API:
    1. Go to https://genius.com/api-clients
    2. Create a new API client
    3. Copy your access token
    """
    # Try to get from secrets first, fallback to empty string
    try:
        return st.secrets.get("GENIUS_ACCESS_TOKEN", "")
    except:
        # If no secrets file exists, you can temporarily hardcode it here for testing
        # IMPORTANT: Don't commit this to version control!
        return 'api key not found'

def search_song(song_title, artist="Taylor Swift"):
    """Search for a song on Genius API"""
    access_token = get_genius_access_token()
    
    if not access_token:
        st.error("Please add your Genius API access token to Streamlit secrets!")
        return None
    
    base_url = "https://api.genius.com"
    headers = {'Authorization': f'Bearer {access_token}'}
    
    search_url = f"{base_url}/search"
    params = {'q': f"{song_title} {artist}"}
    
    try:
        response = requests.get(search_url, headers=headers, params=params)
        response.raise_for_status()
        json_response = response.json()
        
        # Find the best match
        hits = json_response['response']['hits']
        for hit in hits:
            if artist.lower() in hit['result']['primary_artist']['name'].lower():
                return hit['result']
        
        return hits[0]['result'] if hits else None
    
    except requests.exceptions.RequestException as e:
        st.error(f"Error searching for song: {e}")
        return None

def get_song_lyrics(song_title, artist="Taylor Swift"):
    """
    Fetch lyrics using lyricsgenius library
    """
    access_token = get_genius_access_token()
    
    if not access_token:
        return "No API token available. Please add your Genius API access token."
    
    try:
        import lyricsgenius
        
        # Initialize the Genius API client
        genius = lyricsgenius.Genius(access_token)
        genius.verbose = False  # Turn off status messages
        genius.remove_section_headers = True  # Clean up the lyrics
        
        # Search for the song
        song = genius.search_song(song_title, artist)
        
        if song:
            return song.lyrics
        else:
            return f"Lyrics for '{song_title}' by {artist} not found."
            
    except ImportError:
        return """lyricsgenius library not installed. 
        
Please install it using: pip install lyricsgenius
        
Then restart your Streamlit app."""
        
    except Exception as e:
        return f"Error fetching lyrics: {str(e)}"

def clean_lyrics_for_wordcloud(lyrics):
    """Clean lyrics text for word cloud generation"""
    # Remove common words and clean text
    stop_words = {
        'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with',
        'by', 'from', 'up', 'about', 'into', 'through', 'during', 'before',
        'after', 'above', 'below', 'between', 'among', 'within', 'without',
        'a', 'an', 'is', 'was', 'are', 'were', 'been', 'be', 'have', 'has',
        'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should',
        'may', 'might', 'must', 'can', 'i', 'you', 'he', 'she', 'it', 'we',
        'they', 'me', 'him', 'her', 'us', 'them', 'my', 'your', 'his',
        'her', 'its', 'our', 'their', 'this', 'that', 'these', 'those'
    }
    
    # Clean and filter words
    words = re.findall(r'\b[a-zA-Z]+\b', lyrics.lower())
    filtered_words = [word for word in words if word not in stop_words and len(word) > 2]
    
    return ' '.join(filtered_words)

def generate_wordcloud(text, colormap='viridis'):
    """Generate a word cloud from text"""
    if not text.strip():
        return None
    
    wordcloud = WordCloud(
        width=800,
        height=400,
        background_color='white',
        colormap=colormap,
        max_words=100,
        relative_scaling=0.5,
        random_state=42
    ).generate(text)
    
    return wordcloud

def main():
    # Magical Header
    st.markdown("""
    <div class="sparkle">
        <h1 class='main-header'>✨ Enchanted Lyrics ✨</h1>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class='subtitle'>
        <span class="heart-decoration">💜</span>
        Where Taylor Swift's words come alive in magical word clouds
        <span class="heart-decoration">💜</span>
    </div>
    """, unsafe_allow_html=True)
    
    # Era selector for fun
    st.markdown("""
    <div style='text-align: center; margin-bottom: 2rem;'>
        <p style='font-family: "Poppins", sans-serif; font-size: 1.1rem; color: #8B5A83;'>
            🌟 Choose your era and discover the magic in Taylor's words 🌟
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar for settings
    with st.sidebar:
        st.markdown("""
        <div style='text-align: center; margin-bottom: 2rem;'>
            <h2 style='color: #8B5A83; font-family: "Dancing Script", cursive;'>
                ✨ Customize Your Magic ✨
            </h2>
        </div>
        """, unsafe_allow_html=True)
        
        # Era-themed color schemes
        st.markdown("### 🎨 Choose Your Era")
        era_colors = {
            "Fearless 💛": 'autumn',
            "Speak Now 💜": 'plasma',
            "Red ❤️": 'Reds',
            "1989 🩵": 'Blues',
            "Reputation 🖤": 'gray',
            "Lover 💕": 'spring',
            "Folklore 🤎": 'copper',
            "Evermore 🍂": 'viridis',
            "Midnights 💙": 'winter',
            "Tortured Poets 🤍": 'magma'
        }
        
        selected_era = st.selectbox(
            "Pick your favorite era:",
            list(era_colors.keys()),
            index=0
        )
        colormap = era_colors[selected_era]
        
        st.markdown("### 💫 How to Use")
        st.markdown("""
        <div class='taylor-card'>
            <p style='font-family: "Poppins", sans-serif; margin: 0;'>
                1. 🎵 Enter a Taylor Swift song title<br>
                2. ✨ Click 'Analyze Lyrics'<br>
                3. 💜 View the enchanted lyrics<br>
                4. ☁️ Explore the magical word cloud<br>
                5. 🌈 Switch eras for different vibes
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 🎭 Popular Songs to Try")
        st.markdown("""
        <div class='taylor-card'>
            <p style='font-family: "Poppins", sans-serif; font-size: 0.9rem; margin: 0;'>
                💛 Love Story • You Belong With Me<br>
                💜 Enchanted • Back to December<br>
                ❤️ All Too Well • I Knew You Were Trouble<br>
                🩵 Shake It Off • Blank Space<br>
                🖤 Look What You Made Me Do<br>
                💕 Lover • The Archer<br>
                🤎 Cardigan • Exile<br>
                🍂 Willow • Champagne Problems<br>
                💙 Anti-Hero • Lavender Haze<br>
                🤍 Fortnight • I Can Do It With A Broken Heart
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Main input with magical styling
    st.markdown("""
    <div class='taylor-card'>
        <h3 style='text-align: center; font-family: "Playfair Display", serif; color: #8B5A83; margin-bottom: 1rem;'>
            🎤 Enter Your Favorite Taylor Swift Song 🎤
        </h3>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([4, 1])
    
    with col1:
        song_title = st.text_input(
            "",
            placeholder="✨ Type a song title... (e.g., Love Story, Shake It Off, Anti-Hero) ✨",
            help="Enter any Taylor Swift song title to see the magic happen!",
            label_visibility="collapsed"
        )
    
    with col2:
        st.write("")  # Spacing
        st.write("")  # More spacing
        analyze_button = st.button("🔮 Analyze Lyrics", type="primary")
    
    if analyze_button and song_title:
        # Magical loading message
        with st.spinner("🌟 Summoning Taylor's lyrics from the enchanted archives... ✨"):
            # Search for the song
            song_data = search_song(song_title)
            
            if song_data:
                st.markdown(f"""
                <div class='taylor-card' style='text-align: center;'>
                    <h3 style='color: #8B5A83; font-family: "Playfair Display", serif; margin: 0;'>
                        ✨ Found: <span style='color: #ff6b6b;'>{song_data['title']}</span> ✨
                    </h3>
                    <p style='font-family: "Poppins", sans-serif; color: #8B5A83; margin: 5px 0 0 0;'>
                        by {song_data['primary_artist']['name']} 💜
                    </p>
                </div>
                """, unsafe_allow_html=True)
                
                # Get lyrics using the song title
                lyrics = get_song_lyrics(song_data['title'])
                
                # Create two columns for lyrics and word cloud
                col1, col2 = st.columns([1, 1])
                
                with col1:
                    st.markdown("""
                    <div class='floating'>
                        <h3 style='text-align: center; font-family: "Playfair Display", serif; color: #8B5A83;'>
                            📝 Enchanted Lyrics 📝
                        </h3>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown("<div class='lyrics-container'>", unsafe_allow_html=True)
                    st.text_area(
                        "",
                        value=lyrics,
                        height=400,
                        label_visibility="collapsed"
                    )
                    st.markdown("</div>", unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f"""
                    <div class='floating'>
                        <h3 style='text-align: center; font-family: "Playfair Display", serif; color: #8B5A83;'>
                            ☁️ {selected_era} Word Cloud ☁️
                        </h3>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Clean lyrics for word cloud
                    cleaned_text = clean_lyrics_for_wordcloud(lyrics)
                    
                    if cleaned_text:
                        wordcloud = generate_wordcloud(cleaned_text, colormap)
                        
                        if wordcloud:
                            st.markdown("<div class='taylor-card'>", unsafe_allow_html=True)
                            fig, ax = plt.subplots(figsize=(10, 5))
                            fig.patch.set_facecolor('none')
                            ax.imshow(wordcloud, interpolation='bilinear')
                            ax.axis('off')
                            st.pyplot(fig)
                            plt.close()
                            st.markdown("</div>", unsafe_allow_html=True)
                        else:
                            st.warning("✨ The magic couldn't create a word cloud from these lyrics. ✨")
                    else:
                        st.warning("✨ Not enough magical words to create a meaningful cloud. ✨")
                
                # Song info with magical styling
                with st.expander("🎵 Song Information & Magic Details"):
                    st.markdown("""
                    <div class='taylor-card'>
                        <h4 style='text-align: center; color: #8B5A83; font-family: "Playfair Display", serif;'>
                            ✨ Song Magic Details ✨
                        </h4>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.markdown(f"""
                        <div class='metric-container'>
                            <h5 style='color: #8B5A83; margin: 0;'>🎤 Artist</h5>
                            <p style='font-size: 1.2rem; margin: 5px 0 0 0; color: #ff6b6b;'>{song_data['primary_artist']['name']}</p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col2:
                        st.markdown(f"""
                        <div class='metric-container'>
                            <h5 style='color: #8B5A83; margin: 0;'>🔮 Song ID</h5>
                            <p style='font-size: 1.2rem; margin: 5px 0 0 0; color: #ff6b6b;'>{song_data['id']}</p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col3:
                        if song_data.get('release_date_for_display'):
                            st.markdown(f"""
                            <div class='metric-container'>
                                <h5 style='color: #8B5A83; margin: 0;'>📅 Release Date</h5>
                                <p style='font-size: 1.2rem; margin: 5px 0 0 0; color: #ff6b6b;'>{song_data['release_date_for_display']}</p>
                            </div>
                            """, unsafe_allow_html=True)
            
            else:
                st.markdown("""
                <div class='taylor-card' style='text-align: center; background: linear-gradient(45deg, rgba(255,182,193,0.8), rgba(255,160,160,0.8));'>
                    <h4 style='color: #8B5A83; margin: 0;'>
                        ✨ Song not found in the enchanted archives ✨
                    </h4>
                    <p style='color: #8B5A83; margin: 10px 0 0 0;'>
                        Please check the spelling and try again, Swiftie! 💜
                    </p>
                </div>
                """, unsafe_allow_html=True)
    
    elif analyze_button and not song_title:
        st.markdown("""
        <div class='taylor-card' style='text-align: center; background: linear-gradient(45deg, rgba(255,223,186,0.8), rgba(255,206,84,0.8));'>
            <h4 style='color: #8B5A83; margin: 0;'>
                ✨ Please enter a song title first, Swiftie! ✨
            </h4>
        </div>
        """, unsafe_allow_html=True)
    
    # Instructions for setup with magical styling
    if not get_genius_access_token():
        st.markdown("""
        <div class='taylor-card' style='margin-top: 3rem;'>
            <h3 style='text-align: center; color: #8B5A83; font-family: "Dancing Script", cursive;'>
                🔑 Setup Your Enchanted Connection 🔑
            </h3>
            <p style='font-family: "Poppins", sans-serif; color: #8B5A83;'>
                To unlock the full magic of this app, you need to connect to the Genius API:
            </p>
            <ol style='font-family: "Poppins", sans-serif; color: #8B5A83;'>
                <li>✨ Get a free Genius API access token from <a href="https://genius.com/api-clients" target="_blank">genius.com/api-clients</a></li>
                <li>🔮 Add it to your Streamlit secrets as <code>GENIUS_ACCESS_TOKEN</code></li>
                <li>💜 Install additional dependencies: <code>pip install lyricsgenius beautifulsoup4</code></li>
            </ol>
            <p style='font-family: "Poppins", sans-serif; color: #8B5A83; text-align: center; font-style: italic;'>
                The current version shows the magical structure with demo data. ✨
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Footer with Taylor Swift vibes
    st.markdown("""
    <div style='text-align: center; margin-top: 4rem; padding: 2rem;'>
        <p style='font-family: "Dancing Script", cursive; font-size: 1.5rem; color: #8B5A83;'>
            ✨ Made with 💜 for all the Swifties out there ✨
        </p>
        <p style='font-family: "Poppins", sans-serif; color: #8B5A83; font-size: 0.9rem;'>
            "And you call me up again just to break me like a promise" 🎵
        </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
