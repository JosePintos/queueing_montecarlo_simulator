from fastapi import FastAPI
import utils


app = FastAPI()


@app.get("/")
def start_server():
    return utils.runSimulation(horasASimular=0.5)
