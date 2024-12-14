# external
import http.client
import os

from bs4 import BeautifulSoup
import time
import sys

from .exceptions import CmException
from .config import (headers as config_headers, img_headers as config_img_headers,
NEXT_REQ_WAIT_TIME, MAIN_DIV_SELECTOR, prices_categories, NAME_SELECTOR, PRICES_SELECTOR)

import http.client
import socket


def make_request(conn: http.client.HTTPSConnection, url: str, headers: dict, method="GET") \
        -> http.client.HTTPResponse | None:
    try:
        conn.request(method, url, "", headers)
        response = conn.getresponse()

        if response.status == 200:
            return response
        else:
            print(f"Error for {url}: {response.status} {response.reason}")
            return None

    except http.client.HTTPException as e:
        raise CmException(f"HTTPException: {e}")
    except socket.timeout as e:
        raise CmException(f"Socket Timeout: {e}")
    except Exception as e:
        raise CmException(f"An unexpected error occurred: {e}")


def download_image(url: str, name: str, conn_images: http.client.HTTPSConnection) -> str | None:
    res: http.client.HTTPResponse | None = make_request(conn_images, url, config_img_headers)
    if res:
        data: bytes = res.read()
        folder: str = 'downloads'
        filename: str = f'{name}.jpg'
        if not os.path.exists(folder):
            os.makedirs(folder)

        fullpath: str = os.path.join(folder, filename)

        with open(fullpath, 'wb') as image_file:
            image_file.write(data)
        return filename
    else:
        print(f"Failed to access the image. Status: {res.status} {res.reason}")
        return None


def decode_http_response(res: http.client.HTTPResponse) -> str:
    data = res.read()
    content_encoding = res.getheader("Content-Encoding")
    match content_encoding:
        case "gzip":
            import gzip
            data = gzip.decompress(data)
        case "deflate":
            import zlib
            data = zlib.decompress(data)
        case "br":
            import brotli
            data = brotli.decompress(data)
        case _:
            raise CmException("Couldn't decode HTTP response")

    # Decode the byte data into plain HTML
    try:
        content = data.decode("utf-8")
    except UnicodeDecodeError:
        # Fallback to ISO-8859-1 if UTF-8 fails
        content = data.decode("ISO-8859-1")
    except Exception as e:
        raise CmException(f"An unexpected error occurred: {e}")

    return content


def get_card_info(url: str, conn_data: http.client.HTTPSConnection, conn_images: http.client.HTTPSConnection) \
        -> dict | None:
    res: http.client.HTTPResponse | None = make_request(conn_data, url, config_headers)
    if res is None:
        print(f"{url}: Failed to get the card. Check if the url is correct.")
        return res

    content: str = decode_http_response(res)
    soup = BeautifulSoup(content, "html.parser")

    '''before this I used CSS selectors for all the data, 
    but for some cards it didn't work because of a different page structure'''
    #### prices ####
    outer_div = soup.select(MAIN_DIV_SELECTOR)
    card_name_div = soup.select(NAME_SELECTOR)

    if len(outer_div) == 0 or len(card_name_div) == 0:
        print(f"{url}: Failed to get card info. Problem retrieving info.")
        return None

    prices_divs = outer_div[0].select(PRICES_SELECTOR)
    if len(prices_divs) < 5:
        print(f"{url}: Failed to get card info. Problem retrieving prices.")
        return None
    prices = prices_divs[-5:]

    card_info = {'Name': card_name_div[0].text}
    for index, x in enumerate(prices):
        price_category = prices_categories[index]
        card_info[price_category] = prices[index].text

    ''' I used this because I couldn't get img tag with selectors
     but only from a list of all images. Will try to fix'''
    #### image ####
    image_url = soup.find_all('img')[3].get('src')
    image_name = download_image(image_url, card_info['Name'], conn_images)
    card_info['Image'] = image_name

    return card_info


def get_all_cards_info(urls: list, conn_data: http.client.HTTPSConnection, conn_images: http.client.HTTPSConnection) \
        -> list:
    cards_info = []
    for card_id, url in enumerate(urls):
        new_card = get_card_info(url, conn_data, conn_images)
        if new_card is not None:
            cards_info.append(new_card)
            print(f'{cards_info[-1]["Name"]} - Request successful!')
        else:
            print("Continuing...")

        progress_bar(NEXT_REQ_WAIT_TIME) if card_id < len(urls) - 1 else None
    print("Downloading process finished.")

    return cards_info

def progress_bar(duration):
    print("Waiting to make the next request...")

    bar_length = 40
    interval = duration / bar_length

    for i in range(1, bar_length + 1):
        time.sleep(interval)

        sys.stdout.write('\r')
        sys.stdout.write(f"[{'#' * i}{'.' * (bar_length - i)}] {i * 100 // bar_length}%")
        sys.stdout.flush()

    sys.stdout.write('\n')