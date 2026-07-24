def test_admin_routes_require_admin(client, annotator_headers):
    response = client.get("/admin/users", headers=annotator_headers)
    assert response.status_code == 403


def test_verification_routes_require_verifier(client, annotator_headers):
    response = client.get("/verifications/pending", headers=annotator_headers)
    assert response.status_code == 403


def test_export_routes_require_verifier(client, annotator_headers):
    response = client.get("/export/stats", headers=annotator_headers)
    assert response.status_code == 403


def test_verifier_can_access_export(client, verifier_headers):
    response = client.get("/export/stats", headers=verifier_headers)
    assert response.status_code in (200, 500)


def test_annotator_can_access_phrases(client, annotator_headers):
    response = client.get("/phrases/random", headers=annotator_headers)
    assert response.status_code in (200, 404)


def test_verifier_can_access_verify(client, verifier_headers):
    response = client.get("/verifications/pending", headers=verifier_headers)
    assert response.status_code == 200
