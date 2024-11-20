import random
from string import ascii_letters

import pytest


@pytest.fixture
def fake_user_name():
    def _generate(length):
        return "".join(random.choice(ascii_letters) for _ in range(length))

    return _generate
