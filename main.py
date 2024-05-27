import yt_dlp

def download_youtube_video(video_url, download_path):
    try:
        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'outtmpl': f'{download_path}/%(title)s.%(ext)s'
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
        print("Download completed!")
    except Exception as e:
        print(f"Error: {e}")


video_url = 'https://www.youtube.com/watch?v=RVhhCeQU-nA&t=1s'
download_path = 'vids'
download_youtube_video(video_url, download_path)
