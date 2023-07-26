from google.cloud.sql import connector
from decouple import config
from dotenv import load_dotenv
import os

load_dotenv()
dbase = os.getenv("dbase")
duser = os.getenv("duser")
dpw = os.getenv("dpw")
# Replace dip with your instance connection name
dip = os.getenv("dip")

# Define a function to open database connection
def open_db_connection(db_name, user, password):
    # Try to connect to the database
    try:
        # Create a connection object using the connector.connect function
        mydb = connector.connect(
            dip,
            user,
            password,
            db_name,
            enable_iam_auth=True
        )
        # Print a success message
        print("Opened connection to database:", db_name)
        # Return the connection object
        return mydb
    # Handle any exceptions
    except Exception as e:
        # Print an error message
        print("Failed to open connection to database:", e)
        # Return None
        return None

# Define a function to close database connection
def close_db_connection(mydb, db_name):
    # Check if the connection object exists
    if mydb:
        # Try to close the connection
        try:
            # Close the connection
            mydb.close()
            # Print a success message
            print("Closed connection to database:", db_name)
        # Handle any exceptions
        except Exception as e:
            # Print an error message
            print("Failed to close connection to database:", e)



def defineDB():
   mydb=open_db_connection(
       dbase,
       duser,
       dpw,
   )
   return mydb

