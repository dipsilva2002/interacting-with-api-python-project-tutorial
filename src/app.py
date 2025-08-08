import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

load_dotenv()
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(auth_manager=auth_manager)

artist_name = "Morat"
results = sp.search(q=f"artist:{artist_name}", type="artist", limit=1)
artist_id = results["artists"]["items"][0]["id"]

top_tracks = sp.artist_top_tracks(artist_id, country="US")["tracks"]

data = []
for track in top_tracks[:10]:
    duration_min = track["duration_ms"] / 60000
    data.append({
        "name": track["name"],
        "popularity": track["popularity"],
        "duration_min": duration_min
    })

df = pd.DataFrame(data)

df_sorted = df.sort_values(by="popularity", ascending=True)
print("\n=== Top 3 canciones menos populares ===")
print(df_sorted.head(3))

sns.scatterplot(data=df, x="duration_min", y="popularity")
plt.title(f"Popularidad vs Duración - {artist_name}")
plt.xlabel("Duración (min)")
plt.ylabel("Popularidad")
plt.show()

correlation = df['duration_min'].corr(df['popularity'])
if correlation > 0:
    print("Parece haber una correlación positiva: las canciones más largas tienden a ser más populares.")
elif correlation < 0:
    print("Parece haber una correlación negativa: las canciones más cortas tienden a ser más populares.")
else:
    print("No se observa una correlación clara entre duración y popularidad.")

