from flask import Flask, request, send_file
import youtube_dl
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        link = request.form['link']
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': 'music/%(title)s.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(link, download=True)
            filename = ydl.prepare_filename(info_dict)
        os.system(f"vlc --play-and-exit --qt-start-minimized {filename}")
        os.remove(filename)
        return "音楽が再生されました。"
    return '''
        <form method="post">
            <label for="link">YouTubeリンク:</label>
            <input type="text" name="link" id="link" required>
            <input type="submit" value="再生">
        </form>
    '''

if __name__ == '__main__':
    app.run()
    
