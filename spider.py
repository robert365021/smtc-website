import csv
import re
import fnmatch
import os
import requests
from requests.exceptions import HTTPError
from bs4 import BeautifulSoup

def get_html_paths():
    paths = {}
    for root, dirnames, filenames in os.walk('./Akers-BrownCemetery'):
        for filename in fnmatch.filter(filenames, '*.html'):
            path = os.path.join(root, filename)
            paths[path] = path
    return paths

def attempt_update_link(link):
    if os.path.basename(link).lower().endswith(".html"):
        return "-1"
    else:
        return get_updated_link(link, dir_path, 0)

def update_anchor_links_in_html(soup, dir_path, full_path):
    for anchor in soup.findAll('a'):
        link = anchor.get('href')
        new_link = attempt_update_link(link)
        if new_link == "-1":
            anchor['href'] = link
        elif new_link == "":
            with open('fix.csv', 'a') as csvfile:
                csvwriter = csv.writer(csvfile)
                csvwriter.writerow([full_path, link])
        else:
            anchor['href'] = new_link

def update_image_links_in_html(soup, dir_path, full_path):
    for image in soup.findAll('img'):
        link = image.get('src')
        new_link = attempt_update_link(link)
        if new_link == "-1":
            image['src'] = link
        elif new_link == "":
            with open('fix.csv', 'a') as csvfile:
                csvwriter = csv.writer(csvfile)
                csvwriter.writerow([full_path, link])
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

fail_fields = ['source_file', 'suspicious_link']
with open('fix.csv', 'w') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(fail_fields)

paths = get_html_paths()

for path in paths:
    rel_path_full = os.path.relpath(path)

    if "Giles-Marshall-LincolnCountyCemWeb/" in rel_path_full:
        rel_path_full = rel_path_full.replace("Giles-Marshall-LincolnCountyCemWeb/", "Giles-Marshall-LincolnCountyCemWebImages/")

    if "AlabamaCemeteriesWeb/" in rel_path_full:
        rel_path_full = rel_path_full.replace("AlabamaCemeteriesWeb/", "AlabamaCemeteriesImages/")

    try:
        slash_index = rel_path_full.rindex("/")
        dir_path = rel_path_full[:slash_index]
    except:
        dir_path = rel_path_full

    print("updating " + dir_path + " links for " + path)
    soup = BeautifulSoup(open(path), "html5lib")
    update_anchor_links_in_html(soup, dir_path, path)
    update_image_links_in_html(soup, dir_path, path)

    with open(path, "w") as file:
        file.write(str(soup))
