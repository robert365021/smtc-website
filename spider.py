import csv
import re
import fnmatch
import os
import requests
from requests.exceptions import HTTPError
from bs4 import BeautifulSoup
from datetime import datetime

visited_file_name = ".visited"
fix_file_name = "fix-" + datetime.now().strftime("%Y-%m-%d-%H-%M") + ".csv"
fix_fields = ['source_file', 'img_link', 'suspicious_link']

def get_html_paths():
    visited_paths = {}

    with open(visited_file_name) as f:
        content = f.readlines()
    content = [x.strip() for x in content]

    for line in content:
        visited_paths[line]= line

    paths = {}

    for root, dirnames, filenames in os.walk('.'):
        for filename in fnmatch.filter(filenames, '*.html'):
            path = os.path.join(root, filename)
            if path not in visited_paths:
                paths[path] = path
    return paths

def attempt_update_link(link):
    if link != None:
        if os.path.basename(link).lower().endswith(".html"):
            return "-1"
        else:
            return get_updated_link(link, dir_path, 0)
    else:
        return "-1"

def update_anchor_links_in_html(soup, dir_path, full_path):
    for anchor in soup.findAll('a'):
        link = anchor.get('href')
        new_link = attempt_update_link(link)
        if new_link == "-1":
            anchor['href'] = link
        elif new_link == "":
            print("link marked for fix")
            with open(fix_file_name, 'a') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fix_fields)
                writer.writerow({'source_file': full_path, 'img_link': 'false', 'suspicious_link': link})
        else:
            print("link updated")
            anchor['href'] = new_link

def update_image_links_in_html(soup, dir_path, full_path):
    for image in soup.findAll('img'):
        link = image.get('src')
        new_link = attempt_update_link(link)
        if new_link == "-1":
            image['src'] = link
        elif new_link == "":
            print("link marked for fix")
            with open(fix_file_name, 'a') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fix_fields)
                writer.writerow({'source_file': full_path, 'img_link': 'true', 'suspicious_link': link})
        else:
            print("link updated")
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

with open(fix_file_name, 'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fix_fields)
    writer.writeheader()

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

    print("START: " + path)

    soup = BeautifulSoup(open(path), "html5lib")
    update_anchor_links_in_html(soup, dir_path, path)
    update_image_links_in_html(soup, dir_path, path)

    with open(path, "w") as file:
        file.write(str(soup))

    with open(visited_file_name, "a") as visited_file:
        visited_file.write(path + "\n")

    print("END: " + path)
