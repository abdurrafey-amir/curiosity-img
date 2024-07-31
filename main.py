from argparse import ArgumentParser
import os
import requests
import sys
import datetime as dt
import re
from dotenv import load_dotenv

load_dotenv()

api_key = os.environ.get('api_key')
DATE = re.compile(r"(\d\d\d\d)-(\d\d)-(\d\d)")
timeout = 20


def main():
    if not api_key:
        sys.exit('api key not set')

    parser = ArgumentParser(description="an api explorer that can get mars rover curiosity's images")
    parser.add_argument("-m", "--mars", nargs=2, dest="mars", metavar=("file_name", "date"), help="write the Mars rover image urls to a text file")

    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit()

    if args.mars is not None:
        file_name, date = args.mars
        mars_rover_photos(file_name, date)

def mars_rover_photos(file_name, date):
    if not re.search(DATE, date):
        print('invalid date format, use YYYY-MM-DD.')
        return False
    
    if not file_name or file_name == " " or not file_name.endswith(".txt"):
        print("invalid file name, must contain characters and end with .txt")
        return False
    
    date_year, date_month, date_day = date.split("-")

    try:
        date_dt = dt.datetime(year=int(date_year), month=int(date_month), day=int(date_day))
    except ValueError:
        print('invalid date, use correct values for year, month, day.')
        return False
    
    if date_dt > dt.datetime.today():
        print('date must not be after today.')
        return False
    
    mars_endpoint = "https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos"
    params = {
        'earth_date': date,
        'api_key': api_key
    }

    print('getting api response...')
    api_response = requests.get(mars_endpoint, params, timeout=timeout)
    rover_images = api_response.json()

    try: 
        photos = rover_images['photos']
    except KeyError:
        print('inavlid date/api key.')
        return False
    
    images = []
    with open(file_name, 'w', encoding='utf-8') as file:
        for photo in photos:
            image_url = photo['img_src']
            file.write(f'{image_url}\n')
            images.append(image_url)

    try:
        file_extension = os.path.splitext(images[0])[-1].lower()
    except IndexError:
        sys.exit()

    file_name = f'mars{file_extension}'
    image = requests.get(image_url, timeout=timeout)

    with open(file_name, 'wb', encoding=None) as file:
        file.write(image.content)
        print('image fetched.')

    return api_response.status_code



if __name__ == "__main__":
    main()