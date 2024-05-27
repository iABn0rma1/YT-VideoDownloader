from flask import Flask, request, render_template, jsonify
import os
import yt_dlp

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/fetch_info', methods=['POST'])
def fetch_info():
    video_url = request.form.get('video_url')
    if not video_url:
        return jsonify({'error': 'No URL provided.'})
    try:
        info = fetch_video_info(video_url)
        thumbnail_url = info['thumbnail']
        title = info['title']
        return jsonify({'thumbnail_url': thumbnail_url, 'title': title})
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/download', methods=['POST'])
def download():
    video_url = request.form.get('video_url')
    if not video_url:
        return jsonify({'error': "No URL provided."})
    try:
        if 'playlist' in video_url:
            download_youtube_playlist(video_url)
            return jsonify({'message': "Playlist download completed!"})
        else:
            download_youtube_video(video_url)
            return jsonify({'message': "Video download completed!"})
    except Exception as e:
        return jsonify({'error': str(e)})

def fetch_video_info(video_url):
    ydl_opts = {}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(video_url, download=False)
    return info

def download_youtube_video(video_url):
    try:
        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'outtmpl': os.path.join(get_user_downloads_path(), '%(title)s.%(ext)s')
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
    except Exception as e:
        raise e

def download_youtube_playlist(playlist_url):
    try:
        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'outtmpl': os.path.join(get_user_downloads_path(), '%(playlist_index)s - %(title)s.%(ext)s'),
            'noplaylist': False  # Ensure that the entire playlist is downloaded
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([playlist_url])
    except Exception as e:
        raise e

def get_user_downloads_path():
    return os.path.join(os.path.expanduser('~'), 'Downloads')

if __name__ == '__main__':
    app.run(debug=True)
