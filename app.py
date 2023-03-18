#!/usr/bin/env python
# coding: utf-8

from flask import Flask, render_template, request, Response
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import csv
import io

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', mimetype='text/html')

@app.route('/search', methods=['POST'])
def search():
    isrc_codes = request.form['isrc_code']
    isrc_codes = isrc_codes.replace(' ', '').split(',')

    client_credentials_manager = SpotifyClientCredentials(
        client_id='d849ef50cadd46f4a20433793ba904c3',
        client_secret='08838db9151d4a728e279d0950b8164f'
    )
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    data = []
    
    for code in isrc_codes:
        try:
            track_result = sp.search(q=f'isrc:{code}', type='track', limit=1)
            track_item = track_result['tracks']['items'][0]
            track_id = track_item['id']
            song_title = track_item['name']
            artist_name = track_item['artists'][0]['name']
            release_date = track_item['album']['release_date']
            data.append({'ISRC Code': code, 'Song Title': song_title, 'Artist Name': artist_name, 'Release Date': release_date, 'Track ID': track_id})
        except:
            data.append({'ISRC Code': code, 'Song Title': 'Not found', 'Artist Name': 'Not found', 'Release Date': 'Not found', 'Track ID': 'Not found'})

    columns = ['ISRC Code', 'Song Title', 'Artist Name', 'Release Date', 'Track ID']
    df = pd.DataFrame(data, columns=columns)

    return render_template('result.html', tables=[df.to_html(classes='data', header="true", index=False)], titles=df.columns.values, mimetype='text/html')

@app.route('/download', methods=['POST'])
def download():
    isrc_codes = request.form['isrc_code']
    isrc_codes = isrc_codes.replace(' ', '').split(',')

    client_credentials_manager = SpotifyClientCredentials(
        client_id='d849ef50cadd46f4a20433793ba904c3',
        client_secret='08838db9151d4a728e279d0950b8164f'
    )
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    data = []

    for code in isrc_codes:
        try:
            track_result = sp.search(q=f'isrc:{code}', type='track', limit=1)
            track_item = track_result['tracks']['items'][0]
            track_id = track_item['id']
            song_title = track_item['name']
            artist_name = track_item['artists'][0]['name']
            release_date = track_item['album']['release_date']
            data.append({'ISRC Code': code, 'Song Title': song_title, 'Artist Name': artist_name, 'Release Date': release_date, 'Track ID': track_id})
        except:
            data.append({'ISRC Code': code, 'Song Title': 'Not found', 'Artist Name': 'Not found', 'Release Date': 'Not found', 'Track ID': 'Not found'})

    columns = ['ISRC Code', 'Song Title', 'Artist Name', 'Release Date', 'Track ID']
    df = pd.DataFrame(data, columns=columns)

    # Create a buffer for the CSV data
    buffer = io.StringIO()

    # Write the DataFrame to the buffer as a CSV file
    df.to_csv(buffer, index=False)

    # Set the buffer's position to the beginning of the stream
    buffer.seek(0)

    # Create a response object with the CSV data
    response = Response(
        buffer.getvalue(),
        mimetype='text/csv',
        headers={
            'Content-Disposition': f'attachment;filename=isrc_results.csv'
        }
    )

    return response
