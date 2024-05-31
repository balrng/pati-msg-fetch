import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET

# URLs
# Don't change these URLs
messenger_url = "https://forum.paticik.com/messenger/"
login_url = "https://forum.paticik.com/login/"


# Change this with your profile content URL
profile_url = "https://forum.paticik.com/profile/4428-Dark_Soul/content/"

# Should be min. of 1
# Enter the max number of pages you want to extract on your profile content page
content_total_page_number = 1

# User credentials
credentials = {
    'login': 'your_username',
    'password': 'your_password'
}

# Create a session to persist cookies
with requests.Session() as session:
    # Get the login page to retrieve any necessary cookies or tokens
    response = session.get(login_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the CSRF token if needed
    csrf_token = soup.find('input', {'name': 'csrfKey'}).get('value')

    # Additional form dataP
    form_data = {
        'csrfKey': csrf_token,
        'auth': credentials['login'],
        'password': credentials['password'],
        'remember_me': '1',
        '_processLogin': 'usernamepassword',
        'signin': 'Giriş Yap'
    }

    # Headers for the login request
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://forum.paticik.com',
        'Referer': login_url
    }

    # Post the login credentials to login
    login_response = session.post(login_url, data=form_data, headers=headers)

    # Debugging: Print the login response content
    print("Login Response URL:", login_response.url)
    print("Login Response Status Code:", login_response.status_code)
    print("Login Response Headers:", login_response.headers)
    print("Login Response Text:", login_response.text[:1000])  # Print first 1000 characters

    # Check if login was successful by inspecting the messenger page content
    messenger_response = session.get(messenger_url)
    messenger_soup = BeautifulSoup(messenger_response.content, 'html.parser')
    error_message = messenger_soup.find('div', id='elErrorMessage')

    if error_message is None:
        print("Login successful!")

        # Create XML structure
        root = ET.Element('ForumMessages')

        # Loop through all pages
        for i in range(content_total_page_number):
            response = session.get(profile_url)
            if i > 0:
                profile_url_paginated = f"https://forum.paticik.com/profile/4428-Dark_Soul/content/page/{i+1}/"
                response = session.get(profile_url_paginated)

            if response.status_code == 200:
                # Parse the response content with BeautifulSoup
                soup = BeautifulSoup(response.content, 'html.parser')

                # Find all the message containers
                messages = soup.find_all('li', class_='ipsStreamItem')

                for message in messages:
                    title_element = message.find('h2', class_='ipsStreamItem_title')
                    date_element = message.find('time')
                    content_element = message.find('div', class_='ipsStreamItem_snippet')

                    # Check if all elements are found
                    if title_element and date_element and content_element:
                        title = title_element.text.strip()
                        date = date_element['datetime'].split('T')[0]  # Extracting date in YYYY-MM-DD format
                        content = content_element.text.strip()

                        # Create XML entry
                        entry = ET.SubElement(root, 'Entry')
                        title_xml = ET.SubElement(entry, 'Title')
                        title_xml.text = title
                        date_xml = ET.SubElement(entry, 'Date')
                        date_xml.text = date
                        content_xml = ET.SubElement(entry, 'Content')
                        content_xml.text = content

            else:
                print("Failed to retrieve the profile content page. Status code:", response.status_code)

        # Write to a file
        tree = ET.ElementTree(root)
        tree.write("forum_messages_extracted.xml", encoding='utf-8', xml_declaration=True)

    else:
        print("Login failed: 'Ulaşmak istediğiniz sayfa misafirlere görünmüyor' message found.")
