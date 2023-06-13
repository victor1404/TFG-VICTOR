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



class ActionGET_ParticipatoryeProcess(Action):
    
    def name(self) -> Text:
        return "action_procesos_participativos"

    def run(self, dispatcher: CollectingDispatcher,
    tracker: Tracker,
    domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        #obtenemos entities y slots necesarios para la action
        barrio = next(tracker.get_latest_entity_values("barrio"), None)
        mencion = next(tracker.get_latest_entity_values("mencion"), None)
        usuario_registrado = tracker.get_slot("usuario_registrado")
        user_name = tracker.get_slot("user_name")

        #si el usuario está registrado y quiere un proceso de su barrio, buscaremos cual es su barrio en la bdd
        if usuario_registrado == "REGISTRADO" and mencion == "mi":
            dbname = get_database()


            collection_name = dbname["users_list"]
            item_details = list(collection_name.find({"user_name" : user_name }))[0]

            if len(item_details) == 0:
                print("error con usuario")
                return []

            barrio = item_details["neighbour"]

            #posteriormente buscaremos un proceso en dicho barrio 
            response = querys.query_ParticipatoryProceses_location(barrio)
            found = response[1]
            response_dict = response[0]
            
            #le indicaremos si hemos encontrado un proceso en su barrio o no y le devolveremos un proceso
            if found:
                dispatcher.utter_message(text="He encontrado este proceso cerca de tu barrio")
            else:
                dispatcher.utter_message(text="No he encontrado ningún proceso cerca de tu barrio, pero te recomiendo el último proceso que se añadió a Decidim:")

            title = response_dict["title"]["translation"]
            dispatcher.utter_message(text=f"**{title}**")

            slug = response_dict["slug"]
            l = "https://www.decidim.barcelona/processes/" + slug

            dispatcher.utter_template("utter_give_link", tracker, link=l)

            #y guardamos el slug actual
            return [SlotSet("slug_actual", slug)]
 

        elif mencion is not None:
            #si el usuario pide recuperar el último barrio del que se habló
            if mencion.lower() == "ultimo":
                slug = tracker.get_slot('slug_actual')
                if slug == None:
                    dispatcher.utter_message(text="No sé de que proceso me hablas") 
                    return []              

                response_dict = querys.query_ParticipatoryProces_by_slug(slug)

                title = response_dict["title"]["translation"]
                dispatcher.utter_message(text=f"El último proceso del que hablamos era: **{title}**")               

                slug = response_dict["slug"]
                l = "https://www.decidim.barcelona/processes/" + slug
                dispatcher.utter_template("utter_give_link", tracker, link=l)
                return []

            #si el usuario quiere un proceso de su barrio 
            elif mencion.lower() == "mi":
                barrio = tracker.get_slot("barrio")
                if barrio is None:
                    dispatcher.utter_message(text="No sé cual es tu barrio") 
                    return [] 
                else:
                    response = querys.query_ParticipatoryProceses_location(barrio)
                    found = response[1]
                    response_dict = response[0]
                    
                    #le indicaremos si hemos encontrado un proceso en su barrio o no y le devolveremos un proceso
                    if found:
                        dispatcher.utter_message(text="He encontrado este proceso cerca de tu barrio")
                    else:
                        dispatcher.utter_message(text="No he encontrado ningún proceso cerca de tu barrio, pero te recomiendo el último proceso que se añadió a Decidim:")

                    title = response_dict["title"]["translation"]
                    dispatcher.utter_message(text=f"**{title}**")

                    slug = response_dict["slug"]
                    l = "https://www.decidim.barcelona/processes/" + slug

                    dispatcher.utter_template("utter_give_link", tracker, link=l)

                    #y guardamos el slug actual
                    return [SlotSet("slug_actual", slug)]


        elif barrio is None:
            # si no nos ha proporcionado un lugar, se le ofrece el último proceso
            response_dict = querys.query_latest_ParticipatoryProceses()

            title = response_dict["title"]["translation"]
            dispatcher.utter_message(text=f"Te recomiendo el último proceso añadido: **{title}**")               

            slug = response_dict["slug"]
            l = "https://www.decidim.barcelona/processes/" + slug
            dispatcher.utter_template("utter_give_link", tracker, link=l)
            return [SlotSet("slug_actual", slug)]


        else:
            #si el usuario ha indicado un lugar se intenta buscar en ese lugar
            response = querys.query_ParticipatoryProceses_location(barrio)
            found = response[1]
            response_dict = response[0]
            
            #le indicaremos si hemos encontrado un proceso en su barrio o no y le devolveremos un proceso
            if found:
                dispatcher.utter_message(text=f"He encontrado este proceso cerca de {barrio}")
            else:
                dispatcher.utter_message(text=f"No he encontrado ningún proceso cerca de {barrio}, pero te recomiendo el último proceso que se añadió a Decidim:")

            title = response_dict["title"]["translation"]
            dispatcher.utter_message(text=f"**{title}**")

            slug = response_dict["slug"]
            l = "https://www.decidim.barcelona/processes/" + slug

            dispatcher.utter_template("utter_give_link", tracker, link=l)

            #y guardamos el slug actual
            return [SlotSet("slug_actual", slug)]


class ActionLOOK_ParticipatoryProcess(Action):

    def name(self) -> Text:
        return "action_mirar_en_proceso_participativo"

    def run(self, dispatcher: CollectingDispatcher,
    tracker: Tracker,
    domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        #obtenemos entities y slots necesarios para la action
        intent = tracker.latest_message['intent'].get('name')
        slug = tracker.get_slot("slug_actual") 

        #no sabemos a que proceso se refiere
        if slug is None:
            dispatcher.utter_message("No sé a que proceso participativo te refieres")
            return []

        #si ha preguntado sobre debates buscamos si tiene ese componente
        if intent == "debate_en_proceso_participativo":

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


        #si ha preguntado sobre encuentros buscamos si tiene ese componente
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


        #si ha preguntado sobre propuestas buscamos si tiene ese componente
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


        #si ha preguntado sobre presupuestos buscamos si tiene ese componente
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
        
        #obtenemos el contexto en que se encuentra el usuario
        contexto = tracker.get_slot('contexto')

        #si no tiene contexto es porque se encuentra en la página principal
        if contexto is None:
            dispatcher.utter_template("utter_inform", tracker)
            dispatcher.utter_template("utter_discoverability", tracker)
            return []

        #obtenemos el último intent
        intent = tracker.latest_message['intent'].get('name')

        #si esta acción ha saltado por un cambio de página, controlaremos que solo acceda una vez
        if intent == "cambio_pagina":
            estado_contexto = tracker.get_slot('estado_contexto')
            entity = next(tracker.get_latest_entity_values("contexto"), None)

            #si el contexto es True, quiere decir que el usuario aún no ha estado en esta página
            if estado_contexto[entity]:
                # por tanto lo ponemos a False, ya que acaba de llegar a ella por primera vez y mostramos la explicación de la página
                estado_contexto[entity] = False
                dispatcher.utter_template("utter_change_page", tracker)
                
                #y actualizamos el estado de las paginas visitadas
                return [SlotSet('estado_contexto', estado_contexto)]
            return []
        
        #en caso contrario el usuario ha preguntado expresamente, por tanto se le da la explicación de la página donde esté
        else:
            dispatcher.utter_template("utter_change_page", tracker)
            return []


class Action_CONTRL_FLOW_PROPOSALS(Action):

    def name(self) -> Text:
        return "action_control_flow_proposals"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            
        #obtenemos el último intent
        intent = tracker.latest_message['intent'].get('name')

        #si esta acción ha saltado por un cambio de página, controlaremos que solo acceda una vez
        if intent == "cambio_pagina":
            estado_contexto = tracker.get_slot('estado_contexto')
            entity = next(tracker.get_latest_entity_values("contexto"), None)
            
            #si el contexto es True, quiere decir que el usuario aún no ha estado en esta página
            if estado_contexto[entity]:
                # por tanto lo ponemos a False, ya que acaba de llegar a ella por primera vez y mostramos las funcionalidades relacionadas con propuestas
                estado_contexto[entity] = False
                dispatcher.utter_template("utter_control_flow_proposals", tracker)
                
                #y actualizamos el estado de las paginas visitadas
                return [SlotSet('estado_contexto', estado_contexto)]
            return []
        
        #si esta acción ha saltado por otro intent mostramos las funcionalidades relacionadas con propuestas
        dispatcher.utter_template("utter_control_flow_proposals", tracker)
        return []


class ActionLAST3_PROPOSALS(Action):

    def name(self) -> Text:
        return "action_last_3_proposals"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        #obtenemos el slug del proceso en el que se encuentra el usuario y hacemos una query para obtener las últimas propuestas de ese proceso
        slug_actual = str(tracker.get_slot('slug_actual'))
        response = querys.query_last3_Proposals_by_slug(slug_actual)
        
        #le mostramos las propuestas al usuario
        dispatcher.utter_message(text="Estas son las últimas 3 propuestas:")

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


class Action_OFRECER_PROPUESTAS_AMIGOS(Action):

    def name(self) -> Text:
        return "action_propuestas_amigos"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        #obtenemos el nombre del usuario
        user_name = tracker.get_slot("user_name")

        if user_name is not None:

            #buscamos al usuario en la bdd y obtenemos sus amistades
            dbname = get_database()     
            collection_name = dbname["users_list"]
            item_details = list(collection_name.find({"user_name" : user_name}))[0]
            
            
            if "community" in item_details.keys():
                arrayToFind = item_details["community"]
                community = list(collection_name.find({"user_name" : { "$in" : arrayToFind } }))
                
                #dentro de cada amigo iteramos por los procesos participativos y obtenemos las propuestas que siguen de dicho proceso
                for member in community:
                    if "participative_processes" in member.keys():
                        for pp in member["participative_processes"]:
                            
                            slug = list(pp.keys())[0]
                            for propuesta in pp[slug]:
                                nombre = propuesta["nombre"]
                                dispatcher.utter_message(f"- {nombre}")
                                
                                collection_procesos = dbname["ProcesosParticipativos"]
                                proceso = list(collection_procesos.find({"_id" : slug}))[0]

                                link = ""
                                for p in proceso["propuestas"]:
                                    if p["nombre"] == nombre:
                                        link = p["url"]

                                dispatcher.utter_message(text=link)
                return []

            #si el usuario no tiene amigos le indicamos que no podemos buscar propuestas
            else:
                dispatcher.utter_message("No tienes amigos, no podemos ofrecerte ninguna propuesta.")
                return []   

        #si el usuario no tuviera nombre habria sucedido algún error
        dispatcher.utter_message("Ha habido algún error con tu nombre de usuario...")
        return []


class ActionOFFER_resumen_encuentros(Action):

    def name(self) -> Text:
        return "action_offer_resumen_encuentros"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            
        #obtenemos el último intent
        intent = tracker.latest_message['intent'].get('name')

        #si esta acción ha saltado por un cambio de página, controlaremos que solo acceda una vez
        if intent == "cambio_pagina":
            estado_contexto = tracker.get_slot('estado_contexto')
            entity = next(tracker.get_latest_entity_values("contexto"), None)
            
            #si el contexto es True, quiere decir que el usuario aún no ha estado en esta página
            if estado_contexto[entity]:
                estado_contexto[entity] = False
                dbname = get_database()

                #obtenemos el slug del proceso actual y buscamos dicho proceso en la bdd
                slug = str(tracker.get_slot('slug_actual'))
                collection_name = dbname["ProcesosParticipativos"]
                item_details = list(collection_name.find({"_id" : slug}))[0]

                #si no tiene encuentros el chatbot no ofrecerá nada pero tampoco guardará los cambios en el contexto
                if "encuentros" not in item_details.keys():
                    print("sin encuentros")
                    return []

                #en caso de tener encuentros mostramos sus nombres
                dispatcher.utter_message(f"Puedo ofrecerte un resumen de algún encuentro de este proceso:")

                encuentros = []
                for encuentro in item_details["encuentros"]:
                    nombre = encuentro["nombre"]
                    encuentros.append(nombre)
                    dispatcher.utter_message(f"- {nombre}")

                dispatcher.utter_message("Indicame cuál prefieres")
                
                #y actualizamos el estado de las paginas visitadas y guardamos la lista de encuentros ofrecidos
                SlotSet('estado_contexto', estado_contexto) 
                return [SlotSet('lista_ofrecida', encuentros)]
            return []


        #si esta acción ha saltado por otro intent, ejecutamosel codigo igual que arriba 
        dbname = get_database()

        slug = str(tracker.get_slot('slug_actual'))
        collection_name = dbname["ProcesosParticipativos"]
        item_details = list(collection_name.find({"_id" : slug}))[0]

        if "encuentros" not in item_details.keys():
            print("sin encuentros")
            if str(tracker.latest_message['intent'].get('name')) == "resumen_encuentros":
                dispatcher.utter_message("Lo siento no puedo hacer un resumen si no hay comentarios en los encuentros")
            return []

        dispatcher.utter_message(f"Puedo ofrecerte un resumen de algún encuentro de este proceso:")

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

        #obtenemos la referencia a la lista de la mención
        value = 1

        try:
            value = int(mencion)
        except:
            if mencion == "unico" or mencion == "unica":
                value = 1
            if mencion == "primera" or mencion == "primero" or mencion == "1o" or mencion == "1a":
                value = 1
            if mencion == "segunda" or mencion == "segundo" or mencion == "2o" or mencion == "2a":
                value = 2
            if mencion == "tercera" or mencion == "tercero" or mencion == "3o" or mencion == "3a":
                value = 3
            if mencion == "ultima" or mencion == "ultimo":
                value = 0

        #obtenemos la lista ofrecida
        lista_ofrecida = tracker.get_slot('lista_ofrecida')

        if value > len(lista_ofrecida) or value < 0:
            dispatcher.utter_message("Escoja una de las que he mencionado por favor")
            return []
            

        #obtenemos el valor de la referencia
        encuentro = lista_ofrecida[value-1]

        dispatcher.utter_message(f"Te resumiré el encuentro *{encuentro}*:")
        dispatcher.utter_message("Un momento, por favor")

        #buscamos el proceso participativo y nos guardamos sus comentarios en una lista
        collection_name = dbname["ProcesosParticipativos"]
        item_details = collection_name.find({"_id" : slug})
        comentarios=[]
        for item in item_details:
            comentarios = item["encuentros"][value-1]["comentarios"]

        #unificamos la lista en un bloque de texto y llamamos a la función que resume dicho bloque
        text = ''.join(comentarios)
        threshold = 1.2
        summary = run_summarization(text, threshold)

        #debido a que cada texto puede tener una longitud diferente, necesitamos un threshold diferente para obtener un buen resumen, 
        #para ello se irá decrementando el threshold hasta obtener un texto resumido
        while summary == "":
            threshold -= 0.1
            summary = run_summarization(text, threshold)

        #mostramos el texto al usuario
        dispatcher.utter_message("El resumen es el siguiente:")
        dispatcher.utter_message(f"{summary}")
        return []


class Action_CONTRL_FLOW(Action):

    def name(self) -> Text:
        return "action_control_flow"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            
        #obtenemos el último intent
        intent = tracker.latest_message['intent'].get('name')

        #si esta acción ha saltado por un cambio de página, controlaremos que solo acceda una vez
        if intent == "cambio_pagina":
            estado_contexto = tracker.get_slot('estado_contexto')
            entity = next(tracker.get_latest_entity_values("contexto"), None)
            
            #si el contexto es True, quiere decir que el usuario aún no ha estado en esta página
            if estado_contexto[entity]:
                # por tanto lo ponemos a False, ya que acaba de llegar a ella por primera vez y ofrecemos la función de buscar un proceso según los gustos del usuario
                estado_contexto[entity] = False
                dispatcher.utter_template("utter_control_flow", tracker)
                
                #y actualizamos el estado de las paginas visitadas
                return [SlotSet('estado_contexto', estado_contexto)]
            return []
        
        #si esta acción ha saltado por otro intent ofrecemos la función de buscar un proceso según los gustos del usuario
        dispatcher.utter_template("utter_control_flow", tracker)
        return []


class ActionOfferPP_Tematica(Action):

    def name(self) -> Text:
        return "action_offer_pp_tematica"

    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        #obtenemos el nombre de usuario
        user_name = tracker.get_slot('user_name')

        if user_name is not None:
            
            #buscamos al usuario en la bdd y obtenemos sus intereses
            dbname = get_database()     
            collection_name = dbname["users_list"]
            item_details = list(collection_name.find({"user_name" : user_name}))[0]
            
            if "interests" in item_details.keys():
                #buscamos un proceso que cumpla con dichos intereses
                arrayToFind = item_details["interests"]
                response = querys.query_ParticipatoryProceses_interests(arrayToFind)

                #si obtenemos algún proceso de acuerdo a dichos intereses los mostramos al usuario
                if response:
                    dispatcher.utter_message("Tenemos los siguientes procesos según tus intereses: ")
                    for pp in response:
                        slug = pp["slug"]
                        nombre = pp["title"]["translation"]
                        dispatcher.utter_message(f"- {nombre}")
                        link = "https://www.decidim.barcelona/processes/" + slug
                        dispatcher.utter_message(text=link)
                    return []

                #en caso de no obtener ningún proceso informamos al usuario
                else:
                    dispatcher.utter_message("Ningún proceso cumple con tus intereses. Para solucionarlo espere a que se añadan más procesos o amplíe sus intereses.")
                    return []
                
            else:
                dispatcher.utter_message("No puedo buscar un proceso si no has seleccionado ningún interés. Para ello navega hasta tu perfil de usuario.")
                return []   

        dispatcher.utter_message("Ha habido algún error con tu nombre de usuario...")
        return []


class ActionValidarNeighbor(Action):

    def name(self) -> Text:
        return "action_validar_neighbor"

    def run(self, dispatcher: CollectingDispatcher,
    tracker: Tracker,
    domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        #obtenemos el barrio indicado
        barrio = next(tracker.get_latest_entity_values("barrio"), None)

        if barrio is not None:
            if barrio.title() in ALLOWED_LOCATIONS:
                #si el barrio está dentro de los permitidos le informamos y guardamos el barrio en un slot
                dispatcher.utter_message(f"Genial. Recordaré ese barrio ({barrio})")
                return [SlotSet("barrio", barrio)]

        #en caso contrario le indicamos los barrios disponibles.
        dispatcher.utter_message("Puedes indicarme uno de estos barrios y recordaré que te interesa:")
        dispatcher.utter_message("Ciutat Vella, Eixample, Sants, Sarria, Sant Gervasi, Les Corts, Gracia, Horta, Guinardó, Nou Barris, Sant Andreu o Sant Martí.")
        return []

