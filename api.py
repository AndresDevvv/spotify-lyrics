import os
import json
from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
import requests
from dotenv import load_dotenv

load_dotenv()

SPOTIFY_BEARER = os.environ.get("SPOTIFY_BEARER")
SPOTIFY_CLIENT_TOKEN = os.environ.get("SPOTIFY_CLIENT_TOKEN")

CACHE_DIR = "cache"
os.makedirs(CACHE_DIR, exist_ok=True)

@asynccontextmanager
async def lifespan(app: FastAPI):
    if not SPOTIFY_BEARER or not SPOTIFY_CLIENT_TOKEN:
        raise RuntimeError(
            "Missing SPOTIFY_BEARER or SPOTIFY_CLIENT_TOKEN environment variables."
        )
    yield

app = FastAPI(lifespan=lifespan)

HEADERS_BASE = {
    "sec-ch-ua-platform": "\"Windows\"",
    "Referer": "https://open.spotify.com/",
    "accept-language": "en",
    "sec-ch-ua": "\"Not;A=Brand\";v=\"99\", \"Google Chrome\";v=\"139\", \"Chromium\";v=\"139\"",
    "spotify-app-version": "1.2.71.24.gedb225df",
    "sec-ch-ua-mobile": "?0",
    "app-platform": "WebPlayer",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36",
    "accept": "application/json",
}

def get_color_lyrics(track_id: str, market: str, vocal_removal: bool):
    cache_file = os.path.join(CACHE_DIR, f"{track_id}.json")
    if os.path.exists(cache_file):
        with open(cache_file, "r") as f:
            return json.load(f)

    base = "https://spclient.wg.spotify.com/color-lyrics/v2/track"
    url = f"{base}/{track_id}"
    params = {
        "format": "json",
        "vocalRemoval": str(vocal_removal).lower(),
        "market": market,
    }
    headers = {
        **HEADERS_BASE,
        "authorization": f"Bearer {SPOTIFY_BEARER}",
        "client-token": SPOTIFY_CLIENT_TOKEN,
    }

    try:
        r = requests.get(url, headers=headers, params=params, timeout=20)
        r.raise_for_status()
        data = r.json()
        with open(cache_file, "w") as f:
            json.dump(data, f)
        return data
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/lyrics/{track_id}")
async def get_lyrics(track_id: str, market: str = "from_token", vocal_removal: bool = False):
    return get_color_lyrics(track_id, market, vocal_removal)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)