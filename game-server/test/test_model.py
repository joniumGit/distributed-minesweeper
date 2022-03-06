import pytest
from pydantic import ValidationError

from server.models import Start


def test_start_too_many_mines():
    with pytest.raises(ValidationError) as e:
        Start(**{'width': 8, 'height': 8, 'mines': 95})
    assert e.value.errors()[0]['msg'].startswith('Too many mines')


@pytest.mark.parametrize("w,h", [
    (2, 2),
    (1, 1),
    (1, 100),
    (100, 1)
])
def test_start_too_small_field(w, h):
    with pytest.raises(ValidationError) as e:
        Start(**{'width': w, 'height': h, 'mines': 95})
    assert e.value.errors()[0]['msg'].startswith('Bad dimensions')


def test_start_too_small_values():
    with pytest.raises(ValidationError) as e:
        Start(**{'width': 0, 'height': 0, 'mines': 0})
    assert len(e.value.errors()) == 3
