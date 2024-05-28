from flask import Flask, request, render_template, jsonify, send_file
import yt_dlp
import os
import tempfile

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
        video_count = info.get('n_entries', 1)
        return jsonify({'thumbnail_url': thumbnail_url, 'title': title, 'video_count': video_count})
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/download', methods=['POST'])
def download():
    video_url = request.form.get('video_url')
    video_title = request.form.get('video_title')
    if not video_url:
        return jsonify({'error': "No URL provided."})
    try:
        temp_dir = tempfile.mkdtemp()
        file_path = download_youtube_video(video_url, video_title, temp_dir)
        return send_file(file_path, as_attachment=True)
    except Exception as e:
        return jsonify({'error': str(e)})

def fetch_video_info(video_url):
    ydl_opts = {}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(video_url, download=False)
        if 'entries' in info:  # Playlist
            first_video = info['entries'][0]
            info['thumbnail'] = first_video['thumbnail']
            info['title'] = info['title']
            info['n_entries'] = len(info['entries'])
    return info

def download_youtube_video(video_url, video_title, temp_dir):
    try:
        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'outtmpl': os.path.join(temp_dir, f'{video_title}.%(ext)s')
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
        downloaded_file = os.listdir(temp_dir)[0]
        return os.path.join(temp_dir, downloaded_file)
    except Exception as e:
        raise e

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
