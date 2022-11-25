from fastapi import APIRouter
from .accounts import router as accounts_router
from postgres_air.api.auth import router as auth_router


router = APIRouter()
router.include_router(accounts_router)
router.include_router(auth_router)
