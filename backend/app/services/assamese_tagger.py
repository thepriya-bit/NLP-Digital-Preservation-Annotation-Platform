ASSAMESE_PUNCTUATION = set("!?.,;:-—\"'()[]{}""''«»…।॥")
ASSAMESE_VOWELS = set("অআইঈউঊঋএঐওঔ")
ASSAMESE_CONSONANTS = set("কখগঘঙচছজঝঞটঠডঢণতথদধনপফবভমযৰলৱশষসহ")

POS_LEXICON: dict[str, str] = {
    "অ": "DET", "আমি": "PRON", "তুমি": "PRON", "সি": "PRON", "তি": "PRON",
    "এও": "PRON", "সেই": "DET", "এই": "DET", "তেওঁ": "PRON", "আপুনি": "PRON",
    "মই": "PRON", "আমাক": "PRON", "তোমাক": "PRON", "তাক": "PRON", "তেওঁক": "PRON",
    "আমাৰ": "PRON", "তোমাৰ": "PRON", "তাৰ": "PRON", "তেওঁৰ": "PRON",
    "কি": "PRON", "কুন": "DET", "যি": "PRON", "যিকোনো": "DET",
    "নমস্কাৰ": "INTJ", "ধন্যবাদ": "INTJ", "দয়া": "NOUN", "কৰি": "VERB",
    "আছে": "VERB", "আছিল": "VERB", "আছি": "VERB", "নাই": "VERB",
    "যাওক": "VERB", "যাব": "VERB", "গল": "VERB", "গৈ": "VERB",
    "কৰ": "VERB", "কৰে": "VERB", "কৰা": "VERB", "কৰিছে": "VERB",
    "কৰিলে": "VERB", "কৰিম": "VERB", "কৰিব": "VERB", "কৰো": "VERB",
    "কওক": "VERB", "কৈছে": "VERB", "কৈছিল": "VERB",
    "দিয়া": "VERB", "দিয়ে": "VERB", "দিলে": "VERB", "দিছে": "VERB",
    "দিব": "VERB", "দিও": "VERB", "দিয়া": "VERB",
    "পাৰে": "VERB", "পাৰো": "VERB", "পাৰি": "VERB", "পাৰিব": "VERB",
    "হয়": "VERB", "হৈছে": "VERB", "হব": "VERB", "হৈ": "VERB",
    "থাকে": "VERB", "থাকিব": "VERB", "আছো": "VERB", "আছোঁ": "VERB",
    "বলে": "VERB", "বোলা": "VERB",
    "ভাল": "ADJ", "বেয়া": "ADJ", "সুন্দৰ": "ADJ", "মৰম": "NOUN",
    "ডাঙৰ": "ADJ", "সৰু": "ADJ", "পুৰণি": "ADJ", "নতুন": "ADJ",
    "উচ্চ": "ADJ", "নিম্ন": "ADJ", "দীঘল": "ADJ", "চুটি": "ADJ",
    "গৰম": "ADJ", "ঠাণ্ডা": "ADJ", "কঠিন": "ADJ", "সহজ": "ADJ",
    "বহু": "ADJ", "অলপ": "ADV", "বেছি": "ADV", "খুব": "ADV",
    "এতিয়া": "ADV", "কালি": "ADV", "আজি": "ADV", "এতিয়াই": "ADV",
    "পাছত": "ADV", "পিছত": "ADV", "তলত": "ADV", "ওপৰত": "ADV",
    "ভিতৰত": "ADV", "বাহিৰত": "ADV", "আগত": "ADV",
    "আৰু": "CCONJ", "কিন্তু": "CCONJ", "কাৰণ": "SCONJ", "যদি": "SCONJ",
    "তথাপি": "CCONJ", "অথবা": "CCONJ", "নাইবা": "CCONJ", "এবং": "CCONJ",
    "যাতে": "SCONJ", "যেতিয়া": "SCONJ", "তেতিয়া": "ADV",
    "বহুত": "ADJ", "প্ৰতি": "ADP", "কাৰণে": "ADP", "বাবে": "ADP",
    "দ্বাৰা": "ADP", "পৰা": "ADP", "লৈ": "ADP", "লাগি": "ADP",
    "সৈতে": "ADP", "কে": "ADP", "ক": "ADP", "ত": "ADP",
    "এটা": "DET", "এটি": "DET", "এক": "DET", "এজন": "DET",
    "কিছু": "DET", "কেইটা": "DET", "প্ৰত্যেক": "DET", "প্ৰতিটি": "DET",
    "একে": "ADJ",
    "মানুহ": "NOUN", "লোক": "NOUN", "ঘৰ": "NOUN", "বস্তু": "NOUN",
    "কিতাপ": "NOUN", "বই": "NOUN", "বিশ্ববিদ্যালয়": "NOUN",
    "বিদ্যালয়": "NOUN", "বিদ্যালয়": "NOUN", "শিক্ষক": "NOUN",
    "শিক্ষয়িত্ৰী": "NOUN", "ছাত্ৰ": "NOUN", "ছাত্রী": "NOUN",
    "পানী": "NOUN", "খাদ্য": "NOUN", "ভাত": "NOUN", "দেশ": "NOUN",
    "ৰাজ্য": "NOUN", "চহৰ": "NOUN", "গাঁও": "NOUN", "নদী": "NOUN",
    "পৰ্বত": "NOUN", "সূর্য": "NOUN", "চন্দ্ৰ": "NOUN", "তৰা": "NOUN",
    "আকাশ": "NOUN", "মাটি": "NOUN", "জুই": "NOUN", "বতাহ": "NOUN",
    "সময়": "NOUN", "বছৰ": "NOUN", "মাহ": "NOUN", "দিন": "NOUN",
    "সপ্তাহ": "NOUN", "বাৰ": "NOUN", "ঘন্টা": "NOUN", "মিনিট": "NOUN",
    "কাম": "NOUN", "বিশ্বাস": "NOUN", "ভাষা": "NOUN", "অসমীয়া": "NOUN",
    "ইংৰাজী": "NOUN", "বাংলা": "NOUN", "হিন্দী": "NOUN",
    "উদ্দেশ্য": "NOUN", "প্ৰকল্প": "NOUN", "সামাজিক": "ADJ",
    "সাংস্কৃতিক": "ADJ", "ৰাজনৈতিক": "ADJ", "অৰ্থনৈতিক": "ADJ",
    "প্ৰাকৃতিক": "ADJ", "বৈজ্ঞানিক": "ADJ", "প্ৰযুক্তিগত": "ADJ",
    "জাতীয়": "ADJ", "আন্তৰ্জাতিক": "ADJ", "স্থানীয়": "ADJ",
}

