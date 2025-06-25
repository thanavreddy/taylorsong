# ✨ Enchanted Lyrics ✨

💜 **A Taylor Swift-themed lyrics visualizer** that fetches magical lyrics and transforms them into beautiful word clouds inspired by each of her eras.


## 🎤 What It Does

**Enchanted Lyrics** is a dreamy Streamlit app that:

- Lets you search any **Taylor Swift** song
- Fetches lyrics using the **Genius API**
- Displays them with an elegant UI
- Generates **word clouds** based on lyrics
- Allows you to switch between **Taylor Swift's eras**, each with its own visual theme

## 🌟 Features

- 🪄 Stunning UI with custom CSS & animations
- 🎨 Era-themed word cloud color palettes
- ☁️ Real-time lyrics fetching from Genius
- 💬 Elegant lyric display with filtering
- 💫 Era selector sidebar for Swiftie vibes

## 🔧 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/thanavreddy/taylorsong
cd enchanted-lyrics
```

### 2. Install Requirements

```bash
pip install -r requirements.txt
```

Make sure to have Python 3.7+

### 3. Get Genius API Access Token

1. Go to [genius.com/api-clients](https://genius.com/api-clients)
2. Sign in and create a new API client
3. Copy the Access Token

### 4. Add Token to Streamlit Secrets

Create a `.env` file and add your token:(or use the one provided)
```.env
GENIUS_ACCESS_TOKEN = "your_token_here"
```

### 5. Run the App

```bash
streamlit run main.py
```

## 📦 Requirements

- streamlit
- requests
- lyricsgenius
- wordcloud
- matplotlib
- Pillow
- beautifulsoup4 (optional)

You can install them manually:

```bash
pip install streamlit requests lyricsgenius wordcloud matplotlib Pillow beautifulsoup4
```

Or with the provided `requirements.txt`.

## 🌈 Suggested Songs

Try these magical hits to see the visualizer in action:

- 💛 Love Story
- 💜 Enchanted
- ❤️ All Too Well
- 🩵 Shake It Off
- 🖤 Look What You Made Me Do
- 💕 Lover
- 🤎 Cardigan
- 🍂 Willow
- 💙 Anti-Hero
- 🤍 Fortnight

## 🚀 Usage

1. Launch the app using `streamlit run enchanted_lyrics.py`
2. Select your favorite Taylor Swift era from the sidebar
3. Enter a song title in the search box
4. Watch as the lyrics appear with a beautiful word cloud visualization
5. Switch between eras to see different color themes and styles

## 🎨 Era Themes

Each era comes with its own unique visual styling and color palette to match the aesthetic of Taylor's different albums and phases.
