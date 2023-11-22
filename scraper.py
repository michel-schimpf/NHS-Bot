import os
import requests
from bs4 import BeautifulSoup
import time
import json

def scrape_nhs(url):
    response = requests.get(url)
    if response.status_code != 200:
        return "Failed to retrieve the webpage"

    soup = BeautifulSoup(response.content, 'html.parser')
    items = []
    for li in soup.find_all('li'):
        a_tag = li.find('a', href=True)
        if a_tag:
            item_name = a_tag.get_text(strip=True)
            item_link = a_tag['href']
            items.append((item_name, item_link))
 
    # Filtere stuff
    if '/conditions/' in url:
        # Identifiziere und entferne die ersten Elemente, falls notwendig
        if ('Z', '/conditions/#Z') in items:
            target_index = items.index(('Z', '/conditions/#Z'))
            items = items[target_index + 1:]
         # Identifiziere und entferne die letzten Elemente, falls notwendig
        if ('Home', '/') in items:
            target_index = items.index(('Home', '/'))
            items = items[:target_index]
        items = [item for item in items if '/conditions/' in item[1]]
    elif '/medicines/' in url:
        # Identifiziere und entferne die ersten Elemente, falls notwendig
        if ('Z', '/medicines/#Z') in items:
            target_index = items.index(('Z', '/medicines/#Z'))
            items = items[target_index + 1:]
         # Identifiziere und entferne die letzten Elemente, falls notwendig
        if ('Home', '/') in items:
            target_index = items.index(('Home', '/'))
            items = items[:target_index]
        items = [item for item in items if '/medicines/' in item[1]]

    return items

from concurrent.futures import ThreadPoolExecutor
import concurrent

def scrape_section(url):
    # time.sleep(0.1)
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to retrieve the webpage for {url}")
        return None

    soup = BeautifulSoup(response.content, 'html.parser')
    article_tag = soup.find('article')
    if not article_tag:
        print(f"No article found for {url}")
        return None

    sections = article_tag.find_all('section')
    section_texts = [section.get_text(separator='\n', strip=True) for section in sections]
    return section_texts

def fetch_nhs_content(limit=-1):
    conditions = scrape_nhs("https://www.nhs.uk/conditions/")[0:limit]
    # medicines = scrape_nhs("https://www.nhs.uk/medicines/")[0:limit]
    all_items = conditions 
    # all_items.extend(medicines)
    nhs_contents = []
    base_url = "https://www.nhs.uk"

    for name, partial_url in all_items:
        full_url = base_url + partial_url
        section_text = scrape_section(full_url)
        if section_text:
            nhs_contents.append({"name": name, "url": full_url, "content": section_text})

    return nhs_contents



# def store_content_in_files(nhs_content):
#     output_folder = "condition_text_files"
#     if not os.path.exists(output_folder):
#         os.makedirs(output_folder)

#     for condition_name, sections in nhs_content.items():
#         condition_name = condition_name.replace('/', '_')
#         file_path = os.path.join(output_folder, f"{condition_name}.txt")
#         with open(file_path, 'w', encoding='utf-8') as file:
#             for section in sections:
#                 file.write(section + "\n\n")

def store_content_in_json(nhs_contents):
    output_file = "nhs_data.json"
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(nhs_contents, file, ensure_ascii=False, indent=4)

nhs_content = fetch_nhs_content()
store_content_in_json(nhs_content)
# for nh in nhs_content[:3]:
#     print(nh)