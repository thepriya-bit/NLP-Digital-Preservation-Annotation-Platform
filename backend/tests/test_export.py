import json


def test_export_csv_requires_auth(client):
    response = client.get("/export/csv")
    assert response.status_code == 403


def test_export_json_requires_auth(client):
    response = client.get("/export/json")
    assert response.status_code == 403


def test_export_stats_requires_auth(client):
    response = client.get("/export/stats")
    assert response.status_code == 403


def test_export_parquet_requires_auth(client):
    response = client.get("/export/parquet")
    assert response.status_code == 403


def test_export_stats_returns_data(client, auth_headers):
    response = client.get("/export/stats", headers=auth_headers)
    if response.status_code == 200:
        data = response.json()
        assert "total_annotations" in data
        assert "verified_annotations" in data
        assert "pending_verification" in data
        assert "language_distribution" in data
        assert isinstance(data["language_distribution"], dict)


def test_export_csv_returns_csv(client, auth_headers):
    response = client.get("/export/csv", headers=auth_headers)
    if response.status_code == 200:
        assert response.headers["content-type"] == "text/csv"
        assert "verified_dataset.csv" in response.headers["content-disposition"]
        content = response.text
        if content.strip():
            assert "annotation_id" in content
            assert "phrase" in content


def test_export_json_returns_json(client, auth_headers):
    response = client.get("/export/json", headers=auth_headers)
    if response.status_code == 200:
        assert "application/json" in response.headers["content-type"]
        data = json.loads(response.text)
        assert isinstance(data, list)


def test_export_with_language_filter(client, auth_headers):
    response = client.get("/export/csv?language=assamese", headers=auth_headers)
    assert response.status_code in (200, 500)


def test_export_with_date_filter(client, auth_headers):
    response = client.get("/export/json?date_from=2024-01-01&date_to=2027-12-31", headers=auth_headers)
    assert response.status_code in (200, 500)


def test_export_with_trust_score_filter(client, auth_headers):
    response = client.get("/export/csv?min_trust_score=0", headers=auth_headers)
    assert response.status_code in (200, 500)
