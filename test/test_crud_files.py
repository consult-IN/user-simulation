import pytest
from pathlib import Path

from src.crud.crud_files import CRUDFiles


@pytest.fixture
def testing_instance():
    test_instance = CRUDFiles([".txt", ".md", ".csv"])
    yield test_instance
    del test_instance


@pytest.fixture(params=["test_one.txt", "test_two.md", "test_three.csv"])
def available_files(request, tmp_path):
    tmp_file_path = tmp_path / Path(request.param)
    with open(tmp_file_path, "w"):
        pass
    return tmp_file_path


@pytest.mark.parametrize(
    "file_names_to_test", [("test_one.txt"), ("test_two.md"), ("test_three.csv")]
)
def test_create_path_file_not_present(
    testing_instance, tmp_path: Path, file_names_to_test: str
):
    test_result = testing_instance.create(tmp_path / file_names_to_test)
    assert test_result == tmp_path / file_names_to_test
    assert (tmp_path / file_names_to_test) in testing_instance.registered_paths


def test_create_path_file_already_exists(testing_instance, available_files: Path):
    test_result = testing_instance.create(available_files)
    assert test_result == available_files


@pytest.mark.parametrize(
    "file_paths_with_impossible_extension",
    [
        ("test_one.xlsx"),
        ("test_two.pptx"),
        ("test_three.docx"),
        ("test_four.unknown_extension"),
    ],
)
def test_create_path_extension_impossible(
    testing_instance, file_paths_with_impossible_extension
):
    with pytest.raises(Exception) as exc:
        _ = testing_instance.create(file_paths_with_impossible_extension)

    assert file_paths_with_impossible_extension in exc.value.args[0]
    assert "Extension of path cannot be handled by this instance" in exc.value.args[0]


# ---- read_file


@pytest.mark.parametrize(
    "test_file_with_content, actual_content",
    [("test/test_data/test_file.txt", "Hello World!")],
)
def test_read_file_content_type(
    testing_instance, test_file_with_content, actual_content
):
    test_result = testing_instance.read(test_file_with_content)

    assert isinstance(test_result, list)
    assert isinstance(test_result[0], str)
    assert test_result[0] == actual_content
    assert Path(test_file_with_content) in testing_instance.registered_paths


# ---- delete_file


def test_delete_file(testing_instance: CRUDFiles, available_files: Path):
    test_result = testing_instance.delete(available_files)

    assert isinstance(test_result, Path)
    assert test_result == available_files
    assert Path(available_files) in testing_instance.registered_paths

# ---- update file

def test_update_file(testing_instance: CRUDFiles, available_files: Path):
    content_to_add: list[str] = ["Hello \n", "World \n", "From \n", "Test \n"]

    test_result = testing_instance.update(available_files, content_to_append=content_to_add)

    assert isinstance(test_result, Path)
    assert Path(test_result) in testing_instance.registered_paths