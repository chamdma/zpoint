from fastapi import APIRouter,Request,Body,Depends
from models.zpoint_model import ZPointCollection




from utils import  jwt_bearer_auth

from datetime import datetime


router=APIRouter()




@router.post("/zpoint/set/create")
async def create_point(
    request:Request,
    point_set_name:str=Body(...),
    price: float=Body(...),
    points: int=Body(...),
    is_adjustable:bool=Body(...),
    image:str=Body(...)
                        
                        
                        
                        
                        
                        
):
    
    status = True
    created_at = datetime.now()
    updated_at = datetime.now()

   

    if ZPointCollection.objects(point_set_name=point_set_name).first():
        return {
                "status_code": 400,
                "description": "Point set name already exists",
                "status": False,
                "data": [],
            }
    
    try:
        new_point_set =ZPointCollection(
            point_set_name=point_set_name,
            price=price,
            points=points,
            image=image,
            is_adjustable=is_adjustable,
            status=status,
            created_at = datetime.utcnow(),
            updated_at = datetime.utcnow()
        )
         

        new_point_set.save()



        point_data = new_point_set.to_mongo()
        point_data.pop("_id", None)  
        point_data["created_at"] = point_data["created_at"].isoformat(timespec='seconds') + "Z"
        point_data["updated_at"] = point_data["updated_at"].isoformat(timespec='seconds') + "Z"

        return {
            "status": True,
            "status_code": 200,
            "description": "Point collection created successfully",
            "data": [point_data], 
        }

    except Exception as e:
        return {
            "status": False,
            "status_code": 500,
            "description": f"Error creating point collection: {str(e)}",
            "data": [],
            "error": str(e),
        }
    




















@router.post("/zpoints/set/list")
async def list_point(
    request: Request,
    token_data: dict = Depends(jwt_bearer_auth),
    user_id: str = Body("", embed=True)  
):
    try:
       
        point_sets = ZPointCollection.objects(status=True)

      
        data = [
            {
                "point_set_name": point.point_set_name,
                "price": point.price,
                "points": point.points,
                "image": point.image,
                "is_adjustable": point.is_adjustable,
                "created_at": point.created_at.isoformat(timespec='seconds') + "Z",
                "updated_at": point.updated_at.isoformat(timespec='seconds') + "Z",
                "status": point.status
            }
            for point in point_sets
        ]

        return {
            "status": True,
            "status_code": 200,
            "description": "Point collection list fetched successfully",
            "data": data
        }

    except Exception as e:
        return {
            "status": False,
            "status_code": 500,
            "description": f"Error fetching point collection: {str(e)}",
            "data": []
        }
    

@router.post("/zpoint/set/edit")
async def edit_point(
    request:Request,
    token_data: dict = Depends(jwt_bearer_auth),
    id:str=Body("",embed=True),
    point_set_name:str=Body(...),
    price:float=Body(...),
    points:int=Body(...),
    is_adjustable:bool=Body(...)
):
    try:
        point_set=ZPointCollection.objects(point_set_name=point_set_name).first()


        point_set.point_set_name=point_set_name
        point_set.price = price
        point_set.points=points
        point_set.is_adjustable=is_adjustable

        point_set.save()


        response_data={
            "id": str(point_set.id),
            "point_set_name":str(point_set.point_set_name),
            "price":float(point_set.price),
            "points":int(point_set.points),
            "is_adjustable":bool(point_set.is_adjustable)    
            }
        return {
            "status": True,
            "status_code": 200,
            "description": "Point collection edited successfully",
            "data": [response_data]
        }

    except Exception as e:
        return {
            "status": False,
            "status_code": 500,
            "description": f"Error editing point collection: {str(e)}",
            "data": [],
            "error": str(e)
        }