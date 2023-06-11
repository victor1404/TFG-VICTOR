# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"
import requests

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.events import EventType, SlotSet, FollowupAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
import querys

from pymongo_get_database import get_database
from sumarization import run_summarization


definiciones = {
    "procesos participativos" : "Los procesos participativos son una serie de encuentros delimitados en un tiempo concreto para promover el debate y el contraste de argumentos entre la ciudadanía, o entre ésta y las personas responsables municipales."
    ,"organos de participacion" : "Los órganos de participación son canales de encuentro y de interlocución regulares entre la ciudadanía y el Ayuntamiento para debatir y recoger opiniones y propuestas con el fin de incidir en las políticas municipales. "
    ,"inciativas ciudadanas" : "La iniciativa ciudadana es el medio que tiene la ciudadanía para promover, a través de la recogida de firmas, que el Ayuntamiento lleve a cabo una determinada acción de interés colectivo, siempre que esté dentro de sus competencias."
    ,"registrar" : "Un registro informático es un tipo o conjunto de datos almacenados en un sistema "
    ,"iniciar sesion" : "La sesión informática suele incluir el intercambio de paquetes de información entre un usuario y un servidor. Es habitual que el usuario deba ingresar un nombre de usuario y contraseña para iniciar una sesión, en un procedimiento conocido como log in o loguearse."
    ,"debate" : "Espacios digitales para informarte y decidir sobre las propuestas de cada proceso."
    ,"votacion" : "Acción de votar."
    ,"encuentros" : "Encuentros cara a cara vinculados a los procesos de cada territorio o ámbito."
    ,"propuestas" : "Contribuciones de los participantes que pueden recibir el apoyo de los usuarios con función decisoria."
    ,"presupuesto" : "Cálculo anticipado del coste de una obra o un servicio. "
    ,"consejo de barrio" : "Los Consejos de Barrio son órganos para la participación de los vecinos en el desarrollo de la ciudad, basados en la división territorial del término municipal en barrios."
    ,"comentarios" : "Contribuciones de los usuarios al hilo de una propuesta o debate y que pueden recibir una votación negativa o positiva."

}


ALLOWED_LOCATIONS = ["Ciutat Vella", "Eixample", "Sants", "Sarria", "Sant Gervasi", "Les Corts", "Gracia", "Horta", "Guinardó", "Nou Barris", "Sant Andreu", "Sant Martí"]

ACTUAL_PP = dict()
# class ActionDevolverDebates(Action):

#     def name(self) -> Text:
#         return "action_return_debates"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         neighborhood = tracker.get_slot("neighborhood")
#         dispatcher.utter_message(text=f"Estos son los debates en {neighborhood}a los que te puedes unir:")
        
#         if not neighborhood:
#             dispatcher.utter_message(text=f"No sabemos en que zona estás mas interesada. Igualmente estos son los debates mas populares:")
#         else:
#             dispatcher.utter_message(text=f"Estos son los debates en {neighborhood} a los que te puedes unir:")

#         return []



