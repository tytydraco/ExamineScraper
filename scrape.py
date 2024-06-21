import requests
from bs4 import BeautifulSoup
from requests_html import HTMLSession

import re
from markdownify import markdownify

excluded_classes = ['optin-wrapper', 'expand-items', 'th-module-head']

base_url = 'https://examine.com'
full_list = f'{base_url}/supplements'

session = HTMLSession()
full_list_html = session.get(full_list)
full_list_html.html.render(wait=2, sleep=2)
full_list_soup = BeautifulSoup(full_list_html.html.html, 'html.parser')

all_supps = full_list_soup.find(id='all-supplements')
all_supplement_links = all_supps.findAll('a', href=True)
print(f'HREFs: {len(all_supplement_links)}')

for supp_a in all_supplement_links:
    href = supp_a['href']
    href_match = re.match(r'/supplements/(.*)/', href)

    if href_match is None:
        continue

    name = href_match.group(1)
    url = f'{base_url}{href}/research'

    print(f'Parsing {name}...')

    supp_content_html = requests.get(url)
    supp_content_soup = BeautifulSoup(supp_content_html.content, 'html.parser')
    research_breakdown = supp_content_soup.find(class_='w-screen')
    research_breakdown.find('form').decompose()
    content = markdownify(str(research_breakdown), convert=['p'])

    with open(f'supplements/{name}.md', 'w') as f:
        f.write(content)
