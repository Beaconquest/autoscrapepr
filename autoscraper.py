import requests
import csv
from bs4 import BeautifulSoup


URL_NB = 'https://www.kijiji.ca/b-new-brunswick/honda-element/k0l9005?rb=true&dc=true'
URL_NS = 'https://www.kijiji.ca/b-nova-scotia/honda-element/k0l9002?rb=true&dc=true'

class AutoSearch:
    """Searches kijiji for auto sales and posts to a file."""

    def __init__(self, url):
        self.__url = url

    def get_honda_element_soup(self):
        response = requests.get(self.__url, headers={'user-agent': 'webscrapper.py'}, allow_redirects=False)
        soup = BeautifulSoup(response.text, 'lxml')
        search_results = soup.find_all('div', class__:"search-item regular-ad"})
        print(type(search_results))
        print(len(search_results))

        for i in search_results:

            print(i)    
            title_ad = i.find('a', attrs={"class":"title"})
            print(title_ad.text.strip(" \n"))
            price = search_results.find('div',attrs={"class":"price"})
            print(price.text.strip(' \n'))
            description = search_results.find('div', attrs={"class":"description"})
            print(description.text.strip(' \n')[:100])
            print('*' * 100)
        
        #listing_id = soup.find_all('div', 'data-listing-id')
        
        
    def get_search_list(self, soup_results):
        honda_list = []
        
        # listing_id = search_results.find('div', 'data-listing-id')
        print(listing_id)
        honda_list.append(listing_id)

        return honda_list

    def save_honda_results(self, honda_list):
        ''' Writes to a csv file '''
        row = honda_list
        with open("honda_element.csv", 'w') as csv_file:
            fieldnames = ['listing_id', 'date_posted','title', 'location', 'price', 'description', 'ad_link']
            
            csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            csv_writer.writeheader()

            for i in range(len(row)):
                write_to_row = {
                    'Company': f'{row[i]["companyName"]}', 
                    'Street': f'{row[i]["address1"]}', 
                    'City': f'{row[i]["city"]}', 
                    'St': f'{row[i]["state"]}', 
                    'ZIPCode': f'{row[i]["zip"]}', 
                    'AddressStatus': f'{row[i]["addressStatus"]}'}

                csv_writer.writerow(write_to_row)

    def __repr__(self):
        return f"AutoSearch({self.__url})"

if __name__ == "__main__":
    honda_NS = AutoSearch(URL_NS)
    honda_soup = honda_NS.get_honda_element_soup()
    print(honda_soup)
    