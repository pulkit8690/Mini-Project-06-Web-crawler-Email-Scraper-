
# Install following pacakges
# !pip install requests-html
# !pip install re
# !pip install request
# !pip install bs4

import re
import pandas as pd
import requests
from bs4 import BeautifulSoup
from collections import deque
from urllib.parse import urlsplit
import pandas as pd
from requests_html import HTMLSession
import threading
import time
from tqdm import tqdm 
#user_url = "https://www.thapar.edu/sitemap.xml"
#url = ["https://www.thapar.edu"]
EMAIL_REGEX = r"""(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"""
def get_urls_of_xml(xml_url):
    r = requests.get(xml_url)
    xml = r.text
    soup = BeautifulSoup(xml)

    links_arr = []
    for link in soup.findAll('loc'):
        linkstr = link.getText('', True)
        links_arr.append(linkstr)

    return links_arr



links_data_arr = get_urls_of_xml("https://thapar.edu/sitemap.xml")
#print(links_data_arr)
session = HTMLSession()
email=set()
for i in tqdm(links_data_arr):
        #requests.get(f'{i}', verify=False)
        r = session.get(i)
        for re_match in re.finditer(EMAIL_REGEX, r.html.raw_html.decode()):
            email.add(((re_match.group())).replace("-",""))
df = pd.DataFrame(email) 
df.to_csv('Emails.csv', index=False)