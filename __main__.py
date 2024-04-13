import os
from scraper import Scraper
from tqdm import tqdm

# Paths
current_folder = os.path.dirname(__file__)
categories_path = os.path.join(current_folder, 'categories.txt')

scraper = Scraper()

if __name__ == '__main__':
    
    # read and categories
    with open(categories_path, 'r') as f:
        categories = f.readlines()
        
    # Detect last row from excel

    for category in categories:
        categories_pages = scraper.__get_pages_urls__(category)
        
        max_pages = len(categories_pages)
        for category_page in categories_pages:
            page_index = categories_pages.index(category_page) + 1
            products = scraper.__get_products__(category_page, page_index, max_pages)
            
            print("\t\tScrapping products details...")
            for product in tqdm(products):
                product_url = product['url']
                products_details = scraper.__get_product_details__(product_url, product)
                
                # Write products in excel