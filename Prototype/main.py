import ray
import random
from fastapi import FastAPI
from ray import serve

app = FastAPI()


@serve.deployment(route_prefix="/landing-spot")
class LandingSpotInference:
    def __init__(self):
        self.someState = 0

    @app.get("/predict")
    async def get(self, images: str):
        print("Performing prediction for images {0}".format(images))
        prediction = random.uniform(0, 1)
        return {"prediction": prediction}


@app.post("/deploy")
async def deploy_landing_spot(version: int):
    LandingSpotInference.options(
        version=str(version),
        num_replicas=1,
        ray_actor_options={"num_gpus": 0}
    ).deploy()
    return {"Successfully deployed landing spot model version {0}": version}


@app.on_event("startup")  # Code to be run when the server starts.
async def startup_event():
    ray.init(address="auto", namespace="serve")  # Connect to the running Ray cluster.
    print("Starting...")
    await deploy_landing_spot(0)
