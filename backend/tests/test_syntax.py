from app.services.assamese_tagger import tag_syntax, tag_pos, tag_named_entities


class TestTagger:
    def test_tag_syntax_empty(self):
        result = tag_syntax("")
        assert isinstance(result["tokens"], list)
        assert result["pos_tags"] == []
        assert result["named_entities"] == []

    def test_tag_syntax_assamese(self):
        result = tag_syntax("মই বিদ্যালয়লৈ যাওঁ")
        assert len(result["tokens"]) > 0
        assert len(result["pos_tags"]) == len(result["tokens"])
        assert len(result["named_entities"]) == len(result["tokens"])
        assert "syntax_tree" in result

    def test_tag_syntax_mixed(self):
        result = tag_syntax("নমস্কাৰ Hello")
        assert len(result["tokens"]) == 2

    def test_tag_pos_pronoun(self):
        result = tag_pos(["মই", "যাওঁ"])
        assert result[0]["pos"] == "PRON"

    def test_tag_pos_verb(self):
        result = tag_pos(["যাওঁ"])
        assert result[0]["pos"] == "VERB"

    def test_tag_pos_punctuation(self):
        result = tag_pos(["।"])
        assert result[0]["pos"] == "PUNCT"

    def test_tag_pos_number(self):
        result = tag_pos(["১২৩"])
        assert result[0]["pos"] == "NUM"

    def test_tag_pos_unknown(self):
        result = tag_pos(["xyzunknown"])
        pos = result[0]["pos"]
        assert pos in ("X", "NOUN", "VERB", "ADJ", "ADV")

    def test_tag_entities_assamese(self):
        result = tag_named_entities(["অসম", "মই", "যাওঁ"])
        labels = [e["label"] for e in result]
        assert labels == ["LOC", "O", "O"]

    def test_tag_syntax_with_punctuation(self):
        result = tag_syntax("মই, তুমি আৰু সি।")
        assert "।" in result["tokens"]
        punct_tags = [t for t in result["pos_tags"] if t["token"] == "।"]
        if punct_tags:
            assert punct_tags[0]["pos"] == "PUNCT"

    def test_tag_syntax_multiple_sentences(self):
        result = tag_syntax("মই যাম। সি যাব।")
        assert len(result["tokens"]) >= 4
