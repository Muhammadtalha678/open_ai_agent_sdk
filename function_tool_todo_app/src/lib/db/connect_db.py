from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pymongo.errors import ConnectionFailure


class ConnectDb:
    def __init__(self,uri):
          self.uri = uri
          self.client = None
    async def connection(self):
        # print(self.uri)
        self.client = MongoClient(self.uri,server_api=ServerApi('1'))
        try:
            self.client.admin.command('ping')
            print("Pinged your deployment. You successfully connected to MongoDB!")
            return True
        except ConnectionFailure as e:
            print("Error in db",e)
            raise Exception(f"Error whie connecting db:{e}")
    async def close_connection(self):
        if self.client:
            self.client.close()
            
    async def get_database(self):
        return self.client['agent_db']

