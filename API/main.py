from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI
from pydantic import BaseModel
from sql_to_json import get_json
from pin_match import run_metaflow

class userInput(BaseModel):
    # Define your data structure here
    query: str
    email: str
    bucket: str
    file_path: str
    download: bool


class PinMatchInput(BaseModel):
    year: int
    month: int
    db: str
    schm: str
    s3: str
    prefix: str

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


@app.post("/pinmatch")
async def pinmatch(cliArgs:PinMatchInput):
    cliArgs = cliArgs.dict()
    command = [
        "python3", "pin_match/pl_pin_match.py",
        "--environment=pypi",
        "run",
        f"--year={cliArgs['year']}",
        f"--month={cliArgs['month']}",
        f"--db={cliArgs['db']}",
        f"--schema={cliArgs['schm']}",
        f"--s3={cliArgs['s3']}",
        f"--prefix={cliArgs['prefix']}"
    ]
    output = run_metaflow(command )
    payload = {}
    payload['flow_status_link'] = f"https://metaflow.ml.bestegg.com/PLPinMatch/{output['run_id']}"
    payload['message'] = output['message']
    return payload

app.mount("/", StaticFiles(directory="dist", html=True), name="static")