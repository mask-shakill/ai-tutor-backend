# app/api/routes.py
from fastapi import APIRouter
from app.api.users.users import router as users_router

# Create the router instance
router = APIRouter()

# Include the users router
router.include_router(users_router)
