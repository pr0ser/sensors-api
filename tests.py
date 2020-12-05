import schemathesis
from decouple import config

schema = schemathesis.from_uri(config('TEST_URL'))


@schema.parametrize()
def test_api(case):
    case.call_and_validate()
