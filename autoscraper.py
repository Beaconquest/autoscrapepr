import requests
from bs4 import BeautifulSoup


URL_NB = 'https://www.kijiji.ca/b-new-brunswick/honda-element/k0l9005?rb=true&dc=true'
URL_NS = 'https://www.kijiji.ca/b-nova-scotia/honda-element/k0l9002?rb=true&dc=true'

response = requests.get(URL_NS).text
soup = BeautifulSoup(response, 'lxml')
search_results = soup.select('div.search-item.regular-ad')

print(len(search_results))

for truck in search_results: 
    try:
        date_posted = truck.find('span', class_="date-posted").text 
        title_ad = truck.find('a', attrs={"class":"title"}).text.strip(' \n')
        price = truck.find('div',attrs={"class":"price"}).text.strip(' \n')
        description = truck.find('div', attrs={"class":"description"}).text.strip(' \n')[:100]
        ad_link = truck.select_one('a.title')

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

# listing_id = soup.find_all('div', 'data-listing-id')

'''
honda_list = []

row = honda_list
with open("honda_element.csv", 'w') as csv_file:
    fieldnames = ['title', 'price', 'description', 'ad_link']

    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    csv_writer.writeheader()

    for i in range(len(row)):
        write_to_row = {
            'title': f'{row[i]["title"]}', 
            'price': f'{row[i]["price"]}', 
            'description': f'{row[i]["description"]}', 
            'ad_link': f'{row[i]["ad_link"]}', 
            }

    csv_writer.writerow(write_to_row)
'''
