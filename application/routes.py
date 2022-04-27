
from flask import render_template, request, redirect, url_for
from app import app
from flask import request

import pandas as pd
from bs4 import BeautifulSoup
from urllib.request import urlopen 
import requests

headers_std = {
'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36',
'Content-Type': 'text/html',
}

@app.route("/", methods=["GET", "POST"])
def home():
    return render_template("index.html")


@app.route('/add', methods=[ 'GET', 'POST'])
def add():
    # for amazon

    search = request.form['todoitem']
    url = "https://www.amazon.in/s?k=" + search

    html_am = requests.get(url,headers=headers_std).text
    soup_am = BeautifulSoup(html_am,'lxml')


    product_name_class = "a-size-medium a-color-base a-text-normal"
    actual_price_class = "a-price-whole"



    #scrape the product details
    product_names = soup_am.find_all("span", {"class":product_name_class})
    product_prices = soup_am.find_all("span",{"class":actual_price_class})


    product_names_df = []
    product_prices_df = []     

    #make a dataframe
    for i in range(len(product_names)-1):

        product_names_df.append(product_names[i].text.strip())
        product_prices_df.append(product_prices[i].text.strip())

    df_am = pd.DataFrame({'product_name':product_names_df,'price (INR)':product_prices_df})
    am_data = df_am.head()




#for flipkart

    url_fp = "https://www.flipkart.com/search?q="+ search

    html_fp = requests.get(url_fp,headers=headers_std).text
    soup_fp = BeautifulSoup(html_fp,'lxml')

    product_name_class = "_4rR01T"
    actual_price_class = "_30jeq3 _1_WHN1"
    #product_image_class = "_396cs4 _3exPp9" 

    product_name_1 = soup_fp.find_all("div", {"class":product_name_class})
    product_actual_price_1 = soup_fp.find_all("div",{"class":actual_price_class})
    #product_image = soup.find_all("img",{"class": product_image_class})[1]

    #print(product_image["src"])


    product_names_flipkart_df = []
    product_prices_flipkart_df = []


    for i in range(len(product_actual_price_1)):

        product_names_flipkart_df.append(product_name_1[i].text.strip())
        product_prices_flipkart_df.append(product_actual_price_1[i].text.strip())

    df_fp = pd.DataFrame({'product_name':product_names_flipkart_df,'price (INR)':product_prices_flipkart_df})
    fp_data =df_fp.head()

    print(fp_data)
    print(am_data)
    
    return render_template("list.html", am_tables =[am_data.to_html(classes='data', header="true")], fp_tables =[fp_data.to_html(classes='data', header="true")],title_fp=fp_data.columns.values,title_am=am_data.columns.values)






