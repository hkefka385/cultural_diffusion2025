import pandas as pd
import numpy as np
from urllib.parse import urlencode
import requests
import pickle
import time

# Load initial data: assign to the P
def load_data(filepath):
    with open(filepath, mode='rb') as f:
        return pickle.load(f)

# Filter data by year
def filter_data_by_year(data, year=2000):
    filtered_data = []
    for item in data:
        if 'P571' in item[1]['claims']:
            try:
                year_value = int(item[1]['claims']['P571'][0]['mainsnak']['datavalue']['value']['time'][1:5])
                if year_value > year:
                    filtered_data.append(item)
            except:
                continue
    return filtered_data

# Fetch Wikipedia revisions
def fetch_revisions(title, lang_code, retries=5):
    params = {
        'action': 'query',
        'prop': 'revisions',
        'rvprop': 'ids|flags|timestamp|user|userid|comment|content|size|slotsize|tags|roles|contentmodel',
        'titles': title,
        'rvdir': 'newer',
        'formatversion': 2,
        'format': 'json',
        'rvlimit': 500,
    }
    revisions = []
    for attempt in range(retries):
        try:
            url = f"https://{lang_code}.wikipedia.org/w/api.php?{urlencode(params)}"
            response = requests.get(url, timeout=10).json()
            if 'pages' in response.get('query', {}):
                revisions.extend(response['query']['pages'])
            if 'batchcomplete' in response:
                break
            params['rvcontinue'] = response['continue']['rvcontinue']
        except Exception as e:
            time.sleep(2 ** attempt)
        else:
            break
    return revisions

# Process data
def process_data(data, lang_codes, output_dir):
    all_content = {}
    counter = 1
    for i, item in enumerate(data):
        if i % 2000 == 0 and i > 0:
            save_data(all_content, output_dir, counter)
            all_content = {}
            counter += 1

        labels = item[1]['labels']
        save_data = {}
        for lang, value in labels.items():
            if lang in lang_codes:
                save_data[lang] = fetch_revisions(value['value'], lang)
        all_content[item[1]['id']] = [item, save_data]
    save_data(all_content, output_dir, counter)

# Save data to a file
def save_data(data, output_dir, file_index):
    filepath = f"{output_dir}/art_edit_{file_index}.pickle"
    with open(filepath, mode='wb') as f:
        pickle.dump(data, f)

# Main function
def main():
    # Filepaths and parameters
    input_filepath = 'data_raw/wikipedia_art.pickle'
    output_dir = 'edit_wikipedia'
    lang_codes = ['en', 'fr', 'de', 'es', 'ja', 'ru', 'pt', 'zh', 'it', 'fa', 'ar', 'pl', 'uk', 
                  'nl', 'tr', 'he', 'id', 'cs', 'vi', 'fi', 'ko', 'hu', 'hi', 'simple', 'ca', 
                  'el', 'th', 'no', 'ro', 'bn', 'sr']

    # Workflow
    data = load_data(input_filepath)
    filtered_data = filter_data_by_year(data, year=2000)
    process_data(filtered_data, lang_codes, output_dir)

if __name__ == "__main__":
    main()