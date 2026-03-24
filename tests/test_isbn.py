import pytest

from app.isbn import validate_isbn13


class TestValidateIsbn13:
    def test_valid_isbn(self):
        assert validate_isbn13("9780306406157") == "9780306406157"

    def test_valid_isbn_with_hyphens(self):
        assert validate_isbn13("978-0-306-40615-7") == "9780306406157"

    def test_valid_isbn_with_spaces(self):
        assert validate_isbn13("978 0 306 40615 7") == "9780306406157"

    def test_valid_isbn_mixed_separators(self):
        assert validate_isbn13("978-0 306-40615 7") == "9780306406157"

    def test_another_valid_isbn(self):
        assert validate_isbn13("9781234567897") == "9781234567897"

    def test_invalid_check_digit(self):
        with pytest.raises(ValueError, match="Invalid ISBN-13 check digit"):
            validate_isbn13("9780306406158")

    def test_too_short(self):
        with pytest.raises(ValueError, match="exactly 13 digits"):
            validate_isbn13("978030640615")

    def test_too_long(self):
        with pytest.raises(ValueError, match="exactly 13 digits"):
            validate_isbn13("97803064061577")

    def test_non_numeric(self):
        with pytest.raises(ValueError, match="only digits"):
            validate_isbn13("978030640615X")

    def test_empty_string(self):
        with pytest.raises(ValueError, match="exactly 13 digits"):
            validate_isbn13("")

    def test_only_hyphens(self):
        with pytest.raises(ValueError, match="exactly 13 digits"):
            validate_isbn13("---")
