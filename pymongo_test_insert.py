# Get the database using the method we defined in pymongo_test_insert file
from pymongo_get_database import get_database

dbname = get_database()
collection_name = dbname["users_list"]

user_1 = {
  "_id" : "1",
  "user_name" : "Victor",
  "neighbor" : "Nou Barris"
  }
user_2 = {
  "_id" : "2",
  "user_name" : "Inma",
  "neighbor" : "Horta"
  }
user_3 = {
  "_id" : "3",
  "user_name" : "Maite",
  "neighbor" : "Sants"
  }

# DARÁ ERROR SI YA EXISTEN LOS USERS
collection_name.insert_many([user_1,user_2,user_3])
# collection_name.insert_one(item_3)