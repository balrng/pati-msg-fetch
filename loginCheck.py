import requests
from bs4 import BeautifulSoup

# Login URL and profile content URL
login_url = "https://forum.paticik.com/login/"
messenger_url = "https://forum.paticik.com/messenger/"

# User credentials
credentials = {
    'login': '',
    'password': ''
}

# Create a session to persist cookies
with requests.Session() as session:
    # Get the login page to retrieve any necessary cookies or tokens
    response = session.get(login_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find the CSRF token if needed
    csrf_token = soup.find('input', {'name': 'csrfKey'}).get('value')
    
    # Additional form data
    form_data = {
        'csrfKey': csrf_token,
        'auth': credentials['login'],
        'password': credentials['password'],
        'remember_me': '1',
        '_processLogin': 'usernamepassword',
         #'signin': 'Giriş Yap'
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
    else:
        print("Login failed: 'Ulaşmak istediğiniz sayfa misafirlere görünmüyor' message found.")
