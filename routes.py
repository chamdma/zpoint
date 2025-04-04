from fastapi import APIRouter,Request,Body
from models import ZPointCollection
from utils import decode_jwt_token, create_access_token
from datetime import datetime
import database

router=APIRouter()


@router.post("/auth/token")
async def generate_token():
    token = create_access_token({"user": "user123"}) 
    return {
        "status": True,
        "status_code": 200,
        "description": "Token generated successfully",
        "token": token
    }




@router.post("/zpoint/set/create")
async def create_zpoint(
    request:Request,
    point_set_name:str=Body(...),
    price: float=Body(...),
    points: int=Body(...),
    is_adjustable:bool=Body(...)
                        
                        
                        
                        
                        
                        
):
    image = "https://default-image-url.com"
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
async def list_zpoint(
    request: Request,
    user_id: str = Body("", embed=True)  
):
    try:
       
        token = request.headers.get("Authorization", "").replace("Bearer ", "")
        payload = decode_jwt_token(token)
        
        print("Decoded Payload:", payload)


    

       
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