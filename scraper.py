import os
import requests
from dotenv import load_dotenv
from bs4 import BeautifulSoup

load_dotenv()
USER_AGENT = os.getenv('USER_AGENT')


class Scraper():
    """ Scrape products from page 6pm.com """
    
    def __init__(self):
        pass
    
    def __request_page__(self, url: str) -> BeautifulSoup:
        """ Request page and return BeautifulSoup object
        
        Args:
            url (str): URL of the page
        
        Returns:
            BeautifulSoup: BeautifulSoup object
        """
        
        # Request page
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

        
    def __get_products_category__(self, category_page_url: str) -> list:
        """ Get products data from specific category,
            in current page and return data

        Args:
            category_url (str): URL of the category

        Returns:
            list: List of products
            
            Example:
            [
                [
                    
                ]
                ...
            ]
        """
        pass
    
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