import spotipy
import spotipy.util as util
import pandas as pd
from matplotlib import pyplot as plt
import numpy

#First attempt at spotify analysis. 
#Have removed some of the sensitive parts of the code.
#Made various charts and plots of songs per artist statistics.
#Few problems with getting the request/redirect uri to work.



token = util.prompt_for_user_token('user',
                                   'playlist-read-collaborative',
                                   client_id= 'n/a',
                                   client_secret= 'n/a',
                                   redirect_uri='http://localhost')
sp = spotipy.Spotify(auth=token)

playlist = sp.user_playlist('user', 'playlist')
tracks = playlist['tracks']['items']
next_uri = playlist['tracks']['next']
for _ in range(int(playlist['tracks']['total'] / playlist['tracks']['limit'])):
    response = sp._get(next_uri)
    tracks += response['items']
    next_uri = response['next']

tracks_df = pd.DataFrame([(track['track']['id'],
                           track['track']['artists'][0]['name'],
                           track['track']['name'])
                           #parse_date(track['track']['album']['release_date']) if track['track']['album']['release_date'] else None,
                           #parse_date(track['added_at']))
                          for track in playlist['tracks']['items']],
                           columns=['id', 'artist', 'name'])
                         #columns=['id', 'artist', 'name', 'release_date', 'added_at'] )

#convert the dataframe to a csv file
tracks_df.to_csv(r'C:\Users\User\Documents\Visual studio code\liked_songs.csv')

tracks_csv = pd.read_csv('liked_songs.csv')
print(tracks_csv)
#print(tracks_df)   

#attempt to get track count by artist
artists = tracks_df.groupby('artist').id.count().reset_index()
artists = artists[::-1]
print("artists:")
print(artists.head())

#barchart of songs per artist
plt.bar(artists.artist.head(),artists.id.head())
#plt.show()

def absolute_value(val): #fucntion to help display numbers in the piechart.
    a  = numpy.round(val/100.*artists.head().id.sum(), 0)
    return a

#piechart of songs per artist
plt.pie(artists.head().id,labels=artists.artist.head(),autopct=absolute_value)
plt.title("Songs per Artist")
plt.axis('equal')
#plt.show()

top_artists = artists.sort_values('id',ascending=False).reset_index()
top_artists = top_artists.head(50)
print(top_artists)

bottom5_artists = artists.sort_values('id').reset_index()
bottom5_artists = bottom5_artists.head()
print(bottom5_artists)