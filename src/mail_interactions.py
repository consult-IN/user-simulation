import re
import random
from pathlib import Path
import win32com.client

from src.website_walking import BrowserAutomation
from src.create_zip import create_zip
from src.setup_logger import logger


class MailInteraction:
    """
    This class offers functionality to interact with the local instance of
    outlook on your machine.
    """

    def __init__(self) -> None:
        """
        (Constructor) Create the MAPi Interface for the outlook application.
        """
        self.outlook = win32com.client.Dispatch("outlook.application")
        self.mapi = self.outlook.GetNamespace("MAPI")

    def get_messages_in_folder(self):
        """Returns all the items in an outlook directory.

        Returns:
            _type_: Mail-Objects from pywin32
        """
        folder = self.mapi.GetDefaultFolder(6)
        return folder.Items

    def set_mail_status_on_read(self, message):
        """Marks the currently selected mail as read"""
        message.Unread = False

    def send_mail(
        self,
        receiver_address: str,
        subject: str = "Default",
        body: str = "This is a default text.",
        attachement_paths: list[str] = None,
        send=False,
    ):
        """
        This function accepts common inputs present in a mail as parameters and
        creates a mail-object inside your local outlook application for it to be sent.

        Args:
            receiver_address (str): the mail address of the receiver
            subject (str, optional): the mail's subject. Defaults to "Default".
            body (str, optional): the mail's body. Defaults to "This is a default text.".
            attachement_paths (list[str], optional): paths to attachements. Defaults to None.
            send (bool, optional): switch to either only look at the crafted mail or to actually
                send it away. Defaults to False.
        """
        msg = self.outlook.CreateItem(0)

        msg.To = receiver_address
        msg.Subject = subject
        msg.Body = body

        if attachement_paths is not None:
            for path in attachement_paths:
                msg.Attachments.Add(path)

        if send:
            msg.Send()
            logger.info(f"Mail sent to {receiver_address}")
        else:
            msg.Display()
            logger.info("Mail ready for inspection")

    @classmethod
    def get_message_body(cls, message):
        """Return the body of a given message object"""
        return message.body


def get_links_from_text(text: str) -> list[str]:
    """Extract the links from a text string via regex"""
    clean_links = [
        link.replace(">", "") for link in re.findall(r"(https?://[^\s]+)", text)
    ]
    return clean_links


def open_link_from_mail():
    """
    Function to use all the implemented functionaltiy to click on one link in all of the
    available mails in the default outlook folder.
    """
    mail_interaction = MailInteraction()
    message_bodies = [
        MailInteraction.get_message_body(message)
        for message in mail_interaction.get_messages_in_folder()
    ]
    all_available_links_in_messages = [
        get_links_from_text(message_body) for message_body in message_bodies
    ]

    only_allow_following_links = [
        "http://www.consultin.net/"
    ]  # Adjust to a filter criteria on which links to click
    all_available_links_in_messages = list(
        filter(
            lambda x: x in only_allow_following_links,
            sum(all_available_links_in_messages, []),
        )
    )

    BrowserAutomation(
        browser_visible=False, binary_location=None, driver_location=None
    ).walk_website(all_available_links_in_messages, 0)
    logger.info(all_available_links_in_messages)


def example_set_mail_status_on_read():
    """
    Example call of the function set_mail_status_on_read by extracting all unread messages
    and randomly choosing one to be set on "Read"
    """
    mail_interaction = MailInteraction()
    messages_unread = [
        message
        for message in mail_interaction.get_messages_in_folder()
        if message.Unread
    ]

    unread_message_to_set_on_read = random.choices(messages_unread, k=1)[0]
    mail_interaction.set_mail_status_on_read(unread_message_to_set_on_read)
    logger.info(f"Reading Status changed to: {unread_message_to_set_on_read.Unread}")


if __name__ == "__main__":
    TEST_SWITCH: str = "SET_UNREAD"  # choices: "SEND_MAIL" "SET_UNREAD" {other}

    ZIP_AND_SEND_RECEIVER_MAIL: str = "hello"
    ZIP_AND_SEND_SEND_SWITCH = False
    ZIP_AND_SEND_ATTACHEMENT_PATH: Path = Path(
        r"test\test_data\Test_document.pdf"
    ).resolve()

    if TEST_SWITCH == "SEND_MAIL":
        created_zip_path = create_zip(
            path_to_zip=ZIP_AND_SEND_ATTACHEMENT_PATH,
            path_of_zip=(ZIP_AND_SEND_ATTACHEMENT_PATH.parent / "test_zip.zip"),
        )
        mail_interaction = MailInteraction()
        mail_interaction.send_mail(
            receiver_address=ZIP_AND_SEND_RECEIVER_MAIL,
            attachement_paths=[str(created_zip_path)],
            send=ZIP_AND_SEND_SEND_SWITCH,
            subject="Your ZIP-Archive is ready!",
            body="Hi there! Please find your requested files attached.",
        )
    elif TEST_SWITCH == "SET_UNREAD":
        example_set_mail_status_on_read()
    else:
        open_link_from_mail()
