'''平台'''

from fastapi import APIRouter

router = APIRouter()

@router.get("/",summary="說明",description="詳細敘述")
async def hello():
    return {"Hello": "world"}