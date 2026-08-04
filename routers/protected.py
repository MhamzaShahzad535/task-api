from fastapi import APIRouter, Depends

from dependencies.auth import get_current_user


router = APIRouter(
    prefix="/protected",
    tags=["Protected"]
)


@router.get("/profile")
def get_profile(user = Depends(get_current_user)):

    return {
        "message": "Protected profile",
        "user": user
    }