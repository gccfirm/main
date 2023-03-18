#!/usr/bin/env python
# coding: utf-8

from flask import Flask, render_template, request
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', mimetype='text/html')

@app.route('/search', methods=['POST'])
def search():
    isrc_code = request.form['isrc_code']

    client_credentials_manager = SpotifyClientCredentials(
        client_id='d849ef50cadd46f4a20433793ba904c3',
        client_secret='08838db9151d4a728e279d0950b8164f'
    )
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    try:
        track_result = sp.search(q=f'isrc:{isrc_code}', type='track', limit=1)
        track_item = track_result['tracks']['items'][0]
        track_id = track_item['id']
        song_title = track_item['name']
        artist_name = track_item['artists'][0]['name']
        release_date = track_item['album']['release_date']
    except:
        track_id = 'Not found'
        song_title = 'Not found'
        artist_name = 'Not found'
        release_date = 'Not found'

    return render_template('result.html', song_title=song_title, artist_name=artist_name, release_date=release_date, track_id=track_id)

if __name__ == '__main__':
    app.run(debug=True)
