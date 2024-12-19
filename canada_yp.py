import requests
from bs4 import BeautifulSoup

page = requests.get('https://www.canadayp.ca/')
soup = BeautifulSoup(page.text, 'html.parser')
ids = soup.find(id='bd-chained')
ids = ids.find_all('option')
ids = [[x['value'], x.contents[0]] for x in ids if x.contents]

all_links = []
for i in ids:
    #scroll through all pages
    page = requests.get('https://www.canadayp.ca/search_results?tid={}'.format(i[0]))
    soup = BeautifulSoup(page.text, 'html.parser')
    links = soup.find_all('a', {'class':'btn btn-success btn-block'})
    links = ['https://www.canadayp.ca' + x['href'] for x in links]
    all_links.append(links)

    break