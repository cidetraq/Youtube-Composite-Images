try:
    import gdata.youtube
    import gdata.youtube.service
except BaseException:
    pass
import urllib
import requests
import json
import urlparse

yt_service = gdata.youtube.service.YouTubeService()
yt_service.developer_key= 'AIzaSyBDNGWqlt2M6x8US0mNq42ydHc2E-LUOUc'
yt_service.client_id='Youtube Composite Image'

with open('urls.txt') as f:
    for line in f:
        url_data = urlparse.urlparse("http://www.youtube.com/watch?v=z_AbfPXTKms&NR=1")
        query = urlparse.parse_qs(url_data.query)
        id = query["v"][0]
        searchUrl="https://www.googleapis.com/youtube/v3/videos?id="+id+"&key="+yt_service.developer_key+"&part=statistics"
        response = urllib.urlopen(searchUrl).read()
        data = json.loads(response)
        print(data)
        all_data=data['items']
        viewCount=all_data[0]['statistics']['viewCount']
        print viewCount




