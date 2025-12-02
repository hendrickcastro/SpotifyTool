"""
Spotify Playlist Downloader
Downloads your Spotify playlists as MP3 files
"""

import subprocess
import sys
from pathlib import Path
from typing import Optional

import spotipy
from spotipy.oauth2 import SpotifyOAuth
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Prompt, Confirm
from rich.panel import Panel

from config import config

console = Console()


class SpotifyDownloader:
    """Main class for downloading Spotify playlists"""
    
    def __init__(self):
        self.sp: Optional[spotipy.Spotify] = None
        self.user_id: Optional[str] = None
    
    def authenticate(self) -> bool:
        """Authenticate with Spotify API"""
        if not config.validate():
            console.print("[bold red]Error:[/] Missing Spotify credentials!")
            console.print("Please copy 'env_example.txt' to '.env' and fill in your credentials.")
            console.print("Get your credentials from: https://developer.spotify.com/dashboard")
            return False
        
        try:
            auth_manager = SpotifyOAuth(
                client_id=config.SPOTIFY_CLIENT_ID,
                client_secret=config.SPOTIFY_CLIENT_SECRET,
                redirect_uri=config.SPOTIFY_REDIRECT_URI,
                scope=config.SPOTIFY_SCOPE,
                cache_path=".spotify_cache"
            )
            self.sp = spotipy.Spotify(auth_manager=auth_manager)
            
            # Get current user info
            user_info = self.sp.current_user()
            self.user_id = user_info["id"]
            console.print(f"[green]✓[/] Logged in as: [bold]{user_info['display_name']}[/]")
            return True
            
        except Exception as e:
            console.print(f"[bold red]Authentication failed:[/] {e}")
            return False
    
    def get_playlists(self) -> list:
        """Get all playlists for the current user"""
        if not self.sp:
            return []
        
        playlists = []
        results = self.sp.current_user_playlists(limit=50)
        
        while results:
            for item in results["items"]:
                playlists.append({
                    "id": item["id"],
                    "name": item["name"],
                    "tracks": item["tracks"]["total"],
                    "owner": item["owner"]["display_name"],
                    "uri": item["uri"]
                })
            
            if results["next"]:
                results = self.sp.next(results)
            else:
                break
        
        return playlists
    
    def get_liked_songs(self) -> list:
        """Get user's liked songs"""
        if not self.sp:
            return []
        
        tracks = []
        results = self.sp.current_user_saved_tracks(limit=50)
        
        while results:
            for item in results["items"]:
                track = item["track"]
                tracks.append({
                    "name": track["name"],
                    "artist": ", ".join(a["name"] for a in track["artists"]),
                    "album": track["album"]["name"],
                    "uri": track["uri"]
                })
            
            if results["next"]:
                results = self.sp.next(results)
            else:
                break
        
        return tracks
    
    def get_playlist_tracks(self, playlist_id: str) -> list:
        """Get all tracks from a playlist"""
        if not self.sp:
            return []
        
        tracks = []
        results = self.sp.playlist_tracks(playlist_id)
        
        while results:
            for item in results["items"]:
                track = item.get("track")
                if track and track.get("uri"):
                    tracks.append({
                        "name": track["name"],
                        "artist": ", ".join(a["name"] for a in track["artists"]),
                        "album": track["album"]["name"],
                        "uri": track["uri"]
                    })
            
            if results["next"]:
                results = self.sp.next(results)
            else:
                break
        
        return tracks
    
    def display_playlists(self, playlists: list) -> None:
        """Display playlists in a nice table"""
        table = Table(title="Your Spotify Playlists", show_header=True)
        table.add_column("#", style="cyan", justify="right")
        table.add_column("Name", style="green")
        table.add_column("Tracks", style="yellow", justify="right")
        table.add_column("Owner", style="blue")
        
        for idx, playlist in enumerate(playlists, 1):
            table.add_row(
                str(idx),
                playlist["name"],
                str(playlist["tracks"]),
                playlist["owner"]
            )
        
        console.print(table)
    
    def download_tracks(self, tracks: list, output_dir: Path, playlist_name: str = "") -> None:
        """Download tracks using spotdl"""
        if not tracks:
            console.print("[yellow]No tracks to download.[/]")
            return
        
        # Create output directory
        if playlist_name:
            safe_name = "".join(c for c in playlist_name if c.isalnum() or c in (" ", "-", "_")).strip()
            output_dir = output_dir / safe_name
        
        output_dir.mkdir(parents=True, exist_ok=True)
        
        console.print(f"\n[bold]Downloading {len(tracks)} tracks to:[/] {output_dir}")
        
        # Get all track URIs
        track_uris = [t["uri"] for t in tracks]
        
        # Build spotdl command
        cmd = [
            sys.executable, "-m", "spotdl",
            "--output", str(output_dir),
            "--format", config.AUDIO_FORMAT,
            "--bitrate", str(config.AUDIO_QUALITY),
        ] + track_uris
        
        try:
            # Run spotdl
            process = subprocess.run(
                cmd,
                capture_output=False,
                text=True
            )
            
            if process.returncode == 0:
                console.print(f"\n[bold green]✓ Download completed![/]")
            else:
                console.print(f"\n[yellow]Download finished with some issues.[/]")
                
        except FileNotFoundError:
            console.print("[bold red]Error:[/] spotdl not found. Install it with: pip install spotdl")
        except Exception as e:
            console.print(f"[bold red]Download error:[/] {e}")
    
    def download_playlist_by_url(self, url: str) -> None:
        """Download a playlist directly by URL using spotdl"""
        output_dir = config.ensure_download_dir()
        
        console.print(f"\n[bold]Downloading playlist from URL...[/]")
        
        cmd = [
            sys.executable, "-m", "spotdl",
            "--output", str(output_dir),
            "--format", config.AUDIO_FORMAT,
            "--bitrate", str(config.AUDIO_QUALITY),
            url
        ]
        
        try:
            subprocess.run(cmd, capture_output=False, text=True)
            console.print(f"\n[bold green]✓ Download completed![/]")
        except Exception as e:
            console.print(f"[bold red]Download error:[/] {e}")


