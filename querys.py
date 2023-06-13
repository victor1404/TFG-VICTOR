import requests
import json
import pandas as pd
from datetime import datetime

#query que filtra los procesos en orden de más nuevo a más antiguo y devuelve el proceso más nuevo
def query_latest_ParticipatoryProceses():
    query = ("""query {
                    participatoryProcesses(order: {publishedAt: "desc"}) {
                        slug
                        id
                        publishedAt
                        endDate
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
    r = requests.post(url, json={'query': query}, verify=False)
    print(r.status_code)
    json_data = json.loads(r.text)["data"]["participatoryProcesses"]

    response = json_data[0]
    found = False
    today = datetime.today().strftime('%Y-%m-%d')

    for process in json_data:
        if not found:
            if process["endDate"] >= today:
                found = True
                response = process
    return response

#query que filtra un proceso según una localización. En caso de no encontrar ninguno devuelve el proceso más nuevo
def query_ParticipatoryProceses_location(location):
    query = ("""query {
                    participatoryProcesses(order: {publishedAt: "desc"}) {
                        slug
                        id
                        endDate
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
                        metaScope {
                        translation(locale: "es")
                        }
                    }
                }""")

    print(query)

    url = 'https://www.decidim.barcelona/api/'
    r = requests.post(url, json={'query': query}, verify=False)
    print(r.status_code)
    json_data = json.loads(r.text)["data"]["participatoryProcesses"]

    response = json_data[0]
    found = False
    today = datetime.today().strftime('%Y-%m-%d')

    for process in json_data:
        if not found:
            if process["endDate"] >= today:
                if location in process["metaScope"]["translation"]:
                    found = True
                    response = process
                    return [response, True]
                elif location in process["title"]["translation"] or location in process["description"]["translation"] or location in process["localArea"]["translation"]:
                    found = True
                    response = process
                    return [response, True]
    return [response, False]

#query que devuelve las componentes de un proceso participativo concreto
def query_Components_ParticipatoryProceses(slug):
    query = ("""query {
                    participatoryProcess(slug: """ + '"' + f"{slug}" + '"' +  """) {
                        id
                        components{
                        id
                        __typename
                        }
                    }
                }""")

    print(query)

    url = 'https://www.decidim.barcelona/api/'
    r = requests.post(url, json={'query': query}, verify=False)
    print(r.status_code)
    json_data = json.loads(r.text)["data"]["participatoryProcess"]["components"]

    return json_data

#query que devuelve un proceso participativo concreto
def query_ParticipatoryProces_by_slug(slug):
    query = ("""query {
                    participatoryProcess(slug: """ + '"' + f"{slug}" + '"' +  """) {
                        slug
                        id
                        publishedAt
                        endDate
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
    r = requests.post(url, json={'query': query}, verify=False)
    print(r.status_code)
    json_data = json.loads(r.text)["data"]["participatoryProcess"]

    return json_data

#query que devuelve las ultimas propuestas de un proceso participativo concreto
def query_last3_Proposals_by_slug(slug):
    query = ("""query {
                    participatoryProcess(slug: """ + '"' + f"{slug}" + '"' +  """) {
                        id
                        components {
                        ... on Proposals {
                            id
                            proposals(last: 3) {
                            nodes {
                                title {
                                translation(locale: "es")
                                }
                                id
                                __typename
                                createdAt
                                position
                                publishedAt
                                reference
                            }
                            }
                        }
                        }
                    }
                }""")

    print(query)

    url = 'https://www.decidim.barcelona/api/'
    r = requests.post(url, json={'query': query}, verify=False)
    print(r.status_code)
    json_data = json.loads(r.text)["data"]["participatoryProcess"]

    return json_data

#query que filtra los procesos participativos para encontrar algunos donde el tema del proceso participativo coincida con los intereses
def query_ParticipatoryProceses_interests(arrayToFind):
    query = ("""query {
                    participatoryProcesses(order: {publishedAt: "desc"}) {
                        slug
                        id
                        endDate
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
                        metaScope {
                        translation(locale: "es")
                        }
                    }
                }""")

    print(query)

    url = 'https://www.decidim.barcelona/api/'
    r = requests.post(url, json={'query': query}, verify=False)
    print(r.status_code)
    json_data = json.loads(r.text)["data"]["participatoryProcesses"]

    response = []
    found = False
    today = datetime.today().strftime('%Y-%m-%d')

    for process in json_data:
        if process["endDate"] >= today:
            for interest in arrayToFind:
                if interest.lower() in process["localArea"]["translation"].lower() and process not in response:
                    response.append(process)
    return response

