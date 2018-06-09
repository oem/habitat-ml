import unittest
import pandas as pd
from ....web.helpers.data_preparation import prepare_measurements_for_last_day


class TestHelpers(unittest.TestCase):
    test_df = pd.DataFrame(0, index=range(72), columns=range(2))

    def test_prepare_measurements_for_last_day_returns_dicts(self):
        result = prepare_measurements_for_last_day(self.test_df)
        self.assertEqual(type([]), type(result))
        self.assertEqual(type({}), type(result[0]))


if __name__ == '__main__':
    unittest.main()
