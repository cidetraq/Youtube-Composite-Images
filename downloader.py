import subprocess

def download():
    with open('urls.txt') as f:
            for line in f:
                subprocess.Popen([
                    "youtube-dl",
                    "--write-thumbnail", "--skip-download", "--yes-playlist", '-o Playlist_images/%(title)s',
                    line])

