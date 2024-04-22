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
        
    sheets = SpreadsheetManager('products.xlsx')
    sheets.clean_workbook()
    sheets.create_set_sheet('products')
    
    # Delete content and write headers
    sheets.write_data([
        ["name", "model", "price", "url", "sku", "color", "size", "stock", "imgs"],
    ])
    sheets.save()
    
    # Detect last row from excel
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
                    product_detail_values = [
                        product_detail['name'],
                        product_detail['model'],
                        product_detail['price'],
                        product_detail['url'],
                        product_detail['sku'],
                        product_detail['color'],
                        product_detail['size'],
                        product_detail['stock'],
                    ]
                    product_detail_values += images
                    excel_data.append(product_detail_values)
                sheets.write_data(excel_data, last_row + 1)
                sheets.save()
                
                # update last row
                last_row += len(excel_data)