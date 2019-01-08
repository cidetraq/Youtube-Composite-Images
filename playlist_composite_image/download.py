try:
    import gdata.youtube
    import gdata.youtube.service
except BaseException:
    pass
import urllib
import requests
import json
import operator
import os
from apiclient.discovery import build

DEVELOPER_KEY='AIzaSyBDNGWqlt2M6x8US0mNq42ydHc2E-LUOUc'

youtube=build('youtube', 'v3', developerKey=DEVELOPER_KEY)

youtube.client_id='Youtube Composite Image'

d={}

def getInfo():
    global d

    with open('urls.txt') as f:
        for line in f:
            url_data = urllib.parse.urlparse(line)
            query = urllib.parse.parse_qs(url_data.query)
            if 'list' in query:
                playlistID=query['list'][0]
                playlistItems=youtube.playlistItems().list(playlistId=playlistID, 
                part="contentDetails, snippet").execute()
                totalResults=playlistItems['pageInfo']['totalResults']
                RESULTSPERPAGE=5
                x=0
                nextPageToken=playlistItems['nextPageToken']
                while x<totalResults:
                    if x==0:
                        newPlaylistItems=youtube.playlistItems().list(playlistId=playlistID, 
                        part="contentDetails, snippet").execute()
                    else:
                        newPlaylistItems=youtube.playlistItems().list(playlistId=playlistID, 
                        part="contentDetails, snippet",pageToken=nextPageToken).execute()
                    items=newPlaylistItems['items']
                    for item in items:
                        id=item['snippet']['resourceId']['videoId']
                        print(id)
                        viewsAndAdd(id)
                    try:
                        nextPageToken=newPlaylistItems['nextPageToken']
                    except KeyError:
                        pass
                    x+=RESULTSPERPAGE
         
            id = query["v"][0]
            id=id.strip()
            print(id)
            viewsAndAdd(id)

            

    print(d)
    sorted_d = sorted(d.items(), key=lambda x: x[1])
    sorted_d=dict(sorted_d)
    print(sorted_d)
    count=0
    d2={}
    for item in sorted_d:
        print(sorted_d[item])
        d2[count] = sorted_d[item]
        count+=1
    print(d2)
    count=0
    if not os.path.exists("source images"):
        os.makedirs("source images")
    """
    for item in d2:
        urllib.request.urlretrieve("http://img.youtube.com/vi/"+item[0]+"/0.jpg", "source images/"+str(count)+".jpg")
        print('Downloaded image '+str(count+1))
        count+=1
    """
    return d2

def viewsAndAdd(id):
    global d
    id=id
    searchUrl="https://www.googleapis.com/youtube/v3/videos?id="+id+"&key="+DEVELOPER_KEY+"&part=statistics"
    entry=youtube.videos().list(id=id, part='statistics, snippet').execute()
    all_data=entry['items']
    viewCount=all_data[0]['statistics']['viewCount']
    d[id]=int(viewCount)



