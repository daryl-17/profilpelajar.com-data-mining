import requests
from bs4 import BeautifulSoup

base_url = 'https://profilpelajar.com/perguruan/tinggi/'

# Create a file to save the links
file_name = 'links.txt'
file = open(file_name, 'w')

    # Send a GET request to the URL and retrieve the HTML content
response = requests.get(base_url)
html_content = response.text

    # Create a BeautifulSoup object with the HTML content
soup = BeautifulSoup(html_content, 'html.parser')

    # Find the table with the specified class
table = soup.find('table', {'class': 'table table-striped table-sm'})

    # Find all <a> tags within the table
a_tags = table.find_all('a')
        
    # Extract the links from the 'href' attribute of each <a> tag
links = [a['href'] for a in a_tags]

    # Write the extracted links to the file
for link in links:
        file.write(link + '\n')


# Replace the target_link variable with the link you want to find   
file.close()
