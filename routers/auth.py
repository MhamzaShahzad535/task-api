from fastapi import APIRouter, HTTPException, status

from schemas import UserSignup, UserLogin
from supabase_client import supabase

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/signup", status_code=status.HTTP_201_CREATED)
def signup(user: UserSignup):

    try:
        response = supabase.auth.sign_up(
            {
                "email": user.email,
                "password": user.password
            }
        )

        return response

    except Exception as e:
        print("SIGNUP ERROR:", e)

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


@router.post("/login")
def login(user: UserLogin):

    try:
        response = supabase.auth.sign_in_with_password(
            {
                "email": user.email,
                "password": user.password
            }
        )

        return response

    except Exception as e:
        print("LOGIN ERROR:", e)

        raise HTTPException(
            status_code=401,
            detail=str(e)
        )