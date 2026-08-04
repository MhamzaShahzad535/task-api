from fastapi import APIRouter, HTTPException, status, Depends

from schemas import UserSignup, UserLogin
from dependencies.auth import get_current_user
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
            detail="Invalid login credentials"
        )


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(user=Depends(get_current_user)):

    try:
        supabase.auth.sign_out()

        return None

    except Exception as e:
        print("LOGOUT ERROR:", e)

        raise HTTPException(
            status_code=400,
            detail="Logout failed"
        )