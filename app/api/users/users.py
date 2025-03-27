from fastapi import APIRouter, HTTPException, Depends
from app.database.connection import db
from app.models.user_reg_model import UserCreate
from app.api.users.user_service import hash_password, create_access_token

router = APIRouter()

@router.post("/users/register")
async def create_user(user: UserCreate):
    if db["users"].find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="Email already registered")

    user_data = {
        "name": user.name,
        "email": user.email,
        "password": hash_password(user.password),
        "phone": user.phone
    }

    db["users"].insert_one(user_data)
    access_token = create_access_token({"email": user.email})

    return {"message": "User created successfully", "token": access_token}
