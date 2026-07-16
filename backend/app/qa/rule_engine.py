from pydantic import BaseModel

from app.qa.assamese_validator import validate_assamese_text
from app.qa.toxicity_filter import check_toxicity


class QARuleError(BaseModel):
    rule: str
    message: str


class QAResult(BaseModel):
    is_valid: bool
    errors: list[QARuleError] = []


class QARuleEngine:
    @staticmethod
    def validate(text: str, language: str = "assamese") -> QAResult:
        errors: list[QARuleError] = []

        is_valid_unicode, unicode_error = validate_assamese_text(text, language)
        if not is_valid_unicode:
            errors.append(QARuleError(rule="assamese_unicode", message=unicode_error))

        is_clean, toxicity_error = check_toxicity(text)
        if not is_clean:
            errors.append(QARuleError(rule="toxicity", message=toxicity_error))

        return QAResult(is_valid=len(errors) == 0, errors=errors)
