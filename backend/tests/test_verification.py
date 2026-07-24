import pytest


def test_create_annotation_for_verification(client, annotator_headers, auth_headers):
    phrase_resp = client.post(
        "/phrases",
        json={
            "phrase": "পৰীক্ষাৰ বাবে এটা বাক্য",
            "language": "assamese",
            "status": "submitted",
        },
        headers=annotator_headers,
    )
    assert phrase_resp.status_code in (201, 422)

    if phrase_resp.status_code == 201:
        phrase_id = phrase_resp.json()["id"]
        ann_resp = client.post(
            "/annotations",
            json={
                "raw_phrase_id": phrase_id,
                "translated_text": "A sentence for testing",
            },
            headers=annotator_headers,
        )
        assert ann_resp.status_code == 201
        annotation_id = ann_resp.json()["id"]

        vote_resp = client.post(
            "/verifications",
            json={"annotation_id": annotation_id, "vote": "approve"},
            headers=auth_headers,
        )
        assert vote_resp.status_code == 201
        result = vote_resp.json()
        assert result["success"] is True


def test_duplicate_vote_prevented(client, annotator_headers, auth_headers):
    phrase_resp = client.post(
        "/phrases",
        json={"phrase": "দ্বিতীয় পৰীক্ষাৰ বাবে", "language": "assamese", "status": "submitted"},
        headers=annotator_headers,
    )
    if phrase_resp.status_code != 201:
        return

    ann_resp = client.post(
        "/annotations",
        json={"raw_phrase_id": phrase_resp.json()["id"], "translated_text": "Second test"},
        headers=annotator_headers,
    )
    if ann_resp.status_code != 201:
        return

    ann_id = ann_resp.json()["id"]

    client.post(
        "/verifications",
        json={"annotation_id": ann_id, "vote": "approve"},
        headers=auth_headers,
    )

    dup_resp = client.post(
        "/verifications",
        json={"annotation_id": ann_id, "vote": "approve"},
        headers=auth_headers,
    )
    assert dup_resp.status_code == 409


def test_self_vote_prevented(client, annotator_headers):
    phrase_resp = client.post(
        "/phrases",
        json={"phrase": "নিজৰ বাক্য", "language": "assamese"},
        headers=annotator_headers,
    )
    if phrase_resp.status_code != 201:
        return

    ann_resp = client.post(
        "/annotations",
        json={"raw_phrase_id": phrase_resp.json()["id"], "translated_text": "Own translation"},
        headers=annotator_headers,
    )
    if ann_resp.status_code != 201:
        return

    ann_id = ann_resp.json()["id"]
    vote_resp = client.post(
        "/verifications",
        json={"annotation_id": ann_id, "vote": "approve"},
        headers=annotator_headers,
    )
    assert vote_resp.status_code == 409
