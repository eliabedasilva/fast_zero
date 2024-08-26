from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import select

from fast_zero.database import get_session
from fast_zero.models import User
from fast_zero.schemas import Message, UserList, UserPublic, UserSchema

app = FastAPI()

database = []


@app.get("/", response_model=Message)
def read_root():
    return {"message": "Hello world!"}


@app.post("/users/", response_model=UserPublic, status_code=HTTPStatus.CREATED)
def create_user(user: UserSchema, session=Depends(get_session)):
    db_user = session.scalar(
        select(User).where(
            (User.username == user.username) | (User.email == user.email)
        )
    )

    if db_user:
        if db_user.username == user.username:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail="Username already exits",
            )

        elif db_user.email == user.email:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail="Email already exits",
            )

    db_user = User(
        username=user.username, password=user.password, email=user.email
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@app.get("/users/", response_model=UserList)
def read_users(limit: int = 10, skip: int = 0, session=Depends(get_session)):
    users = session.scalars(select(User).limit(limit).offset(skip))

    return {"users": users}


@app.put("/users/{user_id}", response_model=UserPublic)
def update_user(user_id: int, user: UserSchema, session=Depends(get_session)):
    db_user = session.scalar(
        select(User).where(User.id == user_id)
    )

    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found!'
        )
    
    db_user.email = user.email
    db_user.username = user.username
    db_user.password = user.password

    session.commit()
    session.refresh(db_user)
    
    return db_user


@app.delete("/users/{user_id}", response_model=Message)
def delete_user(user_id: int, session=Depends(get_session)):
    db_user = session.scalar(
        select(User).where(User.id == user_id)
    )

    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found!'
        )
    session.delete(db_user)
    session.commit()
    return {"message": "User deleted"}


@app.get("/users/{user_id}", response_model=UserPublic)
def get_user_by_id(user_id: int, session=Depends(get_session)):
    db_user = session.scalar(
        select(User).where(User.id == user_id)
    )

    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found!'
        )
    
    return db_user