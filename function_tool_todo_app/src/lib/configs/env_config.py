from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("OPEN_ROUTER_KEY")
base_url = os.getenv("OPEN_ROUTER_BASE_URL")
mongo_uri = os.getenv("MONGO_URI")  
model_name = os.getenv("MODEL_NAME")