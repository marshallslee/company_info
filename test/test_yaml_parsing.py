import unittest
import yaml
import os


class TestYAMLParsing(unittest.TestCase):
    def test_yaml_parsing(self):
        ENV = os.environ.get('FLASK_ENV')
        with open('config/{}.yaml'.format(ENV)) as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
        self.assertEqual(config['db']['database'], 'company_info')


if __name__ == '__main__':
    unittest.main()
