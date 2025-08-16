from pathlib import Path
import shutil
import tempfile
from unittest import TestCase
from unittest.mock import patch
from src.cli.naming import naming

class TestCLINaming(TestCase):
    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.input_dir = str(Path(self.tmpdir) / "test_input")
        self.output_dir = str(Path(self.tmpdir) / "test_output")
        self.mode = "copy"
        self.in_image = False

        Path(self.input_dir).mkdir(parents=True, exist_ok=True)
        Path(self.output_dir).mkdir(parents=True, exist_ok=True)

    def tearDown(self):
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    @patch("src.cli.naming.check_naming_args")
    @patch("src.cli.naming.show_execution_info")
    @patch("src.core.namer.Namer.run")
    def test_naming(self, mock_run, mock_show_info, mock_check_args):
        naming(
            input_dir=self.input_dir,
            mode=self.mode,
            in_image=self.in_image,
            output_dir=self.output_dir
        )

        mock_check_args.assert_called_once_with(self.mode, self.input_dir)
        mock_show_info.assert_called_once_with(
            self.input_dir, self.mode, self.in_image, self.output_dir
        )
        mock_run.assert_called_once()

    def test_check_naming_args_all_valid(self):
        naming(
            input_dir=self.input_dir,
            mode=self.mode,
            in_image=self.in_image,
            output_dir=self.output_dir
        )

    def test_check_naming_args_invalid_mode(self):
        with self.assertRaises(ValueError):
            naming(
                input_dir=self.input_dir,
                mode="invalid_mode",
                in_image=self.in_image,
                output_dir=self.output_dir
            )
    def test_check_naming_args_nonexistent_directory(self):
        with self.assertRaises(FileNotFoundError):
            naming(
                input_dir=str(Path(self.tmpdir) / "nonexistent"),
                mode=self.mode,
                in_image=self.in_image,
                output_dir=self.output_dir
            )

    def test_check_naming_args_not_a_directory(self):
        file_path = str(Path(self.tmpdir) / "test_file.txt")
        Path(file_path).touch()
        with self.assertRaises(ValueError):
            naming(
                input_dir=file_path,
                mode=self.mode,
                in_image=self.in_image,
                output_dir=self.output_dir
            )
