import os
import subprocess
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/play', methods=['POST'])
def play():
    links = request.json.get('links')
    for link in links:
        download(link)
    subprocess.Popen(['mplayer', '-playlist', 'playlist.txt'], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    return 'Playing'

def download(link):
    cmd = f'yt-dlp -x --audio-format mp3 -o "downloads/%(title)s.%(ext)s" {link}'
    subprocess.run(cmd, shell=True)
    with open('playlist.txt', 'a') as f:
        f.write(f"downloads/{link.split('=')[1]}.mp3\n")

if __name__ == '__main__':
    if not os.path.exists('downloads'):
        os.makedirs('downloads')
    app.run()
    
