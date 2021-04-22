

from fastapi import Header, HTTPException


async def access_control(x_token: str = Header(...)):
    # check if login

    # check if have permission
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")

