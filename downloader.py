import subprocess

def download():
    with open('urls.txt') as f:
            for line in f:
                subprocess.call([
                    "youtube-dl",
                    "--write-thumbnail", "--skip-download", "--yes-playlist", '-o Playlist images/%(title)s',
                    line])

