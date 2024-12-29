import json

import browser_cookie3
from urllib.parse import unquote
from boosty.api.auth.resolvers.file import FileAuthDataResolver


def get_boosty_cookies():
    """
    Extracts cookies for 'boosty.to' from the Chrome browser.

    Returns:
        dict: A dictionary of cookie names and their corresponding values.
    """
    # Extract cookies for 'boosty.to' from Chrome
    cj = browser_cookie3.chrome(domain_name="boosty.to")

    # Convert cookies to a dictionary
    cookies = {}
    for cookie in cj:
        cookies[cookie.name] = cookie.value
    return cookies


def main():
    boosty_cookies = get_boosty_cookies()
    for name, value in boosty_cookies.items():
        print(f"{name}: {value}")

    auth_resolver = FileAuthDataResolver(auth_file="auth.json")
    auth_cookies = {
        cookie_name: unquote(boosty_cookies[cookie_name])
        for cookie_name in boosty_cookies
        if cookie_name in ["auth", "_clientId"]
    }
    auth_data = auth_resolver.load_auth_data()
    # TODO just return if fresh

    auth_resolver.auth_data.from_cookies_data(json.loads(auth_cookies["auth"]))
    auth_resolver.auth_data.device_id = auth_cookies.get("_clientId")
    # auth_resolver.auth_data.user_agent = browser_cookie3.
    auth_resolver.save_auth_data()
    print("Completed saving Boosty cookies to auth.json")



# Example usage
if __name__ == "__main__":
    main()
