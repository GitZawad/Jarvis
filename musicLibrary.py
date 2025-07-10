import yt_dlp
import webbrowser

def search_and_play(song_name):
    # yt-dlp search query format for YouTube
    query = f"ytsearch:{song_name}"
    
    options = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'quiet': True,
        'extract_flat': True  # Only extract URLs
    }

    with yt_dlp.YoutubeDL(options) as ydl:
        info = ydl.extract_info(query, download=False)
        if 'entries' in info:
            first_result = info['entries'][0]
            video_url = f"https://www.youtube.com/watch?v={first_result['id']}"
            print(f"Playing: {first_result['title']}")
            webbrowser.open(video_url)
        else:
            print("No results found.")
