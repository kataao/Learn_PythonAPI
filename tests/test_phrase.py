class TestPhrase:
    def test_short_phrase(self):
        phrase = input("Set a phrase: ")
        assert len(phrase) < 15, "The phrase length should be less than 15 simbols"
