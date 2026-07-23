from fastapi import APIRouter, Depends, HTTPException, status, Form
from mawaqit.schemas.admin import AdminLogin, AdminUpdate, Token
from mawaqit.services.admin import AdminService
from mawaqit.api.deps import get_admin_service, get_current_admin
from mawaqit.models.admin import Admin

router = APIRouter(prefix="/admin", tags=["admin"])

@router.post("/login", response_model=Token)
async def login(
    username: str = Form(...),
    password: str = Form(...),
    service: AdminService = Depends(get_admin_service)
):
    admin = await service.repo.get_by_username(username)
    if not admin or not service.verify_password(password, admin.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"access_token": service.create_token(admin.username), "token_type": "bearer"}

@router.patch("/me")
async def update_me(
    update: AdminUpdate,
    current: Admin = Depends(get_current_admin),
    service: AdminService = Depends(get_admin_service)
):
    if update.username:
        existing = await service.repo.get_by_username(update.username)
        if existing and existing.username != current.username:
            raise HTTPException(status_code=400, detail="Username already taken")
        current.username = update.username
    if update.password:
        current.password_hash = service.hash_password(update.password)
    await service.repo.session.commit()
    await service.repo.session.refresh(current)
    return {"message": "Updated successfully", "username": current.username}