class ActionGET_ParticipatoryeProcess(Action):
    
    def name(self) -> Text:
        return "action_procesos_participativos"

    def run(self, dispatcher: CollectingDispatcher,
    tracker: Tracker,
    domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        neighborhood = next(tracker.get_latest_entity_values("barrio"), None)
        mencion = next(tracker.get_latest_entity_values("mencion"), None)
        usuario_registrado = tracker.get_slot("usuario_registrado")
        user_name = tracker.get_slot("user_name")

        if usuario_registrado == "REGISTRADO" and mencion == "mi":
            dbname = get_database()


            collection_name = dbname["users_list"]
            item_details = list(collection_name.find({"user_name" : user_name }))

            if len(item_details) == 0:
                print("error con usuario")
                return []

            for item in item_details:
                neighborhood = item["neighbor"]

            response_dict = querys.query_ParticipatoryProceses_location(neighborhood)
            ACTUAL_PP = response_dict
            print(ACTUAL_PP)

            title = response_dict["title"]["translation"]
            if mencion == "mi":
                dispatcher.utter_message(text="He intentado buscar cerca tu barrio")
            else:
                dispatcher.utter_message(text=f"He intentado buscar cerca de {neighborhood}")

            dispatcher.utter_message(text=f"He encontrado esto: **{title}**")

            slug = response_dict["slug"]
            l = "https://www.decidim.barcelona/processes/" + slug
            
            if title == "Reurbanización de los interiores de manzana de la Guineueta":
                l = "ProcesoGuineueta-decidim.barcelona.html"
            dispatcher.utter_template("utter_give_link", tracker, link=l)

            return [SlotSet("slug_actual", slug)]


        if neighborhood is None and mencion == "mi":
            neighborhood = tracker.get_slot("barrio")
            if neighborhood is None:
                dispatcher.utter_message(text="No sé cual es tu barrio") 
                return []  

        if mencion is not None:
            if mencion.lower() == "ultimo":
                slug = tracker.get_slot('slug_actual')
                if slug == None:
                    dispatcher.utter_message(text="No sé de que proceso me hablas") 
                    return []              

                response_dict = querys.query_ParticipatoryProces_by_slug(slug)
                ACTUAL_PP = response_dict
                print(ACTUAL_PP)
                title = response_dict["title"]["translation"]
                dispatcher.utter_message(text=f"El ultimo del que hablamos era: **{title}**")               

                slug = response_dict["slug"]
                l = "https://www.decidim.barcelona/processes/" + slug
                dispatcher.utter_template("utter_give_link", tracker, link=l)
                return []


        if neighborhood is None:
            # no nos ha proporcionado un lugar. 
            response_dict = querys.query_latest_ParticipatoryProceses()
            ACTUAL_PP = response_dict
            print(ACTUAL_PP)
            title = response_dict["title"]["translation"]
            dispatcher.utter_message(text=f"Te recomiendo el proceso: **{title}**")               

            slug = response_dict["slug"]
            # l = "https://www.decidim.barcelona/processes/" + slug
            l = "http://localhost:5000/procesoGuineueta"
            dispatcher.utter_template("utter_give_link", tracker, link=l)
            return [SlotSet("slug_actual", slug)]


        else:
            response_dict = querys.query_ParticipatoryProceses_location(neighborhood)
            ACTUAL_PP = response_dict
            print(ACTUAL_PP)

            title = response_dict["title"]["translation"]
            if mencion == "mi":
                dispatcher.utter_message(text="He intentado buscar cerca tu barrio")
            else:
                dispatcher.utter_message(text=f"He intentado buscar cerca de {neighborhood}")

            dispatcher.utter_message(text=f"He encontrado esto: **{title}**")

            slug = response_dict["slug"]
            l = "https://www.decidim.barcelona/processes/" + slug
            
            if title == "Reurbanización de los interiores de manzana de la Guineueta":
                l = "ProcesoGuineueta-decidim.barcelona.html"
            dispatcher.utter_template("utter_give_link", tracker, link=l)

            return [SlotSet("slug_actual", slug)]


class ActionLOOK_ParticipatoryProcess(Action):

    def name(self) -> Text:
        return "action_mirar_en_proceso_participativo"

    def run(self, dispatcher: CollectingDispatcher,
    tracker: Tracker,
    domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        intent = tracker.latest_message['intent'].get('name')
        slug = tracker.get_slot("slug_actual") 
        print(intent)
        print(tracker.latest_message['entities'])
        print(ACTUAL_PP)
        if slug is None:
            dispatcher.utter_message("No sé a que proceso participativo te refieres")
            return []

        if intent == "debate_en_proceso_participativo":
            SlotSet("interests", "Debates")
            componentes = querys.query_Components_ParticipatoryProceses(slug)

            for component in componentes:
                if (component['__typename'] == "Debates"):
                    dispatcher.utter_message("Sí, el proceso tiene debate")

                    id = component["id"]
                    l = "https://www.decidim.barcelona/processes/" + slug +"/f/"+id
                    dispatcher.utter_template("utter_give_link", tracker, link=l)
                    return []
            
            dispatcher.utter_message("Parece que no tiene debate")
            return []

        elif intent == "encuentro_en_proceso_participativo":
            SlotSet("interests", "Meetings")
            componentes = querys.query_Components_ParticipatoryProceses(slug)

            for component in componentes:
                if (component['__typename'] == "Meetings"):
                    dispatcher.utter_message("Sí, el proceso tiene encuentros")

                    id = component["id"]
                    l = "https://www.decidim.barcelona/processes/" + slug +"/f/"+id
                    dispatcher.utter_template("utter_give_link", tracker, link=l)
                    return []
            
            dispatcher.utter_message("Parece que no tiene encuentros")
            return []

        elif intent == "propuesta_en_proceso_participativo":
            SlotSet("interests", "Proposals")
            componentes = querys.query_Components_ParticipatoryProceses(slug)

            for component in componentes:
                if (component['__typename'] == "Proposals"):
                    dispatcher.utter_message("Sí, el proceso tiene propuestas")

                    id = component["id"]
                    l = "https://www.decidim.barcelona/processes/" + slug +"/f/"+id
                    dispatcher.utter_template("utter_give_link", tracker, link=l)
                    return []
            
            dispatcher.utter_message("Parece que no tiene propuestas")
            return []

        elif intent == "presupuesto_en_proceso_participativo":
            SlotSet("interests", "Budgets")
            componentes = querys.query_Components_ParticipatoryProceses(slug)

            for component in componentes:
                if (component['__typename'] == "Budgets"):
                    dispatcher.utter_message("Sí, el proceso tiene presupuestos")

                    id = component["id"]
                    l = "https://www.decidim.barcelona/processes/" + slug +"/f/"+id
                    dispatcher.utter_template("utter_give_link", tracker, link=l)
                    return []
            
            dispatcher.utter_message("Parece que no tiene presupuestos")
            return []


class ActionGET_contexto_AND_ID(Action):

    def name(self) -> Text:
        return "action_show_contexto_and_id"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        contexto = tracker.get_slot('contexto')

        if contexto == None:
            dispatcher.utter_template("utter_inform", tracker)
            dispatcher.utter_template("utter_discoverability", tracker)
            return []

        intent = tracker.latest_message['intent'].get('name')

        if intent == "cambio_pagina":
            estado_contexto = tracker.get_slot('estado_contexto')
            print(estado_contexto)
            entity = next(tracker.get_latest_entity_values("contexto"), None)
            if estado_contexto[entity]:
                estado_contexto[entity] = False
                dispatcher.utter_template("utter_change_page", tracker)
                return [SlotSet('estado_contexto', estado_contexto)]
            return []


        
        id = tracker.sender_id 
        print(id)

        print(contexto)

        pp = str(tracker.get_slot('slug_actual'))
        print(pp)

        state = str(tracker.get_slot('usuario_registrado'))
        print(state)

        dispatcher.utter_template("utter_change_page", tracker)

        return []


class ActionLAST3_PROPOSALS(Action):

    def name(self) -> Text:
        return "action_last_3_proposals"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        intent = tracker.latest_message['intent'].get('name')

        if intent == "cambio_pagina":
            estado_contexto = tracker.get_slot('estado_contexto')
            print(estado_contexto)
            entity = next(tracker.get_latest_entity_values("contexto"), None)

            if estado_contexto[entity]:
                estado_contexto[entity] = False
                slug_actual = str(tracker.get_slot('slug_actual'))

                response = querys.query_last3_Proposals_by_slug(slug_actual)
                
                dispatcher.utter_message(text="Estas son las ultimas 3 propuestas:")

                for component in response["components"]:
                    if "proposals" in component.keys():
                        id = component["id"]
                        for proposal in component["proposals"]["nodes"]:
                            nombre = proposal["title"]["translation"]
                            dispatcher.utter_message(f"- {nombre}")
                            link = "https://www.decidim.barcelona/processes/" + slug_actual + "/f/" + id + "/proposals/" + proposal["id"]
                            dispatcher.utter_message(text=link)
                return [SlotSet('estado_contexto', estado_contexto)]

            return []


        slug_actual = str(tracker.get_slot('slug_actual'))

        response = querys.query_last3_Proposals_by_slug(slug_actual)
        
        dispatcher.utter_message(text="Estas son las ultimas 3 propuestas:")

        for component in response["components"]:
            if "proposals" in component.keys():
                id = component["id"]
                for proposal in component["proposals"]["nodes"]:
                    nombre = proposal["title"]["translation"]
                    if nombre is None:
                        nombre = "Sin titulo"
                    dispatcher.utter_message(f"- {nombre}")
                    link = "https://www.decidim.barcelona/processes/" + slug_actual + "/f/" + id + "/proposals/" + proposal["id"]
                    dispatcher.utter_message(text=link)

        return []


class Action_CONTRL_FLOW_PROPOSALS(Action):

    def name(self) -> Text:
        return "action_control_flow_proposals"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        intent = tracker.latest_message['intent'].get('name')

        if intent == "cambio_pagina":
            estado_contexto = tracker.get_slot('estado_contexto')
            print(estado_contexto)
            entity = next(tracker.get_latest_entity_values("contexto"), None)
            if estado_contexto[entity]:
                # estado_contexto[entity] = False
                dispatcher.utter_template("utter_control_flow_proposals", tracker)
                return [SlotSet('estado_contexto', estado_contexto)]
            return []
        
        dispatcher.utter_template("utter_control_flow_proposals", tracker)
        return []


class Action_OFRECER_PROPUESTAS_AMIGOS(Action):

    def name(self) -> Text:
        return "action_propuestas_amigos"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        user_name = tracker.get_slot("user_name")
        print(user_name)

        if user_name is not None:

            dbname = get_database()     
            collection_name = dbname["users_list"]
            item_details = list(collection_name.find({"user_name" : user_name}))[0]
            # print(item_details)
            
            if "community" in item_details.keys():
                arrayToFind = item_details["community"]
                print(arrayToFind)
                community = list(collection_name.find({"user_name" : { "$in" : arrayToFind } }))
                # print(community)
                for member in community:
                    if "participative_processes" in member.keys():
                        # print(member)
                        for pp in member["participative_processes"]:
                            print(pp)
                            slug = list(pp.keys())[0]
                            for propuesta in pp[slug]:
                                nombre = propuesta["nombre"]
                                print(nombre)
                                dispatcher.utter_message(f"- {nombre}")
                                
                                collection_procesos = dbname["ProcesosParticipativos"]
                                proceso = list(collection_procesos.find({"_id" : slug}))[0]
                                print(proceso)
                                link = ""
                                for p in proceso["propuestas"]:
                                    if p["nombre"] == nombre:
                                        link = p["url"]
                                dispatcher.utter_message(text=link)

                return []

            else:
                dispatcher.utter_message("No tienes amigos...")
                return []   

            
        dispatcher.utter_message("Ha habido algun error con tu nombre de usuario...")
        return []


class ActionOFFER_resumen_encuentros(Action):

    def name(self) -> Text:
        return "action_offer_resumen_encuentros"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        intent = tracker.latest_message['intent'].get('name')

        if intent == "cambio_pagina":
            estado_contexto = tracker.get_slot('estado_contexto')
            print(estado_contexto)
            entity = next(tracker.get_latest_entity_values("contexto"), None)
            if estado_contexto[entity]:
                estado_contexto[entity] = False
                dbname = get_database()

                slug = str(tracker.get_slot('slug_actual'))


                collection_name = dbname["ProcesosParticipativos"]
                item_details = list(collection_name.find({"_id" : slug}))[0]
                print(item_details)

                if "encuentros" not in item_details.keys():
                    print("sin encuentros")
                    return []

                # dispatcher.utter_message(f"Tenemos los siguientes encuentros para el proceso {slug}:")
                dispatcher.utter_message(f"Puedo ofrecerte un resumen de algun encuentro del proceso {slug}:")

                encuentros = []
                for encuentro in item_details["encuentros"]:
                    # print(encuentro)
                    nombre = encuentro["nombre"]
                    encuentros.append(nombre)
                    dispatcher.utter_message(f"- {nombre}")

                dispatcher.utter_message("Indicame cual prefieres")
                
                SlotSet('estado_contexto', estado_contexto) 
                return [SlotSet('lista_ofrecida', encuentros)]
            return []


        dbname = get_database()

        slug = str(tracker.get_slot('slug_actual'))


        collection_name = dbname["ProcesosParticipativos"]
        item_details = list(collection_name.find({"_id" : slug}))[0]

        if "encuentros" not in item_details.keys():
            print("sin encuentros")
            if str(tracker.latest_message['intent'].get('name')) == "resumen_encuentros":
                dispatcher.utter_message("Lo siento no puedo hacer un resumen si no hay comentarios")
            return []

        dispatcher.utter_message(f"Puedo ofrecerte un resumen de algun encuentro del proceso {slug}:")

        encuentros = []
        for encuentro in item_details["encuentros"]:
            nombre = encuentro["nombre"]
            encuentros.append(nombre)
            dispatcher.utter_message(f"- {nombre}")

        dispatcher.utter_message("Indicame cual prefieres")

        return [SlotSet('lista_ofrecida', encuentros)]


class ActionSumarization(Action):

    def name(self) -> Text:
        return "action_sumarization"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        dbname = get_database()

        slug = str(tracker.get_slot('slug_actual'))
        mencion = next(tracker.get_latest_entity_values("mencion"), None)
        print(mencion)

        value = 1

        try:
            value = int(mencion)
            print("es un numero: ", value)
        except:
            if mencion == "unico" or mencion == "unica":
                value = 1
                print("La unica")
            if mencion == "primera" or mencion == "primero" or mencion == "1o" or mencion == "1a":
                value = 1
                print("La primera")
            if mencion == "segunda" or mencion == "segundo" or mencion == "2o" or mencion == "2a":
                value = 2
                print("La segunda")
            if mencion == "tercera" or mencion == "tercero" or mencion == "3o" or mencion == "3a":
                value = 3
                print("La tercera")
            if mencion == "ultima" or mencion == "ultimo":
                value = 0
                print("La ultima")

        lista_ofrecida = tracker.get_slot('lista_ofrecida')
        print(lista_ofrecida)

        if value > len(lista_ofrecida) or value < 0:
            dispatcher.utter_message("Escoja una de las que he mencionado por favor")
            return []
            

        encuentro = lista_ofrecida[value-1]

        dispatcher.utter_message(f"Te resumiré el encuentro *{encuentro}*:")
        dispatcher.utter_message("Un momento, por favor")


        collection_name = dbname["ProcesosParticipativos"]
        item_details = collection_name.find({"_id" : slug})
        comentarios=[]
        for item in item_details:
            comentarios = item["encuentros"][value-1]["comentarios"]

        text = ''.join(comentarios)
        threshold = 1.2
        summary = run_summarization(text, threshold)
        while summary == "":
            threshold -= 0.1
            summary = run_summarization(text, threshold)

        dispatcher.utter_message("El resumen es el siguiente:")
        dispatcher.utter_message(f"{summary}")
        return []


class Action_CONTRL_FLOW(Action):

    def name(self) -> Text:
        return "action_control_flow"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        intent = tracker.latest_message['intent'].get('name')

        if intent == "cambio_pagina":
            estado_contexto = tracker.get_slot('estado_contexto')
            print(estado_contexto)
            entity = next(tracker.get_latest_entity_values("contexto"), None)
            if estado_contexto[entity]:
                estado_contexto[entity] = False
                dispatcher.utter_template("utter_control_flow", tracker)
                return [SlotSet('estado_contexto', estado_contexto)]
            return []
        
        dispatcher.utter_template("utter_control_flow", tracker)
        return []

class ActionOfferPP_Tematica(Action):

    def name(self) -> Text:
        return "action_offer_pp_tematica"

    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        user_name = tracker.get_slot('user_name')

        if user_name is not None:
            dbname = get_database()     
            collection_name = dbname["users_list"]
            item_details = list(collection_name.find({"user_name" : user_name}))[0]
            
            if "interests" in item_details.keys():
                arrayToFind = item_details["interests"]
                response = querys.query_ParticipatoryProceses_interests(arrayToFind)
                # print(response)

                if response:
                    dispatcher.utter_message("Tenemos los siguientes procesos según tus intereses: ")
                    for pp in response:
                        slug = pp["slug"]
                        nombre = pp["title"]["translation"]
                        dispatcher.utter_message(f"- {nombre}")
                        link = "https://www.decidim.barcelona/processes/" + slug
                        dispatcher.utter_message(text=link)

                return []
                
            else:
                dispatcher.utter_message("No tienes intereses...")
                return []   

        dispatcher.utter_message("Ha habido algun error con tu nombre de usuario...")
        return []


class ActionValidarNeighbor(Action):

    def name(self) -> Text:
        return "action_validar_neighbor"

    def run(self, dispatcher: CollectingDispatcher,
    tracker: Tracker,
    domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        neighborhood = next(tracker.get_latest_entity_values("barrio"), None)
        if neighborhood is not None:
            if neighborhood.title() in ALLOWED_LOCATIONS:
                dispatcher.utter_message(f"Genial. Recordaré ese barrio ({neighborhood})")
                return [SlotSet("barrio", neighborhood)]

        dispatcher.utter_message("Puedes indicarme uno de estos barrios y recordaré que te interesa:")
        dispatcher.utter_message("Ciutat Vella, Eixample, Sants, Sarria, Sant Gervasi, Les Corts, Gracia, Horta, Guinardó, Nou Barris, Sant Andreu o Sant Martí.")
        return []

