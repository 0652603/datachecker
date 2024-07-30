from fastapi import APIRouter

router = APIRouter()

@router.get("/{name}",summary="輸入名字",description="輸入名字(文字格式)")
async def hello(name:str):
    first = [(3*x)+1 for x in range(334)]
    second = [(10*x)+1 for x in range(101)]
    checker = 0
    for i in first :
        for j in second:
            if i == j :
                checker +=1
                continue

    return {"Hello": name, "count" : checker}
