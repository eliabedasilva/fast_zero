from http import HTTPStatus


def test_read_root_deve_retornar_ok_e_hello_world(client):
    response = client.get("/")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"message": "Hello world!"}


def test_create_user(client):
    response = client.post(
        "/users/",
        json={
            "username": "name",
            "password": "pass",
            "email": "email@gmail.com",
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        "username": "name",
        "email": "email@gmail.com",
        "id": 1,
    }


def test_read_users(client):
    response = client.get("/users/")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "users": [
            {
                "username": "name",
                "email": "email@gmail.com",
                "id": 1,
            }
        ]
    }


def test_update_user(client):
    response = client.put(
        "/users/1",
        {
            "username": "name",
            "email": "email@gmail.com",
            "password": "senha",
            "id": 1,
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "username": "name",
        "email": "email@gmail.com",
        "password": "senha",
        "id": 1,
    }


def test_delete_user(client):
    response = client.delete("/users/1")
    assert response.json() == {"message": "User deleted"}


def test_get_user_by_id(client):
    response = client.get("/users/1")
    assert response.status_code == HTTPStatus.ok
    assert response.json() == {
        "username": "name",
        "email": "email@gmail.com",
        "id": 1,
    }
