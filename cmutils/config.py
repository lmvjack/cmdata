from dotenv import load_dotenv
import os

########## ENV DATA (to get cookie for request) ##########
load_dotenv()
cookie = os.getenv('COOKIE')

########## TIME (to wait from a request to another in order not to get blocked ##########
NEXT_REQ_WAIT_TIME = 10

########## REQUEST HEADERS (to make requests) ##########

headers = {
    'Cookie': os.getenv('COOKIE') or "",
    'Host': "www.cardmarket.com",
    'Cache-Control': "max-age=0",
    'Sec-Ch-Ua': "\"Not=A?Brand\";v=\"99\", \"Chromium\";v=\"118\"",
    'Sec-Ch-Ua-Mobile': "?0",
    'Sec-Ch-Ua-Full-Version': "\"\"",
    'Sec-Ch-Ua-Arch': "\"\"",
    'Sec-Ch-Ua-Platform': "\"macOS\"",
    'Sec-Ch-Ua-Platform-Version': "\"\"",
    'Sec-Ch-Ua-Model': "\"\"",
    'Sec-Ch-Ua-Bitness': "\"\"",
    'Sec-Ch-Ua-Full-Version-List': "",
    'Upgrade-Insecure-Requests': "1",
    'User-Agent': "Mozilla/5.0 (iPhone; CPU iPhone OS 5_1 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9B176 Safari/7534.48.3",
    'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    'Sec-Fetch-Site': "none",
    'Sec-Fetch-Mode': "navigate",
    'Sec-Fetch-User': "?1",
    'Sec-Fetch-Dest': "document",
    'Accept-Encoding': "gzip, deflate, br",
    'Accept-Language': "en-GB,en-US;q=0.9,en;q=0.8",
    'Connection': "keep-alive",
}

img_headers = {
    "Referer": "https://www.cardmarket.com/",
}


########## CSS SELECTORS (to get data from HTML response) ##########
prices_categories = ['From','Price Trend', '30-days average price', '7-days average price', '1-day average price']
NAME_SELECTOR = 'body > main > div.page-title-container.d-flex.align-items-center.text-break > div.flex-grow-1 > h1'
MAIN_DIV_SELECTOR = '#tabContent-info > div > div.col-12.col-lg-6.mx-auto > div'
PRICES_SELECTOR = '.col-6.col-xl-7'

# not useful anymore
'''selectors = {
     'Name': 'body > main > div.page-title-container.d-flex.align-items-center.text-break > div.flex-grow-1 > h1',
     'From':'#tabContent-info > div > div.col-12.col-lg-6.mx-auto > div > div.info-list-container.col-12.col-md-8.col-lg-12.mx-auto.align-self-start > dl > dd:nth-child(10)',
     'Price Trend': '#tabContent-info > div > div.col-12.col-lg-6.mx-auto > div > div.info-list-container.col-12.col-md-8.col-lg-12.mx-auto.align-self-start > dl > dd:nth-child(12) > span',
     '30-days average price':'#tabContent-info > div > div.col-12.col-lg-6.mx-auto > div > div.info-list-container.col-12.col-md-8.col-lg-12.mx-auto.align-self-start > dl > dd:nth-child(14) > span',
     '7-days average price':'#tabContent-info > div > div.col-12.col-lg-6.mx-auto > div > div.info-list-container.col-12.col-md-8.col-lg-12.mx-auto.align-self-start > dl > dd:nth-child(16) > span',
     '1-day average price':'#tabContent-info > div > div.col-12.col-lg-6.mx-auto > div > div.info-list-container.col-12.col-md-8.col-lg-12.mx-auto.align-self-start > dl > dd:nth-child(18) > span'
}'''

#if __name__ == "__main__":
    #main()