from sqlalchemy import select

from fast_zero.models import User


def test_create_user(session):
    user = User(
        username="Eliabe",
        email="eliabe@g.com",
        password="senha",
    )
    session.add(user)
    session.commit()

    result = session.scalar(select(User).where(User.email == "eliabe@g.com"))

    assert result.username == "Eliabe"
