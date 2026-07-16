ASSAMESE_LANG = "assamese"


def contains_latin_alphabet(text: str) -> bool:
    for char in text:
        if "A" <= char <= "Z" or "a" <= char <= "z":
            return True
    return False


def validate_assamese_text(text: str, language: str = ASSAMESE_LANG) -> tuple[bool, str | None]:
    if language == ASSAMESE_LANG and contains_latin_alphabet(text):
        return False, "Assamese text contains Latin alphabet characters; use Assamese Unicode script only"
    return True, None
