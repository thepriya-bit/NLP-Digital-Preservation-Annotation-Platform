import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.core.config import settings
from app.core.security import get_password_hash, verify_password
from app.db.database import SessionLocal
from app.models import RawPhrase, User

ASSAMESE_PHRASES = [
    "নমস্কাৰ, আপোনাৰ নাম কি?",
    "মই আজি স্কুললৈ যাম।",
    "অসমীয়া ভাষা অতি মধুৰ।",
    "ব্ৰহ্মপুত্ৰ নদ অসমৰ জীৱনৰেখা।",
    "আপোনাক দেখি ভাল লাগিল।",
    "অসমৰ চাহ বিশ্ব বিখ্যাত।",
    "মই অসমীয়া জাতিৰ গৰ্বিত সন্তান।",
    "বিহু অসমৰ ৰাষ্ট্ৰীয় উৎসৱ।",
    "অসমীয়া সংস্কৃতি অতি সমৃদ্ধ।",
    "গুৱাহাটী অসমৰ সৰ্ববৃহৎ নগৰ।",
    "শিক্ষা জীৱনৰ অমূল্য সম্পদ।",
    "প্ৰকৃতি অসমৰ ৰূপহী বৰণ।",
    "মই অসমীয়া ভাষাত কবিতা লিখোঁ।",
    "আমাৰ সংস্কৃতি ৰক্ষা কৰাটো আমাৰ দায়িত্ব।",
    "এখন সুন্দৰ দেশ ভাৰতবৰ্ষ।",
    "অসমৰ বনৰীয়া জন্তুবোৰ সংৰক্ষণ কৰা উচিত।",
    "কামাখ্যা মন্দিৰ অসমৰ এটা পবিত্ৰ স্থান।",
    "একেলগে আমি অসম গঢ়িম।",
    "অসমীয়া সকলে সদায় আতিথ্যত বিশ্বাস কৰে।",
    "মাজুলী বিশ্বৰ সৰ্ববৃহৎ নদীদ্বীপ।",
    "অসমৰ কৃষি ভিত্তি অৰ্থনীতি।",
    "ৰাজহাঁহ অসমৰ ৰাজ্যিক চৰাই।",
    "এক শিৱসাগৰ অসমৰ ঐতিহাসিক ঠাই।",
    "অসমীয়া সকলে বিভিন্ন উৎসৱ পালন কৰে।",
    "সৰুৰে পৰা অসমীয়া ভাষাৰ শিক্ষা গ্ৰহণ কৰা উচিত।",
    "মোৰ দেশ অসম, মই অসমীয়া।",
    "পৰিৱেশ সংৰক্ষণ সময়ৰ প্ৰয়োজন।",
    "অসমীয়া সাহিত্য জগতত বহু প্ৰতিভা আছে।",
    "আইন শৃংখলা ৰক্ষা কৰা নাগৰিকৰ কৰ্তব্য।",
    "বিভিন্ন জাতি-জনজাতিৰ মিলন অসম।",
    "অসমীয়া ব্যাকৰণ অতি সমৃদ্ধ।",
    "মোৰ সপোন এখন উন্নত অসম।",
    "একতাৰ মাজতেই আমাৰ শক্তি।",
    "কৰ্মক্ষেত্ৰত সততা আৰু নিষ্ঠা প্ৰয়োজন।",
    "অসমৰ পৰ্যটন সম্ভাৱনা অপৰিসীম।",
    "পূৰ্বজনে কৈ গৈছে জ্ঞানেই শক্তি।",
    "অসমীয়া ভাষাত বিজ্ঞান চৰ্চা হোৱা উচিত।",
    "হাতী অসমৰ ৰাজ্যিক পশু।",
    "তৰা অসমৰ ৰাজ্যিক ফুল।",
    "অসমৰ গীত-মাতেৰে পৰিচয়।",
    "সোঁৱৰণী অতি মধুৰ আৰু বেদনাদায়ক।",
    "অসমীয়া নাট্যকলা বিশ্বজুৰি বিখ্যাত।",
    "বুদ্ধি আৰু ধৈৰ্য্য সফলতাৰ মূলমন্ত্ৰ।",
    "অসমীয়া ভাষাক ভাল পাবলৈ শিকা।",
    "শিশুসকল ভৱিষ্যতৰ ৰূপকাৰ।",
    "মহাপুৰুষ শ্ৰীমন্ত শংকৰদেৱ অসমৰ অমূল্য ৰত্ন।",
    "শ্ৰীশ্ৰী মাধৱদেৱ অসমীয়া সংস্কৃতিৰ স্তম্ভ।",
    "অসমৰ সাত ভনী ৰাজ্যৰ ভিতৰত অসম প্ৰধান।",
    "চাহ বাগিচাৰে ভৰা অসমৰ সৌন্দৰ্য।",
    "কাজিৰঙা ৰাষ্ট্ৰীয় উদ্যান বিশ্ব ঐতিহ্য।",
]

