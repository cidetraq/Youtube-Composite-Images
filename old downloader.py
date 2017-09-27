import subprocess
import shutil
import os

def download():
    if os.access("source images", os.F_OK):
        shutil.rmtree("source images")
    with open('urls.txt') as f:
            for line in f:
                subprocess.call([
                    "youtube-dl",
                    "--write-thumbnail", "--skip-download", "--yes-playlist", "-o", "source images/%(title)s",
                    line])
    
