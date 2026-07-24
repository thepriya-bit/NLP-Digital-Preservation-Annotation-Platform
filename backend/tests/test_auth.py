def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_register(client):
    response = client.post(
        "/auth/register",
        json={
            "username": "newuser",
            "email": "new@test.com",
            "password": "securepass",
            "role": "annotator",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert "access_token" in data
    assert data["user"]["username"] == "newuser"
    assert data["user"]["role"] == "annotator"
    assert "is_banned" in data["user"]
    assert data["user"]["is_banned"] is False


def test_register_duplicate(client):
    response = client.post(
        "/auth/register",
        json={
            "username": "dupuser",
            "email": "dup@test.com",
            "password": "securepass",
            "role": "annotator",
        },
    )
    assert response.status_code == 201

    response = client.post(
        "/auth/register",
        json={
            "username": "dupuser",
            "email": "dupother@test.com",
            "password": "securepass",
            "role": "annotator",
        },
    )
    assert response.status_code == 409


def test_login(client):
    client.post(
        "/auth/register",
        json={
            "username": "loginuser",
            "email": "login@test.com",
            "password": "mypassword",
            "role": "verifier",
        },
    )
    response = client.post(
        "/auth/login",
        json={"username": "loginuser", "password": "mypassword"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["user"]["role"] == "verifier"


def test_login_invalid(client):
    response = client.post(
        "/auth/login",
        json={"username": "nonexistent", "password": "wrongpass"},
    )
    assert response.status_code == 401


def test_get_me(client, auth_headers):
    response = client.get("/auth/me", headers=auth_headers)
    assert response.status_code == 200
    assert "username" in response.json()


def test_get_me_unauthorized(client):
    response = client.get("/auth/me")
    assert response.status_code == 403
