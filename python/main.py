""""
Project: PythonClient
Platform: Kamyroll
Script: main.py
Author: hyugogirubato
Date: 2022.10.15
"""

import json
import Kamyroll

# CHANNEL_ID = ['adn', 'neko-sama', 'crunchyroll']


if __name__ == '__main__':
    client = Kamyroll.Client(channel_id='crunchyroll', locale='fr-FR')
    if client.channel_id == 'adn':
        series_id = '699'  # High School DxD
        media_id = '14346'  # S1.Ep1
    elif client.channel_id == 'neko-sama':
        series_id = '5785'  # High School DxD
        media_id = '5785-01-vostfr'  # S1.Ep1
    elif client.channel_id == 'crunchyroll':
        series_id = 'GR2P21J9R'  # High School DxD
        media_id = 'GRZXG2VMY'  # S1.Ep1
    else:
        series_id = ''
        media_id = ''

    # response = client.search('High')
    # response = client.seasons(series_id)
    # response = client.media(series_id)
    # response = client.movies(series_id)
    # response = client.streams(media_id, format='ass')
    response = client.updated(limit=10)
    print(json.dumps(response, indent=4, sort_keys=False))