VERB_SUFFIXES = ["িছে", "িছিল", "িব", "িম", "িলে", "ো", "ওঁ", "ে", "া", "িছ", "িছো", "িছোঁ"]
NOUN_SUFFIXES = ["খন", "জন", "টি", "বোৰ", "হঁত", "সকল", "ৰ", "ক", "ত", "েৰে"]
ADJ_SUFFIXES = ["ীয়", "ীয়", "কৰ", "ময়", "যুক্ত"]
ADV_SUFFIXES = ["কৈ", "ভাবে", "ৰূপে"]


def _lookup_pos(word: str) -> str | None:
    return POS_LEXICON.get(word)


def _rule_based_pos(word: str) -> str:
    if all(c in ASSAMESE_PUNCTUATION for c in word):
        return "PUNCT"
    if any(c in "০১২৩৪৫৬৭৮৯" for c in word):
        return "NUM"
    for suf in VERB_SUFFIXES:
        if word.endswith(suf) and len(word) > len(suf) + 1:
            return "VERB"
    for suf in NOUN_SUFFIXES:
        if word.endswith(suf) and len(word) > len(suf) + 1:
            return "NOUN"
    for suf in ADJ_SUFFIXES:
        if word.endswith(suf):
            return "ADJ"
    for suf in ADV_SUFFIXES:
        if word.endswith(suf):
            return "ADV"
    first = word[0] if word else ""
    if first in ASSAMESE_VOWELS:
        return "NOUN"
    return "X"


def tag_pos(words: list[str]) -> list[dict[str, str]]:
    result: list[dict[str, str]] = []
    for word in words:
        pos = _lookup_pos(word) or _rule_based_pos(word)
        result.append({"token": word, "pos": pos})
    return result


NAMES: set[str] = {
    "অসম", "ভাৰত", "গুৱাহাটী", "যোৰহাট", "ডিব্ৰুগড়",
    "শিৱসাগৰ", "তেজপুৰ", "নলবাৰী", "বঙাইগাঁও", "দক্ষিণ",
    "ব্ৰহ্মপুত্ৰ", "বৰাক", "ভাগীৰথী", "ভাৰতীয়", "অসমীয়া",
}


def tag_named_entities(words: list[str]) -> list[dict[str, str]]:
    result: list[dict[str, str]] = []
    for word in words:
        if word in NAMES:
            result.append({"token": word, "label": "LOC"})
        elif word and word[0].isupper() and not any(c in ASSAMESE_VOWELS for c in word):
            result.append({"token": word, "label": "O"})
        else:
            result.append({"token": word, "label": "O"})
    return result


def tag_syntax(text: str) -> dict:
    import re
    tokens = re.findall(r"[\w\u0980-\u09FF]+|[^\w\s]", text)
    if not tokens:
        tokens = text.split()
    pos_tags = tag_pos(tokens)
    named_entities = tag_named_entities(tokens)
    return {
        "tokens": tokens,
        "pos_tags": pos_tags,
        "named_entities": named_entities,
        "syntax_tree": {"phrase_structure": "flat"},
    }
