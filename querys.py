import requests
import json
import pandas as pd


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


def query_user_information(user_name):
    query = ("""query {
        users(filter: {name:""" + '"' + f"{user_name}" + '"' +  """}) {
            avatarUrl
            badge
            deleted
            id
            name
            nickname
            organizationName
            profilePath
            __typename
        }
    }""")

    print(query)

    url = 'https://www.decidim.barcelona/api/'
    r = requests.post(url, json={'query': query})
    print(r.status_code)
    print(r.text)
    json_data = json.loads(r.text)
    print(json_data)


def query_latest_ParticipatoryProceses():
    query = ("""query {
                    participatoryProcesses(order: {publishedAt: "desc"}) {
                        slug
                        id
                        publishedAt
                        attachments {
                        url
                        thumbnail
                        }
                        components {
                        name {
                            translation(locale: "es")
                        }
                        }
                        description {
                        translation(locale: "es")
                        }
                        localArea {
                        translation(locale: "es")
                        }
                        title {
                        translation(locale: "es")
                        }
                    }
                }""")

    print(query)

    url = 'https://www.decidim.barcelona/api/'
    r = requests.post(url, json={'query': query})
    print(r.status_code)
    # print(r.text)
    json_data = json.loads(r.text)
    print(json_data["data"]["participatoryProcesses"][0])
    return json_data["data"]["participatoryProcesses"][0]