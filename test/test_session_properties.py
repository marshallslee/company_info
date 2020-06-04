import unittest
from db import session


class TestConfig(unittest.TestCase):
    def test_session_autoflush(self):
        autoflush = session.autoflush
        self.assertEqual(autoflush, True)

    def test_session_autocommit(self):
        autocommit = session.autocommit
        self.assertEqual(autocommit, False)


if __name__ == '__main__':
    unittest.main()
