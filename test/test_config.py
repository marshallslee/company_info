import unittest
from app import app


class TestConfig(unittest.TestCase):
    def test_json_as_ascii(self):
        val = app.config.get('JSON_AS_ASCII')
        self.assertEqual(val, False)

    def test_jsonify_prettyprint_regular(self):
        val = app.config.get('JSONIFY_PRETTYPRINT_REGULAR')
        self.assertEqual(val, True)


if __name__ == '__main__':
    unittest.main()
