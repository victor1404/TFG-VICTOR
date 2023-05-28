# Get the database using the method we defined in pymongo_test_insert file
from pymongo_get_database import get_database



user_1 = {
  "_id" : "1",
  "user_name" : "Victor",
  "neighbour" : "Nou Barris", 
  "participative_processes" : [{"usostallermasriera" : [{"nombre":"Poliesportiu piscina municipal"}, {"nombre" : "Taller Masriera Ateneu"}]}],
  "community" : ["Inma", "Maite"],
  "interests": ["Urbanismo", "Urbano"]
  }

user_2 = {
  "_id" : "2",
  "user_name" : "Inma",
  "neighbour" : "Horta", 
  "participative_processes" : [{"usostallermasriera" : [{"nombre":"Un espai per una biblioteca polivalent com espai cultural"}]}],
  "community" : ["Maite"],
  "interests": ["Medio Ambiente"]
  }

user_3 = {
  "_id" : "3",
  "user_name" : "Maite",
  "neighbour" : "Sants", 
  "participative_processes" : [{"usostallermasriera" : [{"nombre":"La Dreta de l'Eixample necessita un Ateneu"}]}],
  "community" : ["Inma"],
  "interests": ["Educación"]
  }

user_4 = {
  "_id" : "4",
  "user_name" : "Jerónimo",
  "neighbour" : "Sant Andreu", 
  "participative_processes" : [{}],
  "community" : ["Victor"],
  "interests": []
  }




dbname = get_database()
collection_name = dbname["users_list"]
collection_name.delete_many({}) #clean the collection
collection_name.insert_many([user_1,user_2,user_3])
# collection_name.insert_one(item_3)