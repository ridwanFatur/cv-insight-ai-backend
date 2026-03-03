import pytest
from utils.email_utils import extract_name_from_email, is_valid_email


@pytest.mark.parametrize(
    "email,expected",
    [
        ("ajeng.faturrahman@example.com", "Ajeng Faturrahman"),
        ("ridwan@example.com", "Ridwan"),
        ("john_doe123@example.com", "John Doe"),
        ("alice-bob@example.com", "Alice Bob"),
        ("foo.bar.baz@example.com", "Foo Bar"),
        ("singleword@example.com", "Singleword"),
        ("user+test@example.com", "User Test"),
        ("multiple..dots@example.com", "Multiple Dots")
    ]
)
def test_extract_name_from_email(email, expected):
    assert extract_name_from_email(email) == expected


@pytest.mark.parametrize(
    "email,expected",
    [
        ("ajeng.faturrahman@example.com", True),
        ("ridwan@example.com", True),
        ("john_doe123@example.com", True),
        ("alice-bob@example.com", True),
        ("foo.bar.baz@example.com", True),
        ("singleword@example.com", True),
        ("user+test@example.com", True),
        ("multiple..dots@example.com", True),
        ("not-an-email", False),
        ("@no-local-part.com", False),
        ("missing-domain@", False),
        ("missingatsign.com", False),
        ("user@.com", False),
    ]
)
def test_is_valid_email(email, expected):
    assert is_valid_email(email) == expected
