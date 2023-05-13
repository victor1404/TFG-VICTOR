from pymongo_get_database import get_database
from pandas import DataFrame

dbname = get_database()
 
# Create a new collection
collection_name = dbname["users_list"]
item_details = collection_name.find()

for item in item_details:
   print(item)
 
# convert the dictionary objects to dataframe
# items_df = DataFrame(item_details)
# print(items_df[])


