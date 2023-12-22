
import re
import requests
from parsel import Selector
from urllib.parse import urljoin
import json

product_urls = [
    'https://www.amazon.com/dp/B07RWRJ4XW/',
]

product_data_list = []

for product_url in product_urls:
    try:
        response = requests.get(product_url)
        print(response.status_code)
        if response.status_code == 200:
            sel = Selector(text=response.text)
            #image_data = json.loads(re.findall(r"colorImages':.*'initial':\s*(\[.+?\])},\n", response.text)[0])
            #variant_data = re.findall(r'dimensionValuesDisplayData"\s*:\s* ({.+?}),\n', response.text)
            #feature_bullets = [bullet.strip() for bullet in sel.css("#feature-bullets li ::text").getall()]
            price_1 = sel.css('.priceToPay ::text').get()

            price_2 = sel.css('.a-price .a-offscreen .a-price-whole ::text').get()
            
            product_data_list.append({
                "name": sel.css("#productTitle::text").get("").strip(),
                "price_1": price_1,
                "price_2": price_2,
                "stars": sel.css("i[data-hook=average-star-rating] ::text").get("").strip(),
                "rating_count": sel.css("div[data-hook=total-review-count] ::text").get("").strip(),
                #"feature_bullets": feature_bullets,
                #"images": image_data,
                #"variant_data": variant_data,
            })
    except Exception as e:
            print("Error", e)
            
            
print(product_data_list)
    