ENGLISH_TRANSLATIONS = [
    "Hello, what is your name?",
    "I will go to school today.",
    "The Assamese language is very sweet.",
    "The Brahmaputra river is the lifeline of Assam.",
    "Nice to meet you.",
    "Assam's tea is world famous.",
    "I am a proud child of the Assamese community.",
    "Bihu is the national festival of Assam.",
    "Assamese culture is very rich.",
    "Guwahati is the largest city in Assam.",
    "Education is a priceless asset in life.",
    "Nature is the beautiful color of Assam.",
    "I write poems in Assamese.",
    "Protecting our culture is our responsibility.",
    "India is a beautiful country.",
    "The wild animals of Assam should be conserved.",
    "Kamakhya temple is a holy place in Assam.",
    "Together we will build Assam.",
    "Assamese people always believe in hospitality.",
    "Majuli is the world's largest river island.",
    "Assam's economy is based on agriculture.",
    "The white-winged duck is the state bird of Assam.",
    "Sivasagar is a historical place in Assam.",
    "Assamese people celebrate various festivals.",
    "Assamese language education should be taken from childhood.",
    "My country is Assam, I am Assamese.",
    "Environmental conservation is the need of the hour.",
    "Assamese literature has many talents.",
    "Maintaining law and order is a citizen's duty.",
    "Assam is a melting pot of various tribes and communities.",
    "Assamese grammar is very rich.",
    "My dream is a developed Assam.",
    "Unity is our strength.",
    "Honesty and dedication are needed in the workplace.",
    "Assam's tourism potential is immense.",
    "Our ancestors said that knowledge is power.",
    "Science should be studied in the Assamese language.",
    "The elephant is the state animal of Assam.",
    "The foxtail orchid is the state flower of Assam.",
    "Assam is known for its songs and music.",
    "Memories are very sweet and painful.",
    "Assamese theater is famous worldwide.",
    "Intelligence and patience are the keys to success.",
    "Learn to love the Assamese language.",
    "Children are the architects of the future.",
    "Srimanta Shankardeva is an invaluable gem of Assam.",
    "Sri Sri Madhavdeva is a pillar of Assamese culture.",
    "Among the seven sister states, Assam is the main one.",
    "Assam's beauty is filled with tea gardens.",
    "Kaziranga National Park is a world heritage site.",
]


def seed_database():
    db = SessionLocal()

    admin = db.query(User).filter(User.username == "admin").first()
    if not admin:
        admin = User(
            username="admin",
            email="admin@nlp-platform.com",
            password_hash=get_password_hash("admin123"),
            role="admin",
            trust_score=0.0,
        )
        db.add(admin)
        db.commit()
        db.refresh(admin)
        print(f"Created admin user (id={admin.id})")
    elif not verify_password("admin123", admin.password_hash):
        admin.password_hash = get_password_hash("admin123")
        db.commit()
        print("Re-hashed admin password")

    riddhi = db.query(User).filter(User.username == "riddhi").first()
    if not riddhi:
        riddhi = User(
            username="riddhi",
            email="riddhi@example.com",
            password_hash=get_password_hash("riddhi123"),
            role="annotator",
            trust_score=0.0,
        )
        db.add(riddhi)
        db.commit()
        db.refresh(riddhi)
        print(f"Created user riddhi (id={riddhi.id})")
    elif not verify_password("riddhi123", riddhi.password_hash):
        riddhi.password_hash = get_password_hash("riddhi123")
        db.commit()
        print("Re-hashed riddhi password")

    priya = db.query(User).filter(User.username == "priya").first()
    if not priya:
        priya = User(
            username="priya",
            email="priya@example.com",
            password_hash=get_password_hash("priya123"),
            role="verifier",
            trust_score=0.0,
        )
        db.add(priya)
        db.commit()
        db.refresh(priya)
        print(f"Created user priya (id={priya.id})")
    elif not verify_password("priya123", priya.password_hash):
        priya.password_hash = get_password_hash("priya123")
        db.commit()
        print("Re-hashed priya password")

    existing_count = db.query(RawPhrase).count()
    if existing_count >= len(ASSAMESE_PHRASES):
        print(f"Database already has {existing_count} phrases. Skipping seed.")
        db.close()
        return

    for i, phrase_text in enumerate(ASSAMESE_PHRASES):
        existing = db.query(RawPhrase).filter(RawPhrase.phrase == phrase_text).first()
        if existing:
            continue
        raw = RawPhrase(
            language="assamese",
            phrase=phrase_text,
            submitted_by=admin.id,
            status="submitted",
        )
        db.add(raw)

    db.commit()
    total = db.query(RawPhrase).count()
    db.close()
    print(f"Seeded database with {total} Assamese phrases")


if __name__ == "__main__":
    seed_database()
