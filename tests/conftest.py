import os

import pytest
from typer.testing import CliRunner


@pytest.fixture(scope="module")
def runner():
    return CliRunner()


@pytest.fixture(scope="module")
def sample_image_path():
    current_working_directory = os.getcwd()
    return os.path.join(current_working_directory, "tests/test_image.jpeg")
