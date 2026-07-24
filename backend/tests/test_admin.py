def test_admin_list_users(client, auth_headers):
    response = client.get("/admin/users", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    if data:
        assert "username" in data[0]
        assert "role" in data[0]


def test_admin_get_user(client, auth_headers):
    response = client.get("/admin/users/1", headers=auth_headers)
    assert response.status_code in (200, 404)


def test_admin_get_user_not_found(client, auth_headers):
    response = client.get("/admin/users/99999", headers=auth_headers)
    assert response.status_code == 404


def test_admin_update_user(client, auth_headers):
    response = client.patch(
        "/admin/users/1",
        json={"trust_score": 42.0},
        headers=auth_headers,
    )
    assert response.status_code == 200
    assert response.json()["trust_score"] == 42.0


def test_admin_ban_user(client, annotator_headers, auth_headers):
    response = client.post("/admin/users/2/ban", headers=auth_headers)
    assert response.status_code in (200, 404)


def test_admin_unban_user(client, auth_headers):
    all_users = client.get("/admin/users", headers=auth_headers).json()
    banned = [u for u in all_users if u["is_banned"]]
    if banned:
        uid = banned[0]["id"]
        response = client.post(f"/admin/users/{uid}/unban", headers=auth_headers)
        assert response.status_code == 200
        assert "unbanned" in response.json()["message"].lower()


def test_admin_cannot_ban_self(client, auth_headers):
    me = client.get("/auth/me", headers=auth_headers).json()
    response = client.post(f"/admin/users/{me['id']}/ban", headers=auth_headers)
    assert response.status_code == 400


def test_admin_stats(client, auth_headers):
    response = client.get("/admin/stats", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert "total_users" in data
    assert "total_phrases" in data


def test_admin_dashboard(client, auth_headers):
    response = client.get("/admin/dashboard", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert "recent_users" in data
    assert "recent_annotations" in data


def test_admin_cleanup_orphans(client, auth_headers):
    response = client.post("/admin/cleanup/orphans", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert "orphans_found" in data
    assert "deleted" in data
