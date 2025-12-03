# 🎵 Musicalar - Music Downloader & 432Hz Converter

Download your Spotify playlists and liked songs as MP3 files.

## Features

- ✅ List all your Spotify playlists
- ✅ Download single or multiple playlists
- ✅ Download liked songs
- ✅ Download by Spotify URL (playlists, albums, tracks)
- ✅ High quality MP3 (320kbps)
- ✅ Automatic metadata tagging
- ✅ Beautiful CLI interface

## Requirements

- Python 3.8+
- FFmpeg (required by spotdl)
- Spotify Developer Account

## Installation

### 1. Install FFmpeg

**Windows (using winget):**
```bash
winget install FFmpeg
```

**Windows (using Chocolatey):**
```bash
choco install ffmpeg
```

**Or download directly from:** https://ffmpeg.org/download.html

### 2. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 3. Set up Spotify API credentials

1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Log in with your Spotify account
3. Click "Create App"
4. Fill in:
   - App name: `SpotifyDL`
   - App description: `Personal playlist downloader`
   - Redirect URI: `http://localhost:8888/callback`
5. Click "Save"
6. In your app settings, copy the **Client ID** and **Client Secret**

### 4. Configure the application

1. Rename `env_example.txt` to `.env`
2. Edit `.env` and fill in your credentials:

```
SPOTIFY_CLIENT_ID=your_client_id_here
SPOTIFY_CLIENT_SECRET=your_client_secret_here
```

## Usage

### Interactive Mode

Run the main script:

```bash
python spotify_downloader.py
```

This will:
1. Open a browser for Spotify authentication (first time only)
2. Show a menu with options:
   - List and download your playlists
   - Download your liked songs
   - Download by Spotify URL

### Direct URL Mode

Download directly from a Spotify URL:

```bash
python spotify_downloader.py "https://open.spotify.com/playlist/YOUR_PLAYLIST_ID"
```

You can also use:
- Album URLs: `https://open.spotify.com/album/...`
- Track URLs: `https://open.spotify.com/track/...`
- Spotify URIs: `spotify:playlist:...`

## Download Location

By default, songs are downloaded to the `./downloads` folder.
You can change this in the `.env` file:

```
DOWNLOAD_PATH=./my_music
```

## Configuration Options

| Variable | Default | Description |
|----------|---------|-------------|
| `SPOTIFY_CLIENT_ID` | - | Your Spotify Client ID |
| `SPOTIFY_CLIENT_SECRET` | - | Your Spotify Client Secret |
| `SPOTIFY_REDIRECT_URI` | `http://localhost:8888/callback` | OAuth redirect URI |
| `DOWNLOAD_PATH` | `./downloads` | Where to save downloaded files |
| `AUDIO_FORMAT` | `mp3` | Output format (mp3, flac, ogg, opus, m4a) |
| `AUDIO_QUALITY` | `320` | Bitrate in kbps |

## Troubleshooting

### "spotdl not found"
Make sure you installed all dependencies:
```bash
pip install -r requirements.txt
```

### "FFmpeg not found"
Install FFmpeg and make sure it's in your system PATH.

### Authentication issues
Delete the `.spotify_cache` file and try again.

### Songs not downloading
Some songs might not be available on YouTube. spotdl will skip these automatically.

## Legal Notice

This tool is for personal use only. Respect copyright laws and Spotify's Terms of Service. Downloaded content should be for personal backup purposes only.

## License

MIT License

