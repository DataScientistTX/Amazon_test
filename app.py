import streamlit as st 
import validators
import re
import requests
from parsel import Selector
from bs4 import BeautifulSoup

def pull_amazon_data(url):
    product_data_list = []

    product_url = url
    try:
        response = requests.get(product_url)
        print(response.status_code)
        if response.status_code == 200:
            sel = Selector(text=response.text)
            #variant_data = re.findall(r'dimensionValuesDisplayData"\s*:\s* ({.+?}),\n', response.text)
            #feature_bullets = [bullet.strip() for bullet in sel.css("#feature-bullets li ::text").getall()]
            
            soup = BeautifulSoup(response.content, features="lxml")
            price_whole, price_fraction = [], []
            price = soup.find_all("span")

            for i in price:
                try:
                    if i['class'] == ['a-price-whole']:

                        itemPrice = f"${str(i.get_text())[:-1]}"
                        price_whole.append(itemPrice)
                        
                    if i['class'] == ['a-price-fraction']:

                        itemPrice = f"${str(i.get_text())}"
                        price_fraction.append(itemPrice)
                        
                except KeyError:
                    continue


            product_data_list.append({
                "name": sel.css("#productTitle::text").get("").strip(),
                "price": sel.css('.a-price-whole::text').get() + '.' + sel.css('.a-price-fraction::text').get(),
                "whole_price":  price_whole,
                "fraction_price": price_fraction,
                "stars": sel.css("i[data-hook=average-star-rating] ::text").get("").strip(),
                "rating_count": sel.css("#acrCustomerReviewText::text").get("").strip(),
            #    "feature_bullets": feature_bullets,
            #    "variant_data": variant_data,
            })
    except Exception as e:
            print("Error", e)
        
    return product_data_list

entered_value = st.text_input('Enter SKU or URL', 'test')

if entered_value == 'test':
    st.write('Please input a valid SKU or URL')

if entered_value != 'test' :
    if validators.url(entered_value):
        #It is a URL 
        url = entered_value
    else:
        #It is a SKU
        url = 'https://www.amazon.com/dp/' + entered_value + '/'

    st.write(url)

    result = pull_amazon_data(url=url)
    st.write(result)