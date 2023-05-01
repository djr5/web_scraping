import csv
import requests
from bs4 import BeautifulSoup

category_list = ["for_sale", "for_rent", "recently_sold"]

base_url = "https://www.zillow.com/homes/"
headers = {
    "authority": "www.zillow.com",
    "path": "/homes/",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
    "scheme": "https",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "en-US,en;q=0.9"
}
page = 1

# Extracting the listings
data_list = []
for catg in category_list:
    for i in range(1, 1000):
        url = base_url + catg + '/{0}'.format(str(i) + '_p')
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        listings = soup.find_all(
            'div', {'class': 'search-page-list-container'})
        if listings:
            uls = listings[0].find_all('ul')
            articles = uls[0].find_all('article')
            category = "Sale" if catg == "for_sale" else (
                "Rent" if catg == "for_rent" else "Sold")
            for item in articles:
                address = item.select_one(
                    'address[data-test="property-card-addr"]').text.strip()
                address_list = address.split(',')
                address_list_content = address_list[-1].strip().split(' ')
                if len(address_list_content) < 2:
                    address_list_content.append('N/A')
                state, zip_code = tuple(address_list_content)
                price = item.select_one(
                    'span[data-test="property-card-price"]').text.strip()
                test = item.select('ul li')
                features = " ".join([el.text.strip() for el in test])
                parsed_data = [category, features,
                               address, state, zip_code, price, 'N/A']
                data_list.append(parsed_data)

# Creating a CSV file to store the data
with open('zillow_data.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    # Writing the column names
    writer.writerow(['Category', 'House Features', 'Address',
                    'State', 'Zip code', 'Price', 'Open Time/Posting Time'])
    # Looping through the listings and extracting the data
    for data_item in data_list:
        # Writing the data to the CSV file
        writer.writerow(data_item)
