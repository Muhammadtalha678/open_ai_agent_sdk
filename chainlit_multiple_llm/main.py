from fastapi import FastAPI
from chainlit.utils import mount_chainlit
app = FastAPI()
@app.get('/cron-job')
def main():
     return {"message":"Hello world"} 
mount_chainlit(app=app,target="chainlit_app.py",path="/")