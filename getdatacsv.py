import csv
import requests
from bs4 import BeautifulSoup
import os

def extract_details(url):
    response = requests.get(url)
    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')
    table = soup.find('table', class_='table-striped table-hover')

    if table:
        data = {}
        rows = table.find_all('tr')
        for row in rows:
            cells = row.find_all('td')
            if len(cells) == 3:
                field = cells[0].get_text(strip=True)
                value = cells[2].get_text(strip=True)
                data[field] = value

        perguruan_tinggi = data.get('Perguruan Tinggi', '')
        email = data.get('Email', '')
        alamat = data.get('Alamat', '')
        telepon = data.get('Telepon', '')
        website = data.get('Website', '')

        return [perguruan_tinggi, email, alamat, telepon, website]
    else:
        return [None, None, None, None, None]

def process_link(url, output_file):
    result = extract_details(url)
    print(f'Data extracted for {url}: {result}')  # Print the extracted data for debugging

    with open(output_file, 'a', newline='') as f:
        writer = csv.writer(f)
        if os.stat(output_file).st_size == 0:
            writer.writerow(['perguruan tinggi', 'email', 'alamat', 'telepon', 'website'])
        
        if any(field is not None for field in result):
            writer.writerow(result)
            print(f'Data extracted and saved to {output_file}.')
        else:
            print(f'Skipped {output_file} as no data found.')

def main():
    with open('links.txt', 'r') as file:
        urls = file.readlines()

    for i, url in enumerate(urls, 1):
        url = url.strip()
        province_name = url.split('/')[5]
        output_file = f'{province_name}.csv'
        print(f'Processing {url} and saving to {output_file}')
        process_link(url, output_file)
        print(f'Processed URL {i}/{len(urls)}')

if __name__ == "__main__":
    main()
