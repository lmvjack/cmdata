# external modules
import http.client
# import ssl
# own module
from cmutils import get_all_cards_info, create_html, CmException, get_user_input


def main():
    # ssl._create_default_https_context = ssl._create_unverified_context
    conn_data = http.client.HTTPSConnection("www.cardmarket.com")
    conn_images = http.client.HTTPSConnection("product-images.s3.cardmarket.com")

    try:
        urls: list
        html_filename: str
        urls, html_filename = get_user_input()

        cards_info: list = get_all_cards_info(
            urls,
            conn_data,
            conn_images)

        create_html(cards_info, html_filename)
        print("End.")
        conn_data.close()
        conn_images.close()
        return

    except CmException as e:
        print(e)
        conn_data.close()
        conn_images.close()
        return
    except Exception as e:
        print(e)
        conn_data.close()
        conn_images.close()
        return


if __name__ == '__main__':
    main()
