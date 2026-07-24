from app.qa.assamese_validator import validate_assamese_text, contains_latin_alphabet
from app.qa.rule_engine import QARuleEngine
from app.qa.toxicity_filter import check_toxicity


class TestAssameseValidator:
    def test_contains_latin_true(self):
        assert contains_latin_alphabet("Hello অসম") is True

    def test_contains_latin_false(self):
        assert contains_latin_alphabet("নমস্কাৰ অসম") is False

    def test_validate_assamese_pure(self):
        valid, error = validate_assamese_text("নমস্কাৰ", "assamese")
        assert valid is True
        assert error is None

    def test_validate_assamese_with_latin(self):
        valid, error = validate_assamese_text("Hello অসম", "assamese")
        assert valid is False
        assert "Latin" in error


class TestToxicityFilter:
    def test_clean_text(self):
        clean, error = check_toxicity("This is a normal sentence")
        assert clean is True
        assert error is None

    def test_empty_text(self):
        clean, error = check_toxicity("")
        assert clean is True


class TestQARuleEngine:
    def test_valid_assamese(self):
        result = QARuleEngine.validate("নমস্কাৰ", "assamese")
        assert result.is_valid is True
        assert len(result.errors) == 0

    def test_invalid_assamese_with_latin(self):
        result = QARuleEngine.validate("Hello অসম", "assamese")
        assert result.is_valid is False
        assert any(e.rule == "assamese_unicode" for e in result.errors)
