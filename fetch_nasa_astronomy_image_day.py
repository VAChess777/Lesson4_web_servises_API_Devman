import os
from datetime import datetime
from pathlib import Path

import requests
from dotenv import load_dotenv


def get_astronomy_pictures_day(
        nasa_api_key, url, path,
        start_date, end_date):
    payload = {
        'start_date': start_date,
        'end_date': end_date,
        'api_key': nasa_api_key
    }
    response = requests.get(
        url,
        params=payload
    )
    response.raise_for_status()
    urls_pictures_day = []
    for hdurl in response.json():
        if hdurl.get('hdurl'):
            urls_pictures_day.append(hdurl.get('hdurl'))
    for images_numbers, urls_pictures_day in enumerate(urls_pictures_day, 1):
        filename = f'nasa_apod_{images_numbers}.jpg'
        image = requests.get(urls_pictures_day)
        image.raise_for_status()
        with open(Path(f'{path}', f'{filename}'), 'wb') as file:
            file.write(image.content)


def create_parser():
    parser = argparse.ArgumentParser(
        description=
        'The program downloads astronomical images of the day from the NASA server.'
    )
    parser.add_argument(
        '-s',
        '--start_date',
        default=datetime.today().strftime('%Y-%m-%d'),
        help=
        'Enter the command in console:'
        '$ python fetch_nasa_astronomy_image_day.py -s(--start_date) {YYYY-mm-dd}. '
        'Where YYYY-mm-dd - is the start date for the download astronomy image day from NASA. '
        'if you do not enter -s(--start_date), then default = today'
    )
    parser.add_argument(
        '-e',
        '--end_date',
        default=datetime.today().strftime('%Y-%m-%d'),
        help=
        'Enter the command in console:'
        '$ python fetch_nasa_astronomy_image_day.py -e(--end_date) {YYYY-mm-dd}. '
        'Where YYYY-mm-dd - is the end date for the download astronomy image day from NASA. '
        'if you do not enter -e(--end_date), then default = today'
    )
    return parser


def main():
    load_dotenv()
    nasa_api_key = os.environ['NASA_API_KEY']
    url = 'https://api.nasa.gov/planetary/apod'
    Path('image_day_Nasa').mkdir(parents=True, exist_ok=True)
    path = 'image_day_Nasa'
    parser = create_parser()
    start_date = parser.parse_args().start_date
    end_date = parser.parse_args().end_date
    get_astronomy_pictures_day(nasa_api_key, url, path, start_date, end_date)


if __name__ == '__main__':

    main()
