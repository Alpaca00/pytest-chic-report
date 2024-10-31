import pytest


class TestMessenger:
    """Test the messenger plugin."""

    def test_expect_passed(self):
        assert 1 == 1

    def test_expect_failed(self):
        assert 1 >= 5

    @pytest.mark.xfail
    def test_expect_xpassed(self):
        assert 1 >= 5

    @pytest.mark.skip
    def test_expect_skipped(self):
        assert 1 == 2

    def test_raise_error(self):
        with pytest.raises(Exception):
            x = 1 / 0

    @pytest.mark.xfail
    def test_asserts_in_loop(self):
        for number in range(1, 10):
            assert number % 2 == 0, f"{number} is not a multiple of 2"

    @pytest.mark.parametrize("number", list(range(0, 10, 2)))
    def test_asserts_by_parametrize_expect_passing(self, number):
        assert number % 2 == 0

    @pytest.mark.parametrize("number", list(range(0, 10, 3)))
    @pytest.mark.xfail
    def test_asserts_by_parametrize_expect_failed(self, number):
        assert number % 2 == 0
