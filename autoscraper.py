import requests
import lxml # not working
import csv
import argparse
import sys

from bs4 import BeautifulSoup
import sys

arg1 = sys.argv[1]
print(arg1)

'''
parser = argparse.ArgumentParser(description='Process string to be searched.')
parser.add_argument("honda element", help='add string to the search', type=str)
args = parser.parse_args()
'''

search_sites = {
    'New Brunswick': f'https://www.kijiji.ca/b-new-brunswick/{arg1}/k0l9005?rb=true&dc=true',
    'Nova Scotia' : f'https://www.kijiji.ca/b-nova-scotia/{arg1}/k0l9002?rb=true&dc=true',
    'PEI' : f'https://www.kijiji.ca/b-prince-edward-island/{arg1}/k0l9011?rb=true&dc=true',
    'Quebec': f'https://www.kijiji.ca/b-quebec/{arg1}/k0l9001?rb=true&dc=true'
    }

search_list = []
search_items = {}

for k, v in search_sites.items():

    print(f'{k} search results:')
    response = requests.get(v).text
    soup = BeautifulSoup(response, features='html.parser')
    search_results = soup.select('div.search-item.regular-ad')

    for search_item in search_results: 
        try:
            date_posted = search_item.find('span', class_="date-posted").text 
            title_ad = search_item.find('a', attrs={"class":"title"}).text.strip(' \n')
            price = search_item.find('div',attrs={"class":"price"}).text.strip(' \n')
            description = search_item.find('div', attrs={"class":"description"}).text.strip(' \n')[:100]
            ad_link = search_item.select_one('a.title')
            
            search_items = {
                "date_posted": date_posted,
                "title_ad": title_ad,
                "price": price,
                "description": description,
                "ad_link": f"https://www.kijiji.ca{ad_link['href']}"
                }

            search_list.append(search_items)

            #terminal out for testing
            print(f'''
            Date Posted: {date_posted}
            Ad title: {title_ad}
            Price: {price}
            Description: {description}
            Link: https://www.kijiji.ca{ad_link["href"]}
            ''')
            print('*' * 100)
        except AttributeError:
            continue
    print(f'Total {k} results:', len(search_list))   


with open(f"{arg1}.csv", 'w') as csv_file:
    fieldnames = ['date_posted', 'title_ad','price', 'description', 'ad_link']

    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    csv_writer.writeheader()

    for i in range(len(search_list)):
        write_to_row = {
            'date_posted':f'{search_list[i]["date_posted"]}',
            'title_ad': f'{search_list[i]["title_ad"]}', 
            'price': f'{search_list[i]["price"]}', 
            'description': f'{search_list[i]["description"]}', 
            'ad_link': f'{search_list[i]["ad_link"]}', 
            }
        csv_writer.writerow(write_to_row)
