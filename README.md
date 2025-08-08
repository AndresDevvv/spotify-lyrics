# Spotify Lyrics API

This project provides an unofficial API to fetch song lyrics from Spotify. It uses an undocumented internal endpoint, so use it at your own risk.

## Features

-   Fetches synchronized, color-coded lyrics.
-   Caches responses to JSON files to avoid repeated requests.
-   Built with FastAPI.

## API Documentation

### Endpoint

`GET /lyrics/{track_id}`

### Parameters

-   `track_id` (string, required): The Spotify track ID.
-   `market` (string, optional, default: "from_token"): The market to use for the request.
-   `vocal_removal` (boolean, optional, default: False): Whether to request lyrics with vocals removed.

### Example Request

```bash
curl http://localhost:8000/lyrics/4a8pP5X2lxwU5aprY44jLn
```

### Example Response

```json
{
    "lyrics": {
        "syncType": "LINE_SYNCED",
        "lines": [
            {
                "startTimeMs": "1000",
                "words": "This is an example",
                "syllables": []
            }
        ]
    }
}
```

## How to Run

1.  **Clone the repository:**

    ```bash
    git clone <repository_url>
    cd spotify-lyrics
    ```

2.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

3.  **Create a `.env` file:**

    Create a `.env` file in the `spotify-lyrics` directory by copying the `.env.example` file:

    ```bash
    cp .env.example .env
    ```

    Then, open the `.env` file and add your Spotify credentials:

    ```
    SPOTIFY_BEARER="your_bearer_token"
    SPOTIFY_CLIENT_TOKEN="your_client_token"
    ```

4.  **Run the server:**

    ```bash
    python api.py
    ```

    The server will be running at `http://localhost:8000`.