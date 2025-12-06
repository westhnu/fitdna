"""
인증 관련 API 엔드포인트
- 회원가입, 로그인, 로그아웃
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()


@router.post("/register")
async def register():
    """회원가입"""
    return {"message": "회원가입 엔드포인트 (구현 예정)"}


@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """로그인"""
    return {
        "access_token": "sample_token",
        "token_type": "bearer",
        "message": "로그인 엔드포인트 (구현 예정)",
    }


@router.post("/logout")
async def logout():
    """로그아웃"""
    return {"message": "로그아웃 엔드포인트 (구현 예정)"}


@router.get("/me")
async def get_current_user():
    """현재 로그인한 사용자 정보"""
    return {"message": "사용자 정보 조회 엔드포인트 (구현 예정)"}
