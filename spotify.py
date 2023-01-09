from pprint import pprint
import requests
import time
tok = '' #place token in here
def get_current_track(token):
    '''gets the track info based on the users token'''
    response = requests.get('https://api.spotify.com/v1/me/player', headers = {"Authorization":f"Bearer {token}"})
    resp_json = response.json()
    id = resp_json['item']['id']
    song = resp_json['item']['name']
    artists = resp_json['item']['artists']
    names = ', '.join([artist['name'] for artist in artists])
    progress = int(resp_json['progress_ms'])
    duration = resp_json['item']['duration_ms']
    link = resp_json['item']['external_urls']['spotify']
    
    current_track = song, names, progress, link, duration
    return current_track

def ms_secMin(ms):
    '''converts the ms to seconds min'''
    sec = ms//1000
    min = sec//60
    sec %= 60
    return min,sec 
def main():
    while True:
        song, artists, progress, link, duration = get_current_track(tok)
        percent = f'{progress/duration*100:.2f}%'
        min, sec = ms_secMin(duration)
        print(f"Song: {song}, Artist(s): {artists}, Progress: {percent}, Song Length: {min} min, {sec} sec, link: {link}")
        time.sleep(1)
if __name__ == '__main__':
    main()
