import pytest

from pathlib import Path

from src.pdf_actions import PDFActions


@pytest.fixture
def testing_instance():
    return PDFActions()


@pytest.mark.parametrize("test_path", [(r"test\test_data\test_link.pdf")])
def test_check_path(testing_instance: PDFActions, test_path: str):
    test_result = testing_instance.check_path(test_path)
    assert isinstance(test_result, Path)


@pytest.mark.parametrize("test_path", [("hello.md"), (r"test\test_data\test_file.txt")])
def test_check_path_no_existance(testing_instance: PDFActions, test_path: str):

    with pytest.raises(Exception):
        _ = testing_instance.check_path(test_path)


# --- get_text
@pytest.mark.parametrize(
    "test_path, actual_content",
    [
        (
            r"test\test_data\test_link.pdf",
            ["http://www.consultin.net/", "https://www.wikipedia.org/"],
        )
    ],
)
def test_get_text(
    testing_instance: PDFActions, test_path: str, actual_content: list[str]
) -> None:
    test_result = testing_instance.get_text(test_path)

    assert isinstance(test_result, list)
    assert isinstance(test_result[0], str)
    assert test_result == actual_content


# --- click_link


@pytest.mark.parametrize("test_path", [(r"test\test_data\test_link.pdf")])
def test_click_link(testing_instance: PDFActions, test_path: str) -> None:
    try:
        _ = testing_instance.click_link(test_path)
    except Exception:
        assert False, f"The call to the link inside the pdf has not worked: {test_path}"
