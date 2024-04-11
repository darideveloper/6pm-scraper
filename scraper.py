import os
import requests
from time import sleep
from dotenv import load_dotenv
from bs4 import BeautifulSoup

load_dotenv()
USER_AGENT = os.getenv('USER_AGENT')


class Scraper():
    """ Scrape products from page 6pm.com """
    
    def __init__(self):
        
        self.home = 'https://www.6pm.com'
    
    def __request_page__(self, url: str) -> BeautifulSoup:
        """ Request page and return BeautifulSoup object
        
        Args:
            url (str): URL of the page
        
        Returns:
            BeautifulSoup: BeautifulSoup object
        """
        
        # Request page
        sleep(3)
        res = requests.get(url, headers={'User-Agent': USER_AGENT})
        soup = BeautifulSoup(res.text, 'html.parser')
        
        return soup
    
    def __get_pages_urls__(self, category_url: str) -> list:
        """ Return list of pages URL from category URL
        
        Args:
            category_url (str): URL of the category
        
        Returns:
            list: List of pages URL
        """
        
        category_url_small = category_url.split('/')[0:4]
        category_url_small = '/'.join(category_url_small)
        print(f'Getting pages from category {category_url_small}')
        
        selectors = {
            'last_page': '.Am-z > a:last-child',
        }
        
        # Get total pages number
        soup = self.__request_page__(category_url)
        last_page = soup.select(selectors['last_page'])[0].text
        last_page_int = int(last_page)
        
        # Generate pages URL
        urls = []
        for page_index in range(last_page_int):
            url = f'{category_url}&p={page_index}'
            urls.append(url)
        
        return urls
        
    def __get_products__(self, category_page_url: str, page_num: int,
                         max_pages: int) -> list:
        """ Get products data from current page and return data

        Args:
            category_url (str): URL of the category
            page_num (int): Page number
            max_pages (int): Max pages number

        Returns:
            list: List of products
            
            Example:
            [
                {
                    'name': 'Name',
                    'model': 'Model',
                    'brand': 'Brand',
                    'price': 'Price',
                    'url': 'url',
                }
                ...
            ]
        """
        
        print(f'\tGetting products from page {page_num} / {max_pages}')
        
        selectors = {
            'product': 'article[data-low-stock]',
            'texts': {
                'name': 'dd[itemprop="brand"]',
                'model': 'dd[itemprop="name"]',
                'price': '[itemprop="price"]',
            },
            'url': 'a',
        }
        
        # Get page data
        soup = self.__request_page__(category_page_url)
        
        products_data = []
        products_elems = soup.select(selectors['product'])
        for product_elem in products_elems:
            product_data = {}
                        
            # Get product detail
            for selector_name, selector in selectors['texts'].items():
                product_data[selector_name] = product_elem.select(selector)[0].text
            
            # Get product url
            url = product_elem.select(selectors['url'])[0]['href']
            product_data['url'] = self.home + url
            products_data.append(product_data)
            
        return products_data
    
    def __get_product_detail__(self, product_url: str) -> dict:
        """ Get product detail from specific product in the page

        Args:
            product_url (str): URL of the product

        Returns:
            dict: Product detail
            
            Example:
            [
                TODO
            ]
        """
        pass