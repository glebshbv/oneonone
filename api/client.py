import os
from dotenv import load_dotenv
import fastapi
from fastapi import Header, Depends, HTTPException
from starlette import status

router = fastapi.APIRouter()
load_dotenv()


def verify_token(x_token: str = Header(...)):
    if x_token != os.getenv('API_TOKEN'):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )


@router.get("/", dependencies=[Depends(verify_token)])
async def root():
    return {"message": "Hello World"}