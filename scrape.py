import requests
from bs4 import BeautifulSoup

import re
from markdownify import markdownify

excluded_classes = ['optin-wrapper', 'expand-items', 'th-module-head']

base_url = 'https://examine.com'
full_list = f'{base_url}/supplements'
full_list_html = requests.get(full_list)
full_list_soup = BeautifulSoup(full_list_html.content, "html.parser")
all_supps = full_list_soup.find(class_='spi-2-all-supplements')

supplements = {}
for supp_a in all_supps.findAll('a', href=True):
    href = supp_a['href']
    name = re.match(r'/supplements/(.*)/', href).group(1)
    url = f'{base_url}{href}'

    if name in supplements:
        continue

    print(f'Parsing {name}...')
    supplements[name] = True
    
    supp_content_html = requests.get(f'{url}/research')
    supp_content_soup = BeautifulSoup(supp_content_html.content, "html.parser")

    content = ""
    for i in supp_content_soup.findAll(id='scientific-research'):
        for c in excluded_classes:
            e = i.find(class_=c)
            if e is not None:
                e.extract()
        content += markdownify(str(i))

    with open(f'supplements/{name}.md', 'w') as f:
        f.write(content)