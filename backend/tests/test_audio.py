import io


def test_audio_upload_requires_auth(client):
    response = client.post("/audio/upload")
    assert response.status_code == 403


def test_audio_upload_invalid_content_type(client, annotator_headers):
    response = client.post(
        "/audio/upload",
        files={"file": ("test.txt", io.BytesIO(b"not audio"), "text/plain")},
        headers=annotator_headers,
    )
    assert response.status_code == 400
    assert "audio" in response.json()["detail"].lower()


def test_audio_upload_valid(client, annotator_headers):
    response = client.post(
        "/audio/upload",
        files={"file": ("test.webm", io.BytesIO(b"fake audio data"), "audio/webm")},
        headers=annotator_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert "audio_url" in data
    assert "filename" in data
    assert data["filename"].endswith(".webm")


def test_audio_upload_mp3(client, annotator_headers):
    response = client.post(
        "/audio/upload",
        files={"file": ("test.mp3", io.BytesIO(b"fake mp3"), "audio/mpeg")},
        headers=annotator_headers,
    )
    assert response.status_code == 200


def test_audio_upload_wav(client, annotator_headers):
    response = client.post(
        "/audio/upload",
        files={"file": ("test.wav", io.BytesIO(b"fake wav"), "audio/wav")},
        headers=annotator_headers,
    )
    assert response.status_code == 200


def test_audio_upload_large_file(client, annotator_headers):
    large_data = b"x" * (60 * 1024 * 1024)
    response = client.post(
        "/audio/upload",
        files={"file": ("large.webm", io.BytesIO(large_data), "audio/webm")},
        headers=annotator_headers,
    )
    assert response.status_code == 413


def test_audio_upload_empty_file(client, annotator_headers):
    response = client.post(
        "/audio/upload",
        files={"file": ("empty.webm", io.BytesIO(b""), "audio/webm")},
        headers=annotator_headers,
    )
    assert response.status_code == 200
    assert "audio_url" in response.json()
