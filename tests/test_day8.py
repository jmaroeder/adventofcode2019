import logging
from textwrap import dedent
import pytest

from adventofcode2019.day8 import parta, partb

LOG = logging.getLogger(__name__)


@pytest.mark.parametrize(
    ('data', 'width', 'height', 'result'), [
        ('123456789012', 3, 2, 1),
    ],
)
def test_parta(data, width, height, result, caplog):
    caplog.set_level(logging.DEBUG)
    assert parta(data, width=width, height=height) == result



@pytest.mark.parametrize(
    ('data', 'width', 'height', 'result'), [
        ('0222112222120000', 2, 2, ' █\n█ \n'),
    ],
)
def test_parta(data, width, height, result, caplog):
    caplog.set_level(logging.DEBUG)
    assert partb(data, width=height, height=height) == result
