
from fastapi import APIRouter
from app.api.users.users import router as users_router
router = APIRouter()

router.include_router(users_router, prefix="/api/auth", tags=["Users"])

