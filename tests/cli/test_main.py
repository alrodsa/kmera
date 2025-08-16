from unittest import TestCase
from unittest.mock import patch
from src.cli.naming import naming
from src.cli.main import main

class TestCLIMain(TestCase):

    @patch("src.cli.main.fire.Fire")
    def test_main_naming(self, mock_fire):
        main()
        mock_fire.assert_called_once_with({"naming": naming})
