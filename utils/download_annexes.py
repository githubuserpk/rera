import requests
from bs4 import BeautifulSoup
import os
import time
import re
import textwrap

os.makedirs('annexes', exist_ok=True)


def clean_text(text):
    # Remove extra spaces between words
    cleaned = re.sub(r'\s+', ' ', text)
    # Remove spaces before punctuation
    cleaned = re.sub(r'\s+([.,!?:;])', r'\1', cleaned)
    # Join hyphenated words that were split across lines
    cleaned = re.sub(r'(\w+)-\s*\n\s*(\w+)', r'\1\2', cleaned)
    # Remove any remaining newlines
    cleaned = cleaned.replace('\n', ' ')
    return cleaned.strip()



def scrape_annex(annex_number):
    url = f"https://artificialintelligenceact.eu/annex/{annex_number}/"
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'lxml')
        
        content_div = soup.find('div', class_='et_pb_module et_pb_post_content et_pb_post_content_0_tb_body')
        if content_div:
            annex_text = content_div.get_text(separator='\n', strip=True)
        else:
            print(f"Annex text not found for annex {annex_number}. Skipping...")
            return

        curated_text = clean_text(annex_text)
        wrapped_text = textwrap.fill(curated_text, width=80) 

        combined_text = f"Annex {annex_number} Text:\n{wrapped_text}\n"

        suitable_recitals_div = soup.find('div', class_='aia-explorer-related')
        if suitable_recitals_div:
            combined_text += "\nSuitable Recitals:\n"
            for link in suitable_recitals_div.find_all('a'):
                recital_number = link.get_text(strip=True)
                recital_url = link.get('href')
                combined_text += f"{recital_number}: {recital_url}\n"
        else:
            combined_text += "\nNo suitable recitals found.\n"

        file_path = f"annexes/annex_{annex_number}.txt"


        with open(file_path, "w", encoding="utf-8") as file:
            file.write(combined_text)
        
        print(f"Downloaded plain text of annex {annex_number} successfully.")

    except requests.exceptions.RequestException as e:
        print(f"Failed to download annex {annex_number}: {e}")
    except Exception as e:
        print(f"An error occurred for annex {annex_number}: {e}")

for i in range(1, 14):
    scrape_annex(i)
    time.sleep(5)