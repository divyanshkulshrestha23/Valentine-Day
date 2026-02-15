import os
import requests
from io import BytesIO
from flask import Flask, render_template
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from haishoku.haishoku import Haishoku

app = Flask(__name__)

# --- SPOTIFY CREDENTIALS ---
# Get these from https://developer.spotify.com/dashboard
CLIENT_ID = '5949e6b0e7284a13be79a0e1cccf2430'  # Set your Client ID
CLIENT_SECRET = '1f5aabbcfaee422f9820fa4655a22a28'  # Set your Client Secret

# Initialize Spotify client
try:
    auth_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
    sp = spotipy.Spotify(auth_manager=auth_manager)
except Exception as e:
    print(f"Spotify Auth Error: {e}")
    sp = None


def get_album_theme(track_id):
    """Fetches album art and extracts its dominant color."""
    if not sp or not CLIENT_ID:
        # Default soft pink if no API keys
        return "rgb(255, 209, 220)"

    try:
        track = sp.track(track_id)
        img_url = track['album']['images'][0]['url']
        #response = requests.get(img_url)
        #img_data = BytesIO(response.content)
        dominant = Haishoku.getDominant(img_url)
        return f"rgb({dominant[0]}, {dominant[1]}, {dominant[2]})"
    except Exception as e:
        return "rgb(255, 209, 220)"



# --- YOUR MEMORIES DATA ---
# track_id is the string after /track/ in a Spotify link
raw_memories = [
    {
        "image": "us1.jpg",
        "caption": "Discovering Each Other",
        "note": "If I ever knew we were destined to be, it was when I won your heart by dancing to this song in CS garden.",
        "track_id": "0bfvHnWWOeU1U5XeKyVLbW",  # Can't Take My Eyes Off You
    },
    {
        "image": "us2.jpg",
        "caption": "Day After Engi",
        "note": "Certainly the day when that feeling of finding home started washing over me. Of course I SHOULDN'T have shown up hungover, but your kind soul probably took the gamble of ignoring that flag and I'm ever so glad for that.",
        "track_id": "1R0a2iXumgCiFb7HEZ7gUE",  # Don't Blame Me
    },
    {
        "image": "us3.jpg",
        "caption": "Sinners",
        "note": "Entering that hall, there was no way either of us knew we were about to see one of the most exciting, passionate, fervent, whirlwind, timeless stories of not just 2025 but of all time. Oh, and the movie was good too ;)",
        "track_id": "7kvLAPEnEPlSbhZDlHFv0p",  # Fitoor
    },
    {
        "image": "us4.jpg",
        "caption": "SRC canteen in PJs",
        "note": "Kinda glad that you got to see me in my default outfit hehe. You think I've a potty/quizzing addiction but wait till you see the full extent of my pajama obsession. God only knows what would've happened had you not approved of this lol.",
        "track_id": "17QTsL4K9B9v4rI8CAIdfC",  # God Only Knows
    },
    {
        "image": "us5.jpg",
        "caption": "Rohini Entry",
        "note": "As many as East Delhi jokes as I may make, no one can't beat how ass Rohini is. So you coming all the way just to see me during my exams, I was in awe of the love and adoration you shower me with. Flowers, even a million of them, are only a fraction of all that I need to repay you.",
        "track_id": "3U4isOIWM3VvDubwSI3y7a",  # All of Me
    },
    {
        "image": "us6.jpg",
        "caption": "Last Day Before Holidays",
        "note": "I was so angry at time that day. It was running out so fast. I was also angry at it for not bringing me to you sooner. But all that happens, happens for a reason. And such is the mystery of love that it's better to just stay lost in it, holding each other's hands and seeing the beautiful roads it takes us on.",
        "track_id": "5GbVzc6Ex5LYlLJqzRQhuy",  # Mystery of Love
    },
    {
        "image": "us7.jpg",
        "caption": "First Day After Holidays",
        "note": "A rollercoaster two months could not bring our love down. When I came back and heard the 'I love you' from you again, I was in a heaven no man could ever reach. Also, we seem to have a great record with movies so we should watch something sooooooonnnnnnn.",
        "track_id": "2ZWlPOoWh0626oTaHrnl2a",  # Ivy
    },
    {
        "image": "us8.jpg",
        "caption": "In a gr8 place in my life rn (East Delhi)",
        "note": "I admit, I don't understand why we never had a proper Laxmi Nagar hangout before. Where else can we find the best family restaurants where we have to sit 4 feet apart to not draw the attention of tharki waiters, lol!",
        "track_id": "1NZs6n6hl8UuMaX0UC0YTz",  #Brooklyn Baby
    },
    {
        "image": "us9.jpg",
        "caption": "Arts-core Kids?",
        "note": "Never did I ever imagine going to art galleries with someone COULD BE SO FUN! Meeting you at an intellectual point in a convo about symbolism and then cracking immature jokes on an auntiyo ki painting? Nothing more peak than this. The sort of love that you've brought out from me has made me believe that there's nothing in this world that I won't find boring if we're in it together.",
        "track_id": "7nhWtCc3v6Vem80gYPlppQ",  #Cool Cat
    },
]


@app.route('/')
def index():
    processed_memories = []
    for item in raw_memories:
        theme_color = get_album_theme(item['track_id'])
        processed_memories.append({
            **item,
            "color": theme_color,
            "embed_url": f"https://open.spotify.com/embed/track/{item['track_id']}?utm_source=generator"
        })

    return render_template('index.html', memories=processed_memories)

if __name__ == '__main__':
    app.run(debug=True)