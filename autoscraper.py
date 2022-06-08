import requests
from bs4 import BeautifulSoup
import csv

URL_NB = 'https://www.kijiji.ca/b-new-brunswick/honda-element/k0l9005?rb=true&dc=true'
URL_NS = 'https://www.kijiji.ca/b-nova-scotia/honda-element/k0l9002?rb=true&dc=true'
honda_list = []
honda_truck = {}
response = requests.get(URL_NS).text
soup = BeautifulSoup(response, 'lxml')
search_results = soup.select('div.search-item.regular-ad')

for truck in search_results: 
    try:
        date_posted = truck.find('span', class_="date-posted").text 
        title_ad = truck.find('a', attrs={"class":"title"}).text.strip(' \n')
        price = truck.find('div',attrs={"class":"price"}).text.strip(' \n')
        description = truck.find('div', attrs={"class":"description"}).text.strip(' \n')[:100]
        ad_link = truck.select_one('a.title')
        
        honda_truck = {
            "date_posted": date_posted,
            "title_ad": title_ad,
            "price": price,
            "description": description,
            "ad_link": f"https://www.kijiji.ca{ad_link['href']}",
            }

        honda_list.append(honda_truck)

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
print(len(honda_list))   


with open("honda_element.csv", 'w') as csv_file:
    fieldnames = ['date_posted', 'title_ad','price', 'description', 'ad_link']

    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    csv_writer.writeheader()

    for i in range(len(honda_list)):
        write_to_row = {
            'date_posted':f'{honda_list[i]["date_posted"]}',
            'title_ad': f'{honda_list[i]["title_ad"]}', 
            'price': f'{honda_list[i]["price"]}', 
            'description': f'{honda_list[i]["description"]}', 
            'ad_link': f'{honda_list[i]["ad_link"]}', 
            }
        csv_writer.writerow(write_to_row)

