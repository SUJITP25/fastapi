from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from schema.user_schema import UserCreateModel, UserModel, UserLoginModel
from services.user_service import UserService
from db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from models.user_model import User
from utils.utils import cerate_access_token, decode_token, verify_password
from datetime import datetime, timedelta

auth_router = APIRouter()
user_service = UserService()


@auth_router.post(
    "/signup", response_model=UserModel, status_code=status.HTTP_201_CREATED
)
async def create_user_account(
    user_data: UserCreateModel, session: AsyncSession = Depends(get_session)
):
    email = user_data.email

    user_exits = await user_service.user_exist(email, session)

    if not user_exits:
        new_user = await user_service.create_user(user_data, session)
        return new_user
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Email Already Exists"
        )


# JWT conatins three parts, the header ,payload and signature. In order, these are seperated by a period sign.


@auth_router.post("/login", response_model=UserLoginModel)
async def user_login(
    login_data: UserLoginModel, session: AsyncSession = Depends(get_session)
):
    email = login_data.email
    password = login_data.password

    user_exists = await user_service.user_exist(email, session)

    if user_exists:
        is_password_valid = verify_password(password, user_exists.password)

        if is_password_valid:
            access_token = cerate_access_token(
                user_data={"email": user_exists.email, "user_uid": str(user_exists.uid)}
            )

            refresh_token = cerate_access_token(
                user_data={
                    "email": user_exists.email,
                    "user_uid": str(user_exists.uid),
                },
                refresh=True,
                expiry=timedelta(days=2),
            )

            return JSONResponse(
                content={
                    "message": "Login Successful",
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "user": {
                        "user_email": user_exists.email,
                        "user_id": user_exists.uid,
                    },
                },
                status_code=status.HTTP_200_OK,
            )
        else:
            raise HTTPException(
                status=status.HTTP_404_NOT_FOUND, detail="Invalid Credentials"
            )
    else:
        raise HTTPException(status=status.HTTP_404_NOT_FOUND, detail="User Not Found")
