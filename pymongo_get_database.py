from pymongo.mongo_client import MongoClient
import certifi

def get_database():
 
   uri = "mongodb+srv://vicllin7:smU7k7KwMMkdfmJl@clustertfg.kaowwhz.mongodb.net/"
   # Create a new client and connect to the server
   client = MongoClient(uri, tlsCAFile=certifi.where())
   # Send a ping to confirm a successful connection
   try:
      client.admin.command('ping')
      print("Pinged your deployment. You successfully connected to MongoDB!")
   except Exception as e:
      print(e)
 
   # Create the database for our example (we will use the same database throughout the tutorial
   return client['tfg_DataBase']
  
# This is added so that many files can reuse the function get_database()
if __name__ == "__main__":   
  
   # Get the database
   dbname = get_database()






   