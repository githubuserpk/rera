import requests
from bs4 import BeautifulSoup
import time
import os
import argparse

# Create the recitals directory if it doesn't exist
os.makedirs('recitals', exist_ok=True)

# Set up command-line argument parsing
parser = argparse.ArgumentParser(description='Download recitals from the EU AI Act website.')
parser.add_argument('start', type=int, help='Starting recital number')
parser.add_argument('end', type=int, help='Ending recital number')

args = parser.parse_args()

# Loop through the specified range of recitals
for i in range(args.start, args.end + 1):
    url = f"https://artificialintelligenceact.eu/recital/{i}/"  # Construct the URL for each recital


    try:
        # Send a GET request to fetch the recital page
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, 'lxml')
        
        # Extract the recital text from the specified div
        recital_div = soup.find('div', class_='et_pb_module et_pb_post_content et_pb_post_content_0_tb_body')
        if recital_div:
            recital_text = recital_div.get_text(separator='\n', strip=True)
        else:
            print(f"Recital text not found for recital {i}. Skipping...")
            continue

        # Extract related articles from the specified div
        related_div = soup.find('div', class_='aia-explorer-related')
        related_articles = []
        if related_div:
            # Find all anchor tags within this div and extract their href and text
            for link in related_div.find_all('a'):
                href = link.get('href')  # Get the href attribute
                text = link.get_text(strip=True)  # Get the link text
                related_articles.append((text, href))  # Store as a tuple (text, href)

        # Combine recital text and related articles (if any) into a formatted string
        combined_text = f"Recital {i} Text:\n{recital_text}\n"
        if related_articles:
            combined_text += "\nRelated Articles:\n"
            for article in related_articles:
                combined_text += f"{article[0]}: {article[1]}\n"
        else:
            combined_text += "\nNo related articles found.\n"

        # Save the plain text to a text file in the recitals folder
        with open(f"recitals/recital_{i}.txt", "w", encoding="utf-8") as file:
            file.write(combined_text)
        
        print(f"Downloaded plain text of recital {i} successfully.")

    except requests.exceptions.RequestException as e:
        print(f"Failed to download recital {i}: {e}")
    except Exception as e:
        print(f"An error occurred for recital {i}: {e}")

    # Wait for 1 minute before fetching the next recital
    if i < args.end:  # Avoid waiting after the last download
        time.sleep(30)  # Sleep for 30 seconds (1 minute)




