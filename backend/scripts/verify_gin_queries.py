from sqlalchemy import create_engine, text
import json

engine = create_engine('postgresql://postgres:password@localhost:5432/nlp_platform')

with engine.connect() as conn:
    print('ROWS')
    for row in conn.execute(text("SELECT id, translated_text, syntax FROM annotations ORDER BY id")).fetchall():
        print(row)

    print('\nINDEXES')
    for row in conn.execute(text("SELECT indexname, indexdef FROM pg_indexes WHERE tablename='annotations' ORDER BY indexname")).fetchall():
        print(row)

    print('\nPLAN for subject=মই')
    plan = conn.execute(
        text("EXPLAIN ANALYZE SELECT * FROM annotations WHERE syntax @> CAST(:filter AS jsonb)"),
        {'filter': json.dumps({'subject': 'মই'})},
    ).scalar()
    print(plan)

    print('\nPLAN for verb=যাওঁ')
    plan = conn.execute(
        text("EXPLAIN ANALYZE SELECT * FROM annotations WHERE syntax @> CAST(:filter AS jsonb)"),
        {'filter': json.dumps({'verb': 'যাওঁ'})},
    ).scalar()
    print(plan)
