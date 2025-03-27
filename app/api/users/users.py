from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.database.connection import db
from app.models.user_model import UserCreate, UserLogin
from app.api.users.user_service import hash_password, verify_password, create_access_token, verify_access_token
from datetime import timedelta
from bson import ObjectId

security = HTTPBearer()
router = APIRouter()

def str_object_id(obj):
    return str(obj) if isinstance(obj, ObjectId) else obj

@router.post("/register")
async def register_user(user: UserCreate):
    if db["users"].find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="Email already registered")

    db["users"].insert_one({
        "username": user.username,
        "email": user.email,
        "password": hash_password(user.password),
        "phone": user.phone
    })
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
        "token_type": "bearer"
    }

@router.get("/me")
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    email = verify_access_token(credentials.credentials)
    user_data = db["users"].find_one({"email": email})
    
    if not user_data:
        raise HTTPException(status_code=404, detail="User not found")
    
    user_data = {key: str_object_id(value) for key, value in user_data.items()}
    user_data.pop("password", None)

    return {"user": user_data}