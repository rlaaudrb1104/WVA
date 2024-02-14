import requests

def check_security_headers(url):
    headers_to_check = [
        'Content-Security-Policy',
        'X-Frame-Options',
        'Strict-Transport-Security',
        'Referrer-Policy',
        'X-Content-Type-Options',
        'Permissions-Policy'
    ]

    try:
        response = requests.head(url)
        security_headers = response.headers

        print("Security Headers for", url)
        for header in headers_to_check:
            if header in security_headers:
                print(header + ":", security_headers[header])
            else:
                print(header + ": Header not found")
    except requests.exceptions.RequestException as e:
        print("Error occurred while fetching the headers:", e)

# Example usage:
url = "https://www.naver.com/"  # Replace with the URL you want to check
check_security_headers(url)