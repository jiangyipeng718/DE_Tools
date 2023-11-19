from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI
from pydantic import BaseModel
from sql_to_json import get_json

class userInput(BaseModel):
    # Define your data structure here
    query: str
    email: str
    bucket: str
    file_path: str
    download: bool


app = FastAPI()


@app.post("/convertsql")
async def create_item(user_input: userInput):
    user_input = user_input.dict()
    batch_dict = get_json(user_input)
    payload = {}
    if user_input['download']:
        payload['json_data'] = batch_dict
    payload['message'] = "Job is successful!"
    
    return payload

@app.get("/hello")
def read_root():
    return {"Hello": "World"}

app.mount("/", StaticFiles(directory="dist", html=True), name="static")