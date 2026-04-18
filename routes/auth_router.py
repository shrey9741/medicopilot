from fastapi import APIRouter, HTTPException, status, Depends
from auth.jwt_handler import create_access_token, verify_password
from auth.middleware import get_current_doctor
from auth.models import LoginRequest, TokenResponse
from auth.registry import DOCTORS

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login", response_model=TokenResponse)
async def login(request: LoginRequest):
    doctor = DOCTORS.get(request.username)
    if not doctor or not verify_password(request.password, doctor["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )
    token = create_access_token({
        "sub": request.username,
        "name": doctor["name"],
        "role": doctor["role"],
    })
    return TokenResponse(
        access_token=token,
        doctor_name=doctor["name"],
        role=doctor["role"],
    )

@router.get("/me")
async def get_me(doctor: dict = Depends(get_current_doctor)):
    return {
        "username": doctor.get("sub"),
        "name": doctor.get("name"),
        "role": doctor.get("role"),
    }

@router.post("/logout")
async def logout():
    return {"message": "Logged out. Delete your token on the client."}