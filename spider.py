import re
import fnmatch
import os
import requests
from requests.exceptions import HTTPError
from bs4 import BeautifulSoup

def get_html_paths():
    paths = {}
    for root, dirnames, filenames in os.walk('.'):
        for filename in fnmatch.filter(filenames, '*.html'):
            path = os.path.join(root, filename)
            paths[path] = path
    return paths

def update_anchor_links_in_html(soup, dir_path):
    for anchor in soup.findAll('a'):
        link = anchor.get('href')
        new_link = get_updated_link(link, dir_path, 0)
        if new_link == "":
            print(f'FAIL: {link}')
        else:
            anchor['href'] = new_link

def update_image_links_in_html(soup, dir_path):
    for image in soup.findAll('img'):
        link = image.get('src')
        new_link = get_updated_link(link, dir_path, 0)
        if new_link == "":
            print(f'FAIL: {link}')
        else:
            image['src'] = new_link

def get_updated_link(link, dir_path, attempt):
    if attempt != 0:
        link = "https://smtc-website.s3.us-east-2.amazonaws.com/" + dir_path + "/" + link

    try:
        response = requests.get(link)
    except Exception as err:
        if attempt == 0:
            return get_updated_link(link, dir_path, attempt + 1)
        else:
            return ""
    else:
        if response.status_code == 200:
            return link
        else:
            if attempt == 0:
                return get_updated_link(link, dir_path, attempt + 1)
            else:
                return ""

paths = get_html_paths()

chosen_path = paths["./Brooks(Abner)Cem/Brooks(Abner)CemList.html"]
rel_path_full = os.path.relpath(chosen_path)
dir_path = rel_path_full[:rel_path_full.rindex("/")]

print("updating links for " + chosen_path)
soup = BeautifulSoup(open(chosen_path), "html5lib")
update_anchor_links_in_html(soup, dir_path)
update_image_links_in_html(soup, dir_path)

with open(chosen_path, "w") as file:
    file.write(str(soup))
