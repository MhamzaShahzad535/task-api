from fastapi import APIRouter

router = APIRouter(
    prefix="/public",
    tags=["Public"]
)

@router.get("/info")
def public_info():
    return {
        "message": "welcome strangerthis info is public"
    }