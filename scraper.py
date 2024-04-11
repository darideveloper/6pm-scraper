import requests
from bs4 import BeautifulSoup


class Scraper():
    """ Scrape products from page 6pm.com """
    
    def __init__(self):
        pass
    
    def __get_pages_urls__(self, category_url: str) -> list:
        """ Return list of pages URL from category URL
        
        Args:
            category_url (str): URL of the category
        
        Returns:
            list: List of pages URL
        """
        
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