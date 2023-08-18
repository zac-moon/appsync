import requests
import socket
def location():
    def get_user_ip():
        try:
            response = requests.get('http://ipinfo.io')
            data = response.json()
            user_ip = data.get('ip', None)
            return user_ip
        except requests.RequestException:
            return None

    def get_location_from_ip(ip_address):
        try:
            response = requests.get(f'http://ipinfo.io/{ip_address}/json')
            data = response.json()
            city = data.get('city', '')
            country = data.get('country', '')
            return city, country
        except requests.RequestException:
            return None, None   

    def format_location(city, country, user_city=None):
        if user_city and city.lower() != user_city.lower():
            return f"near {city}, {country}"
        else:
            return f"{city}, {country}"

    user_ip = get_user_ip()  # Get the user's IP address automatically

    if user_ip:
        user_city = get_location_from_ip(user_ip)[0]

        if user_city:
            location = get_location_from_ip(user_ip)
            city, country = location
            formatted_location = format_location(city, country, user_city)
            return formatted_location
        else:
            return ("Location information not found.")
    else:
        return ("User IP address not found.")