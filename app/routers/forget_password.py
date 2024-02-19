from fastapi import APIRouter, Depends, HTTPException, status
from starlette.responses import JSONResponse
from fastapi_mail import FastMail, MessageSchema, MessageType, ConnectionConfig
import datetime
import jwt
import os
from app.database import User
from app.model.forget_password import (
    ForgetPasswordRequest,
    ResetForegetPassword,
    SuccessMessage,
)
from dotenv import load_dotenv
from passlib.context import CryptContext
import traceback

load_dotenv()

router = APIRouter()

FORGET_PWD_SECRET_KEY = os.getenv("FORGET_PWD_SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
HOST_APP = os.getenv("CLIENT_ORIGIN")
FORGET_PASSWORD_URL = os.getenv("FORGET_PASSWORD_URL")
MAIL_FROM_NAME = os.getenv("MAIL_FROM_NAME")
FORGET_PASSWORD_LINK_EXPIRE_MINUTES = os.getenv("FORGET_PASSWORD_LINK_EXPIRE_MINUTES")
MAIL_USERNAME = os.getenv("MAIL_USERNAME")
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
MAIL_FORM = os.getenv("MAIL_FORM")

conf = ConnectionConfig(
    MAIL_USERNAME=MAIL_USERNAME,
    MAIL_PASSWORD=MAIL_PASSWORD,
    MAIL_FROM=MAIL_FORM,
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
)


def create_reset_password_token(email: str):
    data = {
        "sub": email,
        "exp": datetime.datetime.now() + datetime.timedelta(minutes=10),
    }
    token = jwt.encode(data, FORGET_PWD_SECRET_KEY, ALGORITHM)
    string = token.decode()
    cleaned_string = string.replace("b'", "").replace("'", "")
    return cleaned_string


@router.post("/forget-password")
async def forget_password(fpr: ForgetPasswordRequest):
    try:
        user = User.find_one({"email": fpr.email})
        if user is None:
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content="Invalid Email address",
            )

        secret_token = create_reset_password_token(email=fpr.email)

        forget_url_link = f"{HOST_APP}{FORGET_PASSWORD_URL}/{secret_token}"

        email_body = f"From: {MAIL_FROM_NAME}\nReset_link: {forget_url_link}"

        print(email_body)

        message = MessageSchema(
            subject="Password Reset Instructions",
            recipients=[fpr.email],
            template_body=email_body,
            subtype=MessageType.html,
        )

        template_name = "mail/password_reset.html"

        fm = FastMail(conf)
        await fm.send_message(message, template_name)

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "message": "Email has been sent",
                "success": True,
                "status_code": status.HTTP_200_OK,
            },
        )
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Something Unexpected, Server Error - {e}",
        )


def decode_reset_password_token(token: str):
    try:
        payload = jwt.decode(token, FORGET_PWD_SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        return email
    except Exception as e:
        return None


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/reset-password", response_model=SuccessMessage)
async def reset_password(rfp: ResetForegetPassword):
    try:
        info = decode_reset_password_token(token=rfp.secret_token)
        if info is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Invalid Password Reset Payload or Reset Link Expired",
            )
        if rfp.new_password != rfp.confirm_password:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="New password and confirm password are not same.",
            )

        hashed_password = pwd_context.hash(rfp.new_password)
        User.update_one({"email": info}, {"$set": {"password": hashed_password}})
        return {
            "success": True,
            "status_code": status.HTTP_200_OK,
            "message": "Password Rest Successfull!",
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Some thing unexpected happened! - {e}",
        )
