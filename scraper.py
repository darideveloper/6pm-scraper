import os
import requests
from time import sleep
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from libs.web_scraping import WebScraping

load_dotenv()
USER_AGENT = os.getenv('USER_AGENT')
DEBUG = os.getenv('DEBUG') == 'True'
SHOW_CHROME = os.getenv('SHOW_CHROME') == 'True'


class Scraper(WebScraping):
    """ Scrape products from page 6pm.com """
    
    def __init__(self):
        
        self.home = 'https://www.6pm.com'
        
        # Init chrome
        super().__init__(
            headless=not SHOW_CHROME,
        )
    
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
        
        # Save page
        if DEBUG:
            with open('page.html', 'w') as f:
                f.write(soup.prettify())
        
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
            'last_page': '#searchPagination a:last-child',
        }
        
        # Get total pages number
        soup = self.__request_page__(category_url)
        try:
            last_page = soup.select(selectors['last_page'])[0].text
        except IndexError:
            last_page_int = 1
        else:
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
            
            Structure
            [
                {
                    'name': str,
                    'model': str,
                    'price': str,
                    'url': str,
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
    
    def __get_product_details__(self, product_url: str, product_data: dict) -> list:
        """ Get product detail from specific product in the page

        Args:
            product_url (str): URL of the product
            product_data (dict): Current product data

        Returns:
            dict: Product detail
            
            Structure
            [
                {
                    'name': str
                    'model': str,
                    'price': str,
                    'url': str,
                    'sku': str,
                    'images': list[str]
                    'color': str,
                    'size': str,
                    'stock': int
                }
                ...
            ]
        """
        
        selectors = {
            'sku': '[itemprop="sku"]',
            'color': 'form > div:first-child div label:nth-child(index)',
            'size_wrapper': '#sizingChooser + div > div:nth-child(index)',
            'size': '#sizingChooser + div > div:nth-child(index) label',
            'stock': '[name="colorId"] + div',
            'images': '[style="--grid-columns:2"] img',
        }
        
        products_data = []
        
        self.set_page(product_url)
        for _ in range(4):
            self.go_down()
            sleep(1)
        self.refresh_selenium()
        
        # Get sku and images
        sku = self.get_text(selectors['sku'])
        imgs = self.get_attribs(selectors['images'], 'srcset')
        imgs = list(map(lambda img: img.split("%20")[0], imgs))
        imgs = list(map(lambda img: img.split(" ")[0], imgs))
        product_data['sku'] = sku
        product_data['images'] = imgs
        
        # Extract each color and size combination
        selector_color_base = selectors['color'].replace(
            ':nth-child(index)',
            ''
        )
        selector_sizes_base = selectors['size'].replace(
            ':nth-child(index)',
            ''
        )
        color_num = len(self.get_elems(selector_color_base))
        sizes_num = len(self.get_elems(selector_sizes_base))
        for color_index in range(1, color_num + 1):
            for size_index in range(1, sizes_num + 1):
                
                # Select color
                selector_color = selectors["color"].replace(
                    'index',
                    str(color_index * 2)
                )
                self.click_js(selector_color)
                self.refresh_selenium()
                
                # Skip if size is not available
                selector_size_wrapper = selectors["size_wrapper"].replace(
                    'index',
                    str(size_index)
                )
                size_wrapper_classes = self.get_attrib(selector_size_wrapper, 'class')
                if len(size_wrapper_classes.split(' ')) == 2:
                    continue
                
                selector_size = selectors["size"].replace(
                    'index',
                    str(size_index)
                )
                self.click_js(selector_size)
                self.refresh_selenium()
                
                # Get color and size
                product_data['color'] = self.get_text(selector_color)
                product_data['size'] = self.get_text(selector_size)
                
                stock = self.get_text(selectors['stock'])
                if stock == 'ADD TO SHOPPING BAG':
                    stock = 10
                elif stock == 'OUT OF STOCK':
                    stock = 0
                else:
                    stock = int(stock.split(' ')[1])
                product_data['stock'] = stock
                products_data.append(product_data.copy())
                
        return products_data