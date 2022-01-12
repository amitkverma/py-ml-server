from fastapi import FastAPI
from pydantic import BaseModel
import app.core.mnc.index as MNC

app = FastAPI()

class Claim(BaseModel):
    metaData: dict
    diagnosisList: list
    activityList: list
    priorAuthorization: dict
    observationDetails: dict


@app.post('/validateClaim')
async def validateClaim(claimData:Claim):
    response = await MNC.validateClaim(claimData)
    return response

