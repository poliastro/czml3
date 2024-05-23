import json
import os

import pytest
from czml3.examples import simple

TESTS_DIR = os.path.dirname(os.path.realpath(__file__))


@pytest.mark.parametrize("document,filename", [(simple, "simple.czml")])
def test_simple(document, filename):
    with open(os.path.join(TESTS_DIR, filename)) as fp:
        expected_result = json.load(fp)

    result = json.loads(document.dumps())
    for ii, packet in enumerate(result):
        expected_packet = expected_result[ii]
        for key in packet:
            prop = packet[key]
            expected_prop = expected_packet[key]

            if isinstance(prop, dict):
                for sub_key in prop:
                    assert prop[sub_key] == expected_prop[sub_key]
            else:
                assert prop == expected_prop
