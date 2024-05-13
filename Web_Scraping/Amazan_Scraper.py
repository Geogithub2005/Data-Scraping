from datetime import datetime
import requests
import csv
import bs4
#A string representing the user agent, which identifies the browser or client making the request. To check in--(https://www.whatismybrowser.com/)
USER_AGENT='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36' 
REQUEST_HEADER={
    'User-Agent':USER_AGENT,
    'Accept-Language':'en-US,en;q=0.5'
    } #A dictionary containing request headers, including the user agent and accept language.

def get_page_html(url):
    res=requests.get(url=url,headers=REQUEST_HEADER)
    return res.content

def get_product_price(soup):
    main_price_span = soup.find('span', attrs={
        'class': 'a-price aok-align-center reinventPricePriceToPayMargin priceToPay'
    })
    if main_price_span:
        price_spans = main_price_span.findAll('span')
        if price_spans:
            for span in price_spans:
                price = span.text.strip().replace('₹', '').replace(',', '')
                try:
                    price_float = float(price)
                    return price_float
                except ValueError:
                    continue
        else:
            print("Price spans not found.")
            return None
    else:
        print("Main price span not found.")
        return None

def get_product_title(soup):
    get_product_title=soup.find('span',id='productTitle')
    return get_product_title.text.strip()

def get_product_rating(soup):
    get_product_rating_div=soup.find('div',attrs={
        'id':'averageCustomerReviews'
    })
    product_rating_section=get_product_rating_div.find(
        'i', attrs={'class':'a-icon-star'})
    product_rating_span=product_rating_section.find('span')
    try:
        rating=product_rating_span.text.strip().split()
        return float(rating[0])
    except ValueError:
        print("Value Obtained for price could not be parsed")
        exit()

def get_product_technical_details(soup): 
    details={}
    technical_details_section=soup.find('div',id='prodDetails')
    data_tables=technical_details_section.findAll('table',class_='prodDetTable')
    for table in data_tables:
        table_rows =table.findAll('tr')
        for row in table_rows:
            row_key =row.find('th').text.strip()
            row_value=row.find('td').text.strip().replace('\u200e','')
            details[row_key]=row_value
    return details

def extract_product_info(url):
    product_info={}
    print(f'Scraping URL :{url}')
    html=get_page_html(url=url)
    soup=bs4.BeautifulSoup(html,'lxml')
    product_info['Price']=get_product_price(soup)
    product_info['Title']=get_product_title(soup)
    product_info['Rating']=get_product_rating(soup)
    product_info.update(get_product_technical_details(soup))
    return product_info

if __name__ == "__main__":
    product_data=[]
    with open('amazan_products_urls.csv',newline='') as csvfile:
        reader=csv.reader(csvfile,delimiter=',')
        for row in reader:
            url = row[0]
            product_data.append(extract_product_info(url))
        
    output_file_name = 'ouput-{}.csv'.format(datetime.today().strftime("%m-%d-%Y"))
    with open(output_file_name,'w') as outputfile:
        writer=csv.writer(outputfile)
        writer.writerow(product_data[0].keys())
        for product in product_data:
            writer.writerow(product.values())
