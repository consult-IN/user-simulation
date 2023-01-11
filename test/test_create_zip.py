import pytest
from pathlib import Path

from src.create_zip import get_files_in_path, create_zip

@pytest.mark.parametrize("test_example_paths", [
    (r"test\test_data\Test_document.pdf"),
    (r"test\test_data")
    ])
def test_get_files_in_path_for_types(test_example_paths):
    test_result = get_files_in_path(Path(test_example_paths))

    assert isinstance(test_result, list)
    assert isinstance(test_result[0], Path)

@pytest.mark.parametrize("test_example_paths", [
    (r"test\test_data")
    ])
def test_get_files_in_path_for_paths(test_example_paths):
    test_result = get_files_in_path(Path(test_example_paths))

    assert Path(r"test\test_data\Test_document.pdf") in test_result 
    assert Path(r"test\test_data\Test_document_zwei.pdf") in test_result
    assert len(test_result) == 5

def test_create_zip():
    test_path_zip = r"test\test_data\\test_zip\\test_zip.zip"
    test_path_for_zipping = r"test\test_data"

    test_result_zip_file = create_zip(test_path_for_zipping, test_path_zip)
    assert Path(test_path_zip).exists()