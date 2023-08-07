import asyncio
import csv
import re
import httpx
from bs4 import BeautifulSoup
import aiofiles

async def extract_details(url):
    async with httpx.AsyncClient(timeout=httpx.Timeout(timeout=60.0)) as client:
        try:
            response = await client.get(url)
        except httpx.Timeout as e:
            print(f"Timeout occurred for {url}. Retrying...")
            try:
                response = await client.get(url)
            except httpx.Timeout:
                print(f"Timeout occurred for {url} again. Skipping...")
                return [None, None, None, None, None]
            except httpx.TransportError as e:
                print(f"TransportError occurred for {url}: {e}")
                return [None, None, None, None, None]
        except httpx.TransportError as e:
            print(f"TransportError occurred for {url}: {e}")
            return [None, None, None, None, None]

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

async def process_link(url):
    province_name = re.search(r'Prov-([A-Za-z-]+)', url).group(1).lower()
    output_file = f'{province_name}.csv'

    result = await extract_details(url)

    if any(field is not None for field in result):
        async with aiofiles.open(output_file, 'a', newline='') as f:
            writer = csv.writer(f)
            if f.tell() == 0:
                await writer.writerow(['perguruan tinggi', 'email', 'alamat', 'telepon', 'website'])
            await writer.writerow(result)

        print(f'Data extracted and saved to {output_file}.')

async def main():
    base_url = 'https://profilpelajar.com/perguruan/tinggi/Prov-Sumatera-Utara/e24347877eb7802328bf85875bcf553ac2379c74'
    max_retries = 10
    retry_count = 0

    while retry_count < max_retries:
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(base_url)
                break  # Success, break out of the retry loop
            except httpx.TransportError as e:
                retry_count += 1
                print(f"TransportError occurred for base URL. Retry {retry_count}/{max_retries}.")
                await asyncio.sleep(1)  # Introduce a delay before the next retry

        if retry_count == max_retries:
            print(f"Max retries reached. Exiting.")
            return

    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')
    table = soup.find('table', {'class': 'table table-striped table-sm'})
    a_tags = table.find_all('a')

    urls = [a.get('href') for a in a_tags]

    await asyncio.gather(*[process_link(url) for url in urls])

if __name__ == "__main__":
    asyncio.run(main())
