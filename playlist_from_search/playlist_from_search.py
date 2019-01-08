#!/usr/bin/env python
# coding: utf-8

# In[43]:


#Do this first to override google's argparse
from apiclient.discovery import build
import requests
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.errors import HttpError
import user_config
import argparse
#Relies on oauth2client
from oauth2client import client
from oauth2client.tools import run_flow
from oauth2client.file import Storage


# In[2]:


import user_config
DEVELOPER_KEY=user_config.DEVELOPER_KEY
CLIENT_SECRETS_FILE='client_secrets.json'
SCOPES=["https://www.googleapis.com/auth/youtube"]
API_SERVICE_NAME='youtube'
API_VERSION='v3'


# youtube=build('youtube', 'v3', developerKey=DEVELOPER_KEY)
# youtube.client_id='playlist-test'
# playlist_items=youtube.playlistItems().list(part='snippet', playlistId='PL_DbUpBdiJTFnQDKIHl87bbuNrkNz7C_L')
# result=playlist_items.execute()\
# result

# In[3]:


def build_resource(properties):
    resource = {}
    for p in properties:
        # Given a key like "snippet.title", split into "snippet" and "title", where
        # "snippet" will be an object and "title" will be a property in that object.
        prop_array = p.split('.')
        ref = resource
        for pa in range(0, len(prop_array)):
            is_array = False
            key = prop_array[pa]

              # For properties that have array values, convert a name like
              # "snippet.tags[]" to snippet.tags, and set a flag to handle
              # the value as an array.
            if key[-2:] == '[]':
                key = key[0:len(key)-2:]
                is_array = True

            if pa == (len(prop_array) - 1):
                # Leave properties without values out of inserted resource.
                if properties[p]:
                    if is_array:
                        ref[key] = properties[p].split(',')
                    else:
                        ref[key] = properties[p]
            elif key not in ref:
                # For example, the property is "snippet.title", but the resource does
                # not yet have a "snippet" object. Create the snippet object here.
                # Setting "ref = ref[key]" means that in the next time through the
                # "for pa in range ..." loop, we will be setting a property in the
                # resource's "snippet" object.
                ref[key] = {}
                ref = ref[key]
            else:
            # For example, the property is "snippet.description", and the resource
            # already has a "snippet" object.
                ref = ref[key]
    return resource


# In[26]:


def playlists_insert(client, properties, **kwargs):
    # See full sample for function
    resource = build_resource(properties)

    # See full sample for function
    kwargs = remove_empty_kwargs(**kwargs)

    response = client.playlists().insert(
    body=resource,
    **kwargs
    ).execute()

    return response


# In[6]:


def playlist_items_insert(client, properties, **kwargs):
    # See full sample for function
    resource = build_resource(properties)

    # See full sample for function
    kwargs = remove_empty_kwargs(**kwargs)

    response = client.playlistItems().insert(
    body=resource,
    **kwargs
    ).execute()

    return response


# In[7]:


def remove_empty_kwargs(**kwargs):
    good_kwargs = {}
    if kwargs is not None:
        for key, value in kwargs.items():
            if value:
                good_kwargs[key] = value
    return good_kwargs


# In[8]:


def print_response(response):
    print(response)


# In[42]:


def get_authenticated_service(): # Modified
    credential_path = 'credentials.json'
    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRETS_FILE, SCOPES)
        credentials = run_flow(flow, store)
    return build(API_SERVICE_NAME, API_VERSION, credentials=credentials)


# In[10]:


def youtube_search(client, options):
    # Call the search.list method to retrieve results matching the specified
    # query term.
    query=options.q
    max_results=options.m
    search_response = client.search().list(
    q=query,
    part='id',
    maxResults=max_results
    ).execute()

    video_ids = []
    #channels = []
    #playlists = []

    for search_result in search_response.get('items', []):
        if search_result['id']['kind'] == 'youtube#video':
            video_ids.append('%s' % (search_result['id']['videoId']))
            
    return video_ids


# In[36]:


def main(client, options):
    query=options.q
    new_playlist_properties={'snippet.title': query,
    #'snippet.description': 'Test',
    #'snippet.tags[]': 'Test',
    'snippet.defaultLanguage': 'en',
    'status.privacyStatus': 'public'}
    try:
        new_playlist_id=playlists_insert(client, new_playlist_properties, part='snippet,status')['id']
        video_ids=youtube_search(client, options)
        for video_id in video_ids:
            video_add_properties={'snippet.playlistId': new_playlist_id,
            'snippet.resourceId.kind': 'youtube#video',
            'snippet.resourceId.videoId': video_id
            }
            playlist_items_insert(client, video_add_properties, part='snippet')
    except HttpError as e:
        print('An HTTP error %d occurred:\n%s' % (e.resp.status, e.content))
    print('Process completed.')


# class test_options:
#     q='Brian Eno'
#     max_results=2

# test_search=youtube_search(client, test_options)

# test_search

# import datetime
# str(datetime.datetime.now())

# test_response=playlists_insert(client, 
#     {'snippet.title': str(datetime.datetime.now()),
#      #'snippet.description': '',
#      #'snippet.tags[]': '',
#      'snippet.defaultLanguage': 'en',
#      'status.privacyStatus': 'public'},
#     part='snippet,status')

# test_response['id']

# query='Test2'
# play_id='123'
# video_id='456'

# new_playlist=playlists_insert(client, properties, part='id')

# playlist_items_insert(client, 
#     {'snippet.playlistId': '',
#      'snippet.resourceId.kind': 'youtube#video',
#      'snippet.resourceId.videoId': 'M7FIvfx5J10',
#      #'snippet.position': '',
#     },
#     #part='id'
#     #onBehalfOfContentOwner='')
#                      )

# try:
#     videos_to_add=youtube_search(args)
# except HttpError, e:
#     print('An HTTP error %d occurred:\n%s' % (e.resp.status, e.content))

# In[ ]:


#imports()
client=get_authenticated_service()
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-q', type=str, help='Search term')
    parser.add_argument('-m', type=int, help='Max results', default=25)
    #parser.add_argument('-a', '--add-existing', help='Specify playlist name or leave blank to create new playlist', default=None)
    args = parser.parse_args()
    main(client,args)