def main():
    """Main application entry point"""
    console.print(Panel.fit(
        "[bold cyan]🎵 Spotify Playlist Downloader 🎵[/]\n"
        "Download your Spotify playlists as MP3 files",
        border_style="cyan"
    ))
    
    downloader = SpotifyDownloader()
    
    # Check for direct URL mode
    if len(sys.argv) > 1:
        url = sys.argv[1]
        if "spotify.com" in url or "spotify:" in url:
            console.print(f"[cyan]Downloading from URL:[/] {url}")
            downloader.download_playlist_by_url(url)
            return
    
    # Authenticate
    if not downloader.authenticate():
        return
    
    while True:
        console.print("\n[bold]Options:[/]")
        console.print("  [cyan]1.[/] List and download playlists")
        console.print("  [cyan]2.[/] Download liked songs")
        console.print("  [cyan]3.[/] Download by Spotify URL")
        console.print("  [cyan]4.[/] Exit")
        
        choice = Prompt.ask("\nSelect an option", choices=["1", "2", "3", "4"], default="1")
        
        if choice == "1":
            # Get and display playlists
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console
            ) as progress:
                progress.add_task("Fetching playlists...", total=None)
                playlists = downloader.get_playlists()
            
            if not playlists:
                console.print("[yellow]No playlists found.[/]")
                continue
            
            downloader.display_playlists(playlists)
            
            # Select playlist
            console.print("\n[dim]Enter playlist number(s) separated by comma, 'all' for all, or 'back' to go back[/]")
            selection = Prompt.ask("Select playlist(s)")
            
            if selection.lower() == "back":
                continue
            
            selected_playlists = []
            if selection.lower() == "all":
                selected_playlists = playlists
            else:
                try:
                    indices = [int(x.strip()) - 1 for x in selection.split(",")]
                    selected_playlists = [playlists[i] for i in indices if 0 <= i < len(playlists)]
                except ValueError:
                    console.print("[red]Invalid selection.[/]")
                    continue
            
            if not selected_playlists:
                console.print("[yellow]No valid playlists selected.[/]")
                continue
            
            # Confirm download
            total_tracks = sum(p["tracks"] for p in selected_playlists)
            console.print(f"\n[bold]Selected {len(selected_playlists)} playlist(s) with {total_tracks} total tracks.[/]")
            
            if not Confirm.ask("Proceed with download?"):
                continue
            
            # Download each playlist
            output_dir = config.ensure_download_dir()
            
            for playlist in selected_playlists:
                console.print(f"\n[bold cyan]Processing:[/] {playlist['name']}")
                
                with Progress(
                    SpinnerColumn(),
                    TextColumn("[progress.description]{task.description}"),
                    console=console
                ) as progress:
                    progress.add_task(f"Fetching tracks from {playlist['name']}...", total=None)
                    tracks = downloader.get_playlist_tracks(playlist["id"])
                
                downloader.download_tracks(tracks, output_dir, playlist["name"])
        
        elif choice == "2":
            # Download liked songs
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console
            ) as progress:
                progress.add_task("Fetching liked songs...", total=None)
                tracks = downloader.get_liked_songs()
            
            if not tracks:
                console.print("[yellow]No liked songs found.[/]")
                continue
            
            console.print(f"\n[bold]Found {len(tracks)} liked songs.[/]")
            
            if not Confirm.ask("Proceed with download?"):
                continue
            
            output_dir = config.ensure_download_dir()
            downloader.download_tracks(tracks, output_dir, "Liked Songs")
        
        elif choice == "3":
            # Download by URL
            url = Prompt.ask("Enter Spotify URL (playlist, album, or track)")
            
            if not url:
                continue
            
            downloader.download_playlist_by_url(url)
        
        elif choice == "4":
            console.print("[cyan]Goodbye! 👋[/]")
            break


if __name__ == "__main__":
    main()

