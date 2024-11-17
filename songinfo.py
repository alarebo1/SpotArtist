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
                trackname.append(artist.get('name'))
                musiclink.append(artist.get('preview_url'))
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
