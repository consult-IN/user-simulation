from pathlib import Path

from PyPDF2 import PdfReader

from src.setup_logger import logger
from src.website_walking import BrowserAutomation
from src.mail_interactions import get_links_from_text


class PDFActions:
    """Provides functionality to extract text and click links in pdf files."""

    ALLOWED_EXTENSIONS: list[str] = [".pdf"]

    def get_text(self, path: str) -> list[str]:
        """
        Extracts the text from a pdf-file linewise

        Args:
            path (str): path to the pdf file which text should be extracted

        Returns:
            list[str]: the extracted text by line
        """
        file_path = self.check_path(path)
        with open(file_path, "rb") as file_handle:
            pdf = PdfReader(file_handle)
            content = [page.extract_text().strip(" \n") for page in pdf.pages]
        logger.info(f"Found links in pdf: {content}")
        return content

    def click_link(self, path: str) -> None:
        """
        Extracts the text and further its links from the given path to a pdf-file and requests it.

        Args:
            path (str): the path to the pdf-file containing text with links
        """
        joined_content = " ".join(self.get_text(path))
        selection = get_links_from_text(joined_content)

        BrowserAutomation(
            browser_visible=False, binary_location=None, driver_location=None
        ).walk_website(selection, link_clicks=0)
        logger.info(f"Found thes links in PDF:{selection}")

    def check_path(self, path: str) -> Path:
        """
        Checks the path for existance and the correct extension.

        Args:
            path (str): path to be checked

        Raises:
            Exception: on non-existing path
            Exception: on non-pdf file

        Returns:
            Path: checked and converted path object
        """
        file_path = Path(path)
        if not file_path.exists():
            raise Exception(f"Path not found: {file_path}")
        if file_path.suffix not in self.ALLOWED_EXTENSIONS:
            raise Exception(f"Instance cannot handle file type: {file_path}")
        return file_path


if __name__ == "__main__":
    test_path = Path("test/test_data/test_link.pdf")
    pdf_actions = PDFActions()

    print(pdf_actions.get_text(test_path))
    input(">>> Press [ENTER] to continue...")
    pdf_actions.click_link(test_path)
