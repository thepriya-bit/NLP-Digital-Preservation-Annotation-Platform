from better_profanity import profanity

CUSTOM_BADWORDS: list[str] = []


def _init_profanity() -> None:
    profanity.load_censor_words()
    if CUSTOM_BADWORDS:
        profanity.add_censor_words(CUSTOM_BADWORDS)


def check_toxicity(text: str) -> tuple[bool, str | None]:
    _init_profanity()
    if profanity.contains_profanity(text):
        return False, "Submission contains inappropriate or toxic language"
    return True, None
