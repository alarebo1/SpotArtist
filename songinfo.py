import requests
import os
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())


AUTH_URL = 'https://accounts.spotify.com/api/token'
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET =os.getenv("CLIENT_SECRET")
TRACK_URL = "https://api.spotify.com/v1/albums/"
SEARCH_URL ="https://api.spotify.com/v1/search?query="

ALBUM_URL ="https://api.spotify.com/v1/albums/"
# spotify accesses requist
auth_response = requests.post(AUTH_URL, {
    'grant_type': 'client_credentials',
    'client_id': CLIENT_ID,
    'client_secret': CLIENT_SECRET
})

auth_response_data = auth_response.json()

access_token = auth_response_data['access_token']

headers = {
    'Authorization': 'Bearer {}'.format(access_token)
}
songname = []
trackname = []
musiclink = []
tmpurl = []
imgheight = []
imgurl = []
aid = []
found = []
aidname = []  
def searcharitst(Artid):
    try:
        if len(songname)>1:
            songname.clear()
            imgurl.clear()
            musiclink.clear()
            imgheight.clear()
            tmpurl.clear()
            aid.clear()
            trackname.clear()
        #searching artist using there name and getting the are album
        SEARCH_API=SEARCH_URL+Artid+"&type=album&country=US&limit=10&offset=5"
        response = requests.get(SEARCH_API,headers=headers)
        searResult = response.json().get("albums").get('items')
        for album in searResult:
            aid.append(album.get('id'))
            songname.append(album.get('name'))
            
            albumresponse = requests.get(ALBUM_URL+album.get('id'),headers=headers)
            albumData = albumresponse.json().get('images')
            for artist in albumData:
                try:
                    tmpurl.append(artist.get("height"))
                    imgheight.append(artist.get('url'))
                except AttributeError:
                    print("error getting images")
            trackresponse = requests.get(ALBUM_URL+album.get('id')+"/tracks?"+"limit=1",headers=headers)
            trackdata = trackresponse.json().get('items')

            for artist in trackdata:
                track_title = artist.get('name')
                embed_url = search_youtube(Artid+track_title)
                videolink.append(embed_url)

                trackname.append(track_title)
                # Replace Spotify preview with Apple iTunes preview
                preview_url = get_preview_from_itunes(Artid, track_title)
                musiclink.append(preview_url if preview_url else '')

            for i, word in enumerate(musiclink):
                if word == None:
                    musiclink[i] = ''
            for i, word in enumerate(trackname):
                if word == None:
                    musiclink[i] = ''
        for i, word in enumerate(tmpurl):
            if tmpurl[i]==300:
                imgurl.append(imgheight[i])
        dupdelete(Artid)
    except KeyError or TypeError:
        found.clear()
        found.append(0)
def checkArtist(Artid):
    searcharitst(Artid)
    if len(found)==1:   
        return True
    else: 
        return False
tmpsong = songname
tmpimg = []
tmpmusic = []
artistname = []
previwlist = []
imglist = []
def dupdelete(Artid):
    for i, word in enumerate(tmpsong):       
        if (word.lower()==Artid.lower()):
            del songname[i]
            del musiclink[i]
            del imgurl[i]
            dupdelete(Artid)
#searching songs using artist id 
def idsearch(Artid):
    try:
        if len(artistname)>1:
            artistname.clear()
            imglist.clear()
            previwlist.clear()
            aidname.clear()
        ARTIST_TRACK_API = "https://api.spotify.com/v1/artists/"+Artid+"/top-tracks?market=US"
        response = requests.get(ARTIST_TRACK_API,headers=headers)
        trackresponse = response.json()        
        aidname.append(trackresponse.get("tracks")[0].get("artists")[0].get("name"))
        for i in  range(len(trackresponse.get("tracks"))):
            artistname.append(trackresponse.get("tracks")[i].get("album").get("name"))
            previwlist.append(trackresponse.get("tracks")[i].get("preview_url"))
            imglist.append(trackresponse.get("tracks")[i].get("album").get("images")[0].get("url"))
            artistname.append(trackresponse.get("tracks")[0].get("album").get("name"))
        return aidname
    except TypeError:
        found.clear()
        found.append(0)
def get_preview_from_itunes(artist, track):
    query = f"{artist} {track}"
    url = f"https://itunes.apple.com/search?term={requests.utils.quote(query)}&entity=song&limit=1"
    res = requests.get(url)
    if res.status_code == 200:
        results = res.json().get('results')
        if results:
            return results[0].get('previewUrl')
    return ''
def search_youtube(query):
    import re
    search_url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
    response = requests.get(search_url)

    video_ids = re.findall(r"watch\?v=(\S{11})", response.text)
    unique_ids = list(dict.fromkeys(video_ids))  # remove duplicates

    embed_links = [f"https://www.youtube.com/embed/{vid}" for vid in unique_ids[:2]]
    if len (embed_links)> 0:
        return embed_links[0]
    return ""
