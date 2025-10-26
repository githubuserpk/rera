import requests
from bs4 import BeautifulSoup
import os
import time
import re
import textwrap



def merge_files(folder_path):
    """
    Merges all .txt files in the specified folder and returns the combined content.
    
    Parameters:
        folder_path (str): The path to the folder containing the text files.
    
    Returns:
        str: The combined content of all text files in the folder.
    """
    merged_content = []
    
    # Iterate through all files in the folder
    for file_name in sorted(os.listdir(folder_path)):  # Sort to ensure order (e.g., recital_1, recital_2)
        if file_name.endswith(".txt"):  # Only process .txt files
            file_path = os.path.join(folder_path, file_name)
            with open(file_path, "r", encoding="utf-8") as file:
                file_content = file.read()
                merged_content.append(file_content)  # Add the content to the list
    
    # Join all contents into a single string with a separator (optional)
    return "\n\n".join(merged_content)


# Subject Area 2 Annexes
folder = "annexes_test"  # Folder containing recital text files
annexes_text = merge_files(folder)

print(annexes_text)
