import requests

def is_valid_directory(url):
    try:
        response = requests.get(url)
        response_url = response.url
        
        if response.status_code == 200 and response_url == url:  
            return True
        else:
            return False
    except requests.exceptions.RequestException:
        return False

def directory_listing(url, cheatsheet_path):
    directory_found_list = []

    try:
        with open(cheatsheet_path, "r", encoding="utf-8") as directory_cheatsheet:
            directory_index = directory_cheatsheet.read().split("\n")
            
            for directory in directory_index:
                directory_url = f"{url}{directory}"
                if is_valid_directory(directory_url):
                    directory_found_list.append(directory_url)
    
    except FileNotFoundError:
        print(f"Error: File '{cheatsheet_path}' not found.")
    
    if directory_found_list:
        return directory_found_list
    else:
        return ["Directory not found"]