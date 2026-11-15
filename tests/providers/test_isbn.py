import pytest

from faker.providers.isbn import ISBN10, ISBN13
from faker.providers.isbn.en_US import Provider as ISBNProvider
from faker.providers.isbn.es_ES import Provider as EsEsISBNProvider


class TestISBN10:
    def test_check_digit_is_correct(self):
        isbn = ISBN10(group="1", registrant="4516", publication="7331")
        assert isbn.check_digit == "0"
        isbn = ISBN10(group="0", registrant="06", publication="230125")
        assert isbn.check_digit == "X"
        isbn = ISBN10(group="1", registrant="4936", publication="8222")
        assert isbn.check_digit == "9"

    def test_format_length(self):
        isbn = ISBN10(group="1", registrant="4516", publication="7331")
        assert len(isbn.format()) == 10

    def test_format_skips_empty_parts(self):
        isbn = ISBN10(group="84", registrant="", publication="1234567")
        assert isbn.format("-") == "84-1234567-3"
        assert "--" not in isbn.format("-")


class TestISBN13:
    def test_check_digit_is_correct(self):
        isbn = ISBN13(ean="978", group="1", registrant="4516", publication="7331")
        assert isbn.check_digit == "9"
        isbn = ISBN13(ean="978", group="1", registrant="59327", publication="599")
        assert isbn.check_digit == "0"
        isbn = ISBN13(ean="978", group="1", registrant="4919", publication="2757")
        assert isbn.check_digit == "1"

    def test_format_length(self):
        isbn = ISBN13(ean="978", group="1", registrant="4516", publication="7331")
        assert len(isbn.format()) == 13

    def test_format_skips_empty_parts(self):
        isbn = ISBN13(ean="978", group="84", registrant="", publication="1234567")
        assert isbn.format("-") == "978-84-1234567-4"
        assert "--" not in isbn.format("-")


class TestProvider:
    prov = ISBNProvider(None)

    def test_reg_pub_separation(self):
        r1 = ("0000000", "0000001", 1)
        r2 = ("0000002", "0000003", 2)
        assert self.prov._registrant_publication("00000000", [r1, r2]) == (
            "0",
            "0000000",
        )
        assert self.prov._registrant_publication("00000010", [r1, r2]) == (
            "0",
            "0000010",
        )
        assert self.prov._registrant_publication("00000019", [r1, r2]) == (
            "0",
            "0000019",
        )
        assert self.prov._registrant_publication("00000020", [r1, r2]) == (
            "00",
            "000020",
        )
        assert self.prov._registrant_publication("00000030", [r1, r2]) == (
            "00",
            "000030",
        )
        assert self.prov._registrant_publication("00000031", [r1, r2]) == (
            "00",
            "000031",
        )
        assert self.prov._registrant_publication("00000039", [r1, r2]) == (
            "00",
            "000039",
        )

    def test_rule_not_found(self):
        with pytest.raises(Exception):
            r = ("0000000", "0000001", 1)
            self.prov._registrant_publication("0000002", [r])


class TestEsEs:
    """Tests es_ES isbn provider"""

    num_samples = 1000

    def test_rules_only_contain_valid_registration_groups(self):
        # Spain's registration groups are 978-84 and 979-13; "978-13" is not
        # a real group, and every rule must yield a non-empty registrant.
        assert set(EsEsISBNProvider.rules) == {"978"}
        assert set(EsEsISBNProvider.rules["978"]) == {"84"}
        for rules in EsEsISBNProvider.rules["978"].values():
            assert all(reg_len > 0 for _, _, reg_len in rules)

    def test_isbn13_is_well_formed(self, faker, num_samples):
        for _ in range(num_samples):
            isbn = faker.isbn13()
            parts = isbn.split("-")
            assert len(parts) == 5
            assert parts[:2] == ["978", "84"]
            assert all(parts)
            assert len(isbn.replace("-", "")) == 13

    def test_isbn10_is_well_formed(self, faker, num_samples):
        for _ in range(num_samples):
            isbn = faker.isbn10()
            parts = isbn.split("-")
            assert len(parts) == 4
            assert parts[0] == "84"
            assert all(parts)
            assert len(isbn.replace("-", "")) == 10

    def test_isbn_stdnum(self, faker, num_samples):
        try:
            from stdnum import isbn as isbn_validator
        except ImportError:
            pytest.skip("stdnum not available")
        for _ in range(num_samples):
            isbn_validator.validate(faker.isbn13())
            isbn_validator.validate(faker.isbn10())
