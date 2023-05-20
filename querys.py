import requests
import json
import pandas as pd
from datetime import datetime


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
    r = requests.post(url, json={'query': query})
    print(r.status_code)
    # print(r.text)
    json_data = json.loads(r.text)["data"]["participatoryProcesses"]
    # print(json_data["data"]["participatoryProcesses"][0])
    # return json_data["data"]["participatoryProcesses"][0]

    response = json_data[0]
    found = False
    today = datetime.today().strftime('%Y-%m-%d')

    for process in json_data:
        if not found:
            if process["endDate"] >= today:
                found = True
                response = process
    return response


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
    r = requests.post(url, json={'query': query})
    print(r.status_code)
    # print(r.text)
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
                elif location in process["title"]["translation"] or location in process["description"]["translation"] or location in process["localArea"]["translation"]:
                    found = True
                    response = process
    return response



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
    r = requests.post(url, json={'query': query})
    print(r.status_code)
    # print(r.text)
    json_data = json.loads(r.text)["data"]["participatoryProcess"]["components"]
    print(json_data)

    return json_data

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
    r = requests.post(url, json={'query': query})
    print(r.status_code)

    json_data = json.loads(r.text)["data"]["participatoryProcess"]

    response = json_data
    found = False
    return response


def query_last3_Proposals_by_slug(slug):
    query = ("""query {
                    participatoryProcess(slug: """ + '"' + f"{slug}" + '"' +  """) {
                        id
                        components {
                        ... on Proposals {
                            id
                            proposals(last: 3) {
                            nodes {
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
    r = requests.post(url, json={'query': query})
    print(r.status_code)

    json_data = json.loads(r.text)["data"]["participatoryProcess"]

    response = json_data
    found = False
    return response









































# QUERYS SIN USO
    def query_Debates():
        query = ("""query {
                        participatoryProcesses(filter: {publishedSince: "2022-01-01"}) {
                            slug
                            title {
                            translation(locale: "es")
                            }
                            components {
                            ... on Meetings {
                                id
                                __typename
                                participatorySpace{
                                id
                                title {
                                    translation (locale: "es")
                                }
                                }
                            }
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

    def query_Surveys():
        query = ("""query {
                        participatoryProcesses(filter: {publishedSince: "2022-01-01"}) {
                            slug
                            title {
                            translation(locale: "es")
                            }
                            components {
                            ... on Surveys {
                                id
                                __typename
                                participatorySpace{
                                id
                                title {
                                    translation (locale: "es")
                                }
                                }
                            }
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

    def query_Budgets():
        query = ("""query {
                        participatoryProcesses(filter: {publishedSince: "2022-01-01"}) {
                            slug
                            title {
                            translation(locale: "es")
                            }
                            components {
                            ... on Budgets {
                                id
                                __typename
                                participatorySpace{
                                id
                                title {
                                    translation (locale: "es")
                                }
                                }
                            }
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
        
    def query_Proposals():
        query = ("""query {
                        participatoryProcesses(filter: {publishedSince: "2022-01-01"}) {
                            slug
                            title {
                            translation(locale: "es")
                            }
                            components {
                            ... on Proposals {
                                id
                                __typename
                                participatorySpace{
                                id
                                title {
                                    translation (locale: "es")
                                }
                                }
                            }
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


    def query_Debate_location():
        query = ("""query {
                        participatoryProcesses(filter: {publishedSince: "2022-01-01"}) {
                            slug
                            title {
                            translation(locale: "es")
                            }
                            localArea {
                            translation(locale: "es")
                            }
                            description {
                            translation(locale: "es")
                            }
                            components {
                            ... on Debates {
                                id
                                __typename
                                participatorySpace{
                                id
                                title {
                                    translation (locale: "es")
                                }
                                }
                            }
                            }
                        }
                        }""")

        print(query)

        url = 'https://www.decidim.barcelona/api/'
        r = requests.post(url, json={'query': query})
        print(r.status_code)
        # print(r.text)
        json_data = json.loads(r.text)
        # print(json_data["data"]["participatoryProcesses"])
        return json_data["data"]["participatoryProcesses"]

    def query_Surveys_location():
        query = ("""query {
                        participatoryProcesses(filter: {publishedSince: "2022-01-01"}) {
                            slug
                            title {
                            translation(locale: "es")
                            }
                            localArea {
                            translation(locale: "es")
                            }
                            description {
                            translation(locale: "es")
                            }
                            components {
                            ... on Surveys {
                                id
                                __typename
                                participatorySpace{
                                id
                                title {
                                    translation (locale: "es")
                                }
                                }
                            }
                            }
                        }
                        }""")

        print(query)

        url = 'https://www.decidim.barcelona/api/'
        r = requests.post(url, json={'query': query})
        print(r.status_code)
        # print(r.text)
        json_data = json.loads(r.text)
        # print(json_data["data"]["participatoryProcesses"])
        return json_data["data"]["participatoryProcesses"]

    def query_Budget_location():
        query = ("""query {
                        participatoryProcesses(filter: {publishedSince: "2022-01-01"}) {
                            slug
                            title {
                            translation(locale: "es")
                            }
                            localArea {
                            translation(locale: "es")
                            }
                            description {
                            translation(locale: "es")
                            }
                            components {
                            ... on Budgets {
                                id
                                __typename
                                participatorySpace{
                                id
                                title {
                                    translation (locale: "es")
                                }
                                }
                            }
                            }
                        }
                        }""")

        print(query)

        url = 'https://www.decidim.barcelona/api/'
        r = requests.post(url, json={'query': query})
        print(r.status_code)
        # print(r.text)
        json_data = json.loads(r.text)
        # print(json_data["data"]["participatoryProcesses"])
        return json_data["data"]["participatoryProcesses"]

    def query_Proposal_location():
        query = ("""query {
                    participatoryProcesses(filter: {publishedSince: "2022-01-01"}) {
                        slug
                        title {
                        translation(locale: "es")
                        }
                        localArea {
                        translation(locale: "es")
                        }
                        description {
                        translation(locale: "es")
                        }
                        components {
                        ... on Proposals {
                            id
                            __typename
                            participatorySpace{
                            id
                            title {
                                translation (locale: "es")
                            }
                            }
                        }
                        }
                    }
                    }""")

        print(query)

        url = 'https://www.decidim.barcelona/api/'
        r = requests.post(url, json={'query': query})
        print(r.status_code)
        # print(r.text)
        json_data = json.loads(r.text)
        # print(json_data["data"]["participatoryProcesses"])
        return json_data["data"]["participatoryProcesses"]
