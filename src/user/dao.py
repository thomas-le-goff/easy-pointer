import uuid

from sqlmodel import Session, select

from .models import User


def get_user_by_id(session: Session, id: str | None) -> User | None:
    if id == None:
        return None
    user = session.exec(select(User).where(
        User.id == uuid.UUID(id))).one_or_none()
    print(user)
    return user


def get_user_by_oauth2_provider_user_id(session: Session, id: str | None) -> User | None:
    if id == None:
        return None
    return session.exec(select(User).where(User.oauth2_provider_user_id == id)).one_or_none()
