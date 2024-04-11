import os
from scraper import Scraper

# Paths
current_folder = os.path.dirname(__file__)
categories_path = os.path.join(current_folder, 'categories.txt')

scraper = Scraper()

if __name__ == '__main__':
    
    # read and categories
    with open(categories_path, 'r') as f:
        categories = f.readlines()

    for category in categories:
        categories_urls = scraper.__get_pages_urls__(category)
        
        for category_url in categories_urls:
            page_index = categories_urls.index(category_url) + 1
            products = scraper.__get_products__(category_url, page_index)

# import requests
# from libs.web_scraping import WebScraping

# url = 'https://www.6pm.com/women-dresses/CKvXARDE1wHAAQHiAgMBAhg.zso?pf_rd_r=TAZW5WP7390E7EFED51K&pf_rd_p=9a889a1b-da0f-4e16-8c25-0095ad735c94'

# # Basic requests
# res = requests.get(url)
# with open('http-basic-requests.html', 'w') as f:
#     f.write(res.text)
    
# # Basic requests
# user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
# res = requests.get(url, headers={'User-Agent': user_agent})
# with open('http-user-agent-requests.html', 'w') as f:
#     f.write(res.text)