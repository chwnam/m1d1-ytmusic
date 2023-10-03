from os.path import dirname, exists as path_exists, join as path_join
from json import dumps as json_dumps

from dotenv import dotenv_values
from ytmusicapi import YTMusic


def main():
    env_path = path_join(dirname(__file__), '.env')

    if not path_exists(env_path):
        print('ERROR: .env file not found!')
        return

    config = dotenv_values(env_path)
    playlist_id = config['YOUTUBE_PLAYLIST_ID']
    list_limit = int(config['LIST_LIMIT'])

    ytm = YTMusic(path_join(dirname(__file__), 'oauth.json'))
    playlist = ytm.get_playlist(playlistId=playlist_id)

    sequence = int(playlist['trackCount'])
    tracks = playlist['tracks']
    items = []

    for track in tracks:
        items.append(
            {
                'yt_id': track['videoId'],
                'artist': track['artists'][0]['name'],
                'title': track['title'],
                'length': track['duration'],
                'sequence': sequence,
            }
        )
        sequence -= 1
        list_limit -= 1
        if 0 == list_limit:
            break

    print(json_dumps(items, ensure_ascii=False))


if __name__ == '__main__':
    main()
