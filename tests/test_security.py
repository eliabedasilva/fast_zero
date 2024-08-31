from jwt import decode

from fast_zero.security import create_acess_token, settings


def test_jwt():
    data = {"sub": "teste@test.com"}
    token = create_acess_token(data)

    result = decode(
        token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
    )

    assert result["sub"] == data["sub"]
    assert result["exp"]
