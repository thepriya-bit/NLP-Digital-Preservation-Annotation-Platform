import json
from sqlalchemy import create_engine, text

DATABASE_URL = 'postgresql://postgres:password@localhost:5432/nlp_platform'
engine = create_engine(DATABASE_URL)

with engine.begin() as conn:
    # Create a sample user if missing
    user_result = conn.execute(
        text("SELECT id FROM users WHERE username = :username"),
        {"username": "assamese_annotator"},
    ).fetchone()
    if not user_result:
        conn.execute(
            text(
                "INSERT INTO users (username, email, password_hash, role, trust_score, created_at) "
                "VALUES (:username, :email, :password_hash, :role, :trust_score, NOW())"
            ),
            {
                "username": "assamese_annotator",
                "email": "annotator@example.com",
                "password_hash": "hashed-password",
                "role": "annotator",
                "trust_score": 0.95,
            },
        )
        user_result = conn.execute(
            text("SELECT id FROM users WHERE username = :username"),
            {"username": "assamese_annotator"},
        ).fetchone()
    user_id = user_result[0]

    # Create a sample raw phrase if missing
    phrase_result = conn.execute(
        text("SELECT id FROM raw_phrases WHERE phrase = :phrase"),
        {"phrase": "মই বিদ্যালয়লৈ যাওঁ।"},
    ).fetchone()
    if not phrase_result:
        conn.execute(
            text(
                "INSERT INTO raw_phrases (language, phrase, audio_url, submitted_by, status, created_at) "
                "VALUES (:language, :phrase, :audio_url, :submitted_by, :status, NOW())"
            ),
            {
                "language": "as",
                "phrase": "মই বিদ্যালয়লৈ যাওঁ।",
                "audio_url": None,
                "submitted_by": user_id,
                "status": "approved",
            },
        )
        phrase_result = conn.execute(
            text("SELECT id FROM raw_phrases WHERE phrase = :phrase"),
            {"phrase": "মই বিদ্যালয়লৈ যাওঁ।"},
        ).fetchone()
    raw_phrase_id = phrase_result[0]

    # Insert sample annotation
    syntax = {
        "subject": "মই",
        "verb": "যাওঁ",
        "object": "বিদ্যালয়লৈ",
        "tense": "Present",
        "voice": "Active",
    }
    pos_tags = {"মই": "PRON", "বিদ্যালয়লৈ": "NOUN", "যাওঁ": "VERB"}
    named_entities = {}

    conn.execute(
        text(
            "INSERT INTO annotations (raw_phrase_id, translated_text, pos_tags, named_entities, syntax, created_by, created_at) "
            "VALUES (:raw_phrase_id, :translated_text, CAST(:pos_tags AS jsonb), CAST(:named_entities AS jsonb), CAST(:syntax AS jsonb), :created_by, NOW())"
        ),
        {
            "raw_phrase_id": raw_phrase_id,
            "translated_text": "I go to school.",
            "pos_tags": json.dumps(pos_tags),
            "named_entities": json.dumps(named_entities),
            "syntax": json.dumps(syntax),
            "created_by": user_id,
        },
    )

    print("Inserted sample annotation")

    print("\nColumns for annotations:")
    columns = conn.execute(
        text("SELECT column_name, data_type FROM information_schema.columns WHERE table_name='annotations' ORDER BY ordinal_position")
    ).fetchall()
    for row in columns:
        print(row)

    print("\nRows matching subject=মই:")
    rows_subject = conn.execute(
        text("SELECT id, translated_text, syntax FROM annotations WHERE syntax @> CAST(:filter AS jsonb)") ,
        {"filter": json.dumps({"subject": "মই"})},
    ).fetchall()
    for row in rows_subject:
        print(row)

    print("\nRows matching verb=যাওঁ:")
    rows_verb = conn.execute(
        text("SELECT id, translated_text, syntax FROM annotations WHERE syntax @> CAST(:filter AS jsonb)") ,
        {"filter": json.dumps({"verb": "যাওঁ"})},
    ).fetchall()
    for row in rows_verb:
        print(row)
