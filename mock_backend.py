from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
import requests
import asyncio
import traceback
import json
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

DUMMY_URL = "https://cs145-iot-cup-1745973870.ap-southeast-1.elb.amazonaws.com"

class VerifyRequest(BaseModel):
    uid: str
    dob: str

class LogRequest(BaseModel):
    message: str

app = FastAPI()

API_KEY = "39983"

def send_post_request(uid, consent, dob):
    response = requests.post(
        f"{DUMMY_URL}/api/v1/auth/yes-no",
        json={
            "individual_id": uid,
            "consent": consent,
            "dob": dob
        },
        verify = False
    )

    return response

@app.post("/verify")
async def verify(payload: VerifyRequest, x_api_key: str = Header(None)):
    try:
        if x_api_key != API_KEY:
            raise HTTPException(status_code=401, detail="Unauthorized")

        
        print("\033[34mPAYLOAD\033[0m:", payload)

        loop = asyncio.get_event_loop()

        try:

            response = await asyncio.wait_for(
                loop.run_in_executor(None, send_post_request, payload.uid, True, payload.dob),
                timeout=60.0
            )

            response_body = response.json()
            print("\033[34mMOSIP RESPONSE\033[0m:", json.dumps(response_body, indent=2))
        
            if (not response_body['response']['authStatus']):
                print("\033[31mINVALID NATIONAL ID\033[0m")
                return { "authorized": False }

            print("\033[32mVALID NATIONAL ID\033[0m")

        except asyncio.TimeoutError:
            print("\033[31mERROR: MOSIP timed out, falling back to DB query\033[31m")

        # 2. Query PWD database
        pwd_res = requests.post(
            "https://iot-cup-connection-db-worker.jrbuizon.workers.dev",
            json={"userId": payload.uid},
            headers={
                "Content-Type": "application/json"
            }
        )
        data = pwd_res.json()
        if (not data["exists"]):
            print("\033[31mINVALID PWD\033[0m")
            return { "authorized": False }
        print("\033[32mVALID PWD\033[0m")
        # 3. Return result to ESP32
        return { "authorized": True }
    except HTTPException:
        raise
    except Exception as e:
        print("\033[31mERROR\033[0m: ", str(e))
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/log")
async def message(payload: LogRequest, x_api_key: str = Header(None)):
    try:
        if x_api_key != API_KEY:
            raise HTTPException(status_code=401, detail="Unauthorized")
        print("\033[34mLOG\033[0m: ", payload.message)
        return { "received": True, "message": payload.message }

    except HTTPException:
        raise
    except Exception as e:
        print("\033[31mERROR\033[0m: ", str(e))
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
