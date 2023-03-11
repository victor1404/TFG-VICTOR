import requests
import json
import pandas as pd

def weather(city):
    api_address='http://api.openweathermap.org/data/2.5/weather?appid=0c42f7f6b53b244c78a418f4f181282a&q='

    url = api_address + city 
    json_data = requests.get(url).json() 
    format_add = json_data['main'] 
    print(format_add) 
    return format_add


def query_demo():
    query = """query {
        characters {
        results {
        name
        status
        species
        type
        gender
        }
    }
    }"""

    url = 'https://rickandmortyapi.com/graphql/'
    r = requests.post(url, json={'query': query})
    print(r.status_code)
    print(r.text)
    json_data = json.loads(r.text)
    df_data = json_data['data']['characters']['results']
    df = pd.DataFrame(df_data)
    print(df_data)

def query_decidim():
    query = """query {
        decidim {
            version
        }
    }"""

    url = 'https://www.decidim.barcelona/api/'
    r = requests.post(url, json={'query': query})
    print(r.status_code)
    print(r.text)
    json_data = json.loads(r.text)
    print(json_data)