import io
import os
import zipfile
from shutil import copyfile
from unittest.mock import MagicMock, patch

import pytest
from PIL import Image
from typer.testing import CliRunner

from imagemangler.cli import app


@patch("cv2.waitKey", MagicMock())
@patch("cv2.destroyAllWindows", MagicMock())
def test_main_valid_local_image(runner, sample_image_path):
    # Test if the main function runs without error with a valid local image
    with runner.isolated_filesystem():
        isolated_image_path = "isolated_test_image.jpeg"
        copyfile(sample_image_path, isolated_image_path)

        result = runner.invoke(
            app, [sample_image_path, "--quality", "70", "--quality-step", "2"]
        )
        print(result.exception, result.output)
        assert result.exit_code == 0


@patch("cv2.waitKey", MagicMock())
@patch("cv2.destroyAllWindows", MagicMock())
def test_main_save_last_mangled_image(runner, sample_image_path):
    # Test if the last mangled image is saved
    with runner.isolated_filesystem():
        # Copy the sample image into the isolated filesystem
        isolated_image_path = "isolated_test_image.jpeg"
        copyfile(sample_image_path, isolated_image_path)

        result = runner.invoke(
            app,
            [isolated_image_path, "--quality", "70", "--quality-step", "2"],
            input="n\ny\n",
        )
        assert result.exit_code == 0
        assert os.path.exists("mangled_img.jpeg")


@patch("cv2.waitKey", MagicMock())
@patch("cv2.destroyAllWindows", MagicMock())
def test_main_save_all_mangled_images(runner, sample_image_path):
    # Test if all mangled images are saved in a zip file
    with runner.isolated_filesystem():
        isolated_image_path = "isolated_test_image.jpeg"
        copyfile(sample_image_path, isolated_image_path)

        result = runner.invoke(
            app,
            [isolated_image_path, "--quality", "70", "--quality-step", "2"],
            input="y\n",
        )
        assert result.exit_code == 0
        expected_zip_filename = "mangled_isolated_test_image.zip"
        assert os.path.exists(expected_zip_filename)

        # Verify if the zip file contains the expected images
        with zipfile.ZipFile(expected_zip_filename, "r") as zf:
            assert len(zf.namelist()) > 0
            for i, file_name in enumerate(zf.namelist()):
                assert file_name == f"mangled_img_{i}.jpeg"
