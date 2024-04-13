import os
from scraper import Scraper
from tqdm import tqdm
from libs.xlsx import SpreadsheetManager

# Paths
current_folder = os.path.dirname(__file__)
categories_path = os.path.join(current_folder, 'categories.txt')

scraper = Scraper()

if __name__ == '__main__':
    
    # read and categories
    with open(categories_path, 'r') as f:
        categories = f.readlines()
        
    # Detect last row from excel
    sheets = SpreadsheetManager('products.xlsx')
    sheets.create_set_sheet('products')
    old_data = sheets.get_data()
    old_data = list(filter(lambda row: row[0], old_data))
    last_row = len(old_data)

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
                excel_data = []
                for product_detail in products_details:
                    images = product_detail['images']
                    del product_detail['images']
                    excel_data.append(list(product_detail.values()) + images)
                sheets.write_data(excel_data, last_row + 1)
                sheets.save()
                
                # update last row
                last_row += len(excel_data)