from string import (
    ascii_letters,
    ascii_lowercase,
    ascii_uppercase,
    digits,
    hexdigits,
    printable,
    punctuation,
)

import pytest

from src.user.session import hash_password, verify_password


class TestHashPassword:
    def test_hash_password_returns_a_string(self):
        password = "password"
        hashed_password = hash_password(password)
        assert isinstance(hashed_password, str)

    def test_hash_password_empty_string(self):
        """Checks that empty password generate correct hash password"""
        password = ""
        hashed_password = hash_password(password)
        assert len(hashed_password) > 0

    def test_hash_password_returns_different_strings_for_different_passwords(self):
        password1 = "password1"
        password2 = "password2"
        hashed_password1 = hash_password(password1)
        hashed_password2 = hash_password(password2)
        assert hashed_password1 != hashed_password2

    def test_hash_password_should_return_different_hash_when_password_is_the_same(self):
        password = "password"
        hashed_password = hash_password(password)
        assert hash_password(password) != hashed_password

    @pytest.mark.parametrize("size_password", [1, 100, 1000, 10000])
    def test_should_return_password_when_size_is_different(self, size_password):
        password = "p" * size_password
        hashed_password = hash_password(password)
        assert hashed_password

    @pytest.mark.parametrize(
        "password",
        [
            ascii_lowercase,
            ascii_uppercase,
            ascii_letters,
            digits,
            hexdigits,
            punctuation,
            printable,
        ],
    )
    def test_hash_password_handles_special_characters(self, password):
        """Should handle password with special characters"""
        hashed_password = hash_password(password)
        assert hashed_password


class TestVerifyPassword:
    def test_verify_password_returns_true_for_correct_password(self):
        password = "password"
        hashed_password = hash_password(password)
        assert verify_password(hashed_password, password)

    def test_verify_password_returns_false_for_incorrect_password(self):
        password = "password"
        hashed_password = hash_password(password)
        assert not verify_password(hashed_password, "new_one")
