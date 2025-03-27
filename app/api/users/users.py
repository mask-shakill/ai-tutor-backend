# app/api/users.py
from fastapi import APIRouter, HTTPException
from app.database.connection import db
from app.models.user_reg_model import UserCreate

# Create the router instance
router = APIRouter()

# Endpoint to register a new user
@router.post("/users/")
async def create_user(user: UserCreate):
    # Check if user already exists (using email as the unique identifier)
    existing_user = db["users"].find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Prepare the user data for insertion
    user_data = {
        "email": user.email,
        "password": user.password  # No encryption here, storing plain password
    }

    # Insert the new user into the 'users' collection
    db["users"].insert_one(user_data)
    return {"message": "User created successfully"}
