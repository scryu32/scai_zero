#검색엔진 GOOGLE_SEARCH
import os
import requests

api_key = os.environ.get('GOOGLE_SEARCH')
cx = "6721e7368bb034897"

def search_google(query):
    url = f"https://www.googleapis.com/customsearch/v1"
    params = {
        "key": api_key,
        "cx": cx,
        "q": query,
    }
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        print("Error:", response.status_code)
        return None

def getSearch(search_param):
    results = search_google(search_param)
    items = """"""
    if results:
        for item in results.get("items", []):
            items += f""" "Title:", {item["title"]}\n """
            items += f""" "Link:", {item["link"]}\n """
            items += f""" "Snippet:", {item["snippet"]}\n """
            items += f""" \n """
    return items
