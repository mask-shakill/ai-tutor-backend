from fastapi import APIRouter, HTTPException
from app.database.connection import db
from app.api.users.user_service import hash_password, verify_password, create_access_token
from app.models.user_model import UserCreate, UserLogin
from datetime import timedelta
from bson import ObjectId

router = APIRouter()
def str_object_id(obj):
    if isinstance(obj, ObjectId):
        return str(obj)
    return obj

@router.post("/register")
async def register_user(user: UserCreate):
    if db["users"].find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="Email already registered")

    user_data = {
        "username": user.username,
        "email": user.email,
        "password": hash_password(user.password), 
        "phone": user.phone
    }

    db["users"].insert_one(user_data)
    return {"status": True, "message": "User registered successfully"}
@router.post("/login")
async def login_user(user: UserLogin):
    user_data = db["users"].find_one({"email": user.email})
    
    if not user_data or not verify_password(user.password, user_data["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": user_data["email"]}, expires_delta=timedelta(minutes=30))
    
    user_data = {key: str_object_id(value) for key, value in user_data.items()}
    user_data.pop("password", None)

    return {
        "status": True,
        "message": "Login successful",
        "user": user_data, 
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": 1800  
    }
