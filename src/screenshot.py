import os
import sys
import argparse
import pyautogui as sc


from src.setup_logger import logger


def check_path(dir_img_path: str) -> str:
    """checking if directory path exists"""
    state = True
    try:
        os.chdir(dir_img_path)  # checking if files/directory can be saved here
        state = True
    except FileNotFoundError as error:
        state = str(error)
    return state


def check_filename(img_path: str, dir_img_path: str) -> str:
    """Check filename

    Args:
        img_path (str): _description_
        dir_img_path (str): _description_

    Returns:
        str: image path if checked
    """
    try:
        os.chdir(dir_img_path)
        dir_list = list(os.walk("."))  # searching all files in directory
        all_files_in_dir = dir_list[0][2]
        exist = False
        counter = 1
        while True:
            for file in all_files_in_dir:
                if file in img_path:  # checking if file name already exists
                    exist = True
                    break
            if exist is True:
                filename = img_path.split(".")[0]  # splitting filename for changes
                x = 0
                elements_to_delete = []
                for (
                    element
                ) in filename:  # searching for numbers in already existed filename
                    try:
                        int(element)
                        elements_to_delete.append(x)
                        x += 1
                    except ValueError:
                        pass
                this_filename = list(filename)  # getting screenshot number
                for element in elements_to_delete:
                    this_filename[element] = ""
                filename = "".join(this_filename)
                img_path = (
                    filename + f"{str(counter)}." + img_path.split(".")[1]
                )  # new image path
            else:
                break
            counter += 1
    except Exception as error:
        logger.error(str(error))
        sys.exit()
    this_img_path = img_path
    return this_img_path


def shot(img_path: str, allowed_extensions: list[str]) -> None:
    """Create a screenshot from the current screen

    Args:
        img_path (str): path of the screenshot to be made
        allowed_extensions (list[tr]): List of possible extensions to save the screenshot to
    """
    dir_img_path_l = []
    if "/" in img_path:
        args = img_path.split("/")
        for arg in args:
            ext_found = False
            for extension in allowed_extensions:
                if extension in arg:
                    ext_found = True
                    break
            if ext_found is False:
                dir_img_path_l.append(arg)
        dir_img_path = "/".join(dir_img_path_l)
    else:
        dir_img_path = img_path
    path_state = check_path(dir_img_path)
    if path_state is not True:  # if directory path does not exist
        try:
            os.mkdir(dir_img_path)  # creating directory to save screenshots in
        except Exception as error:
            logger.error(f"Could not create path -> {dir_img_path} \n[!] {str(error)}")
            sys.exit()
    this_img_path = check_filename(img_path, dir_img_path)
    try:
        sc.screenshot().save(this_img_path)  # make and save screenshot
        logger.info(f"Saved screenshot at {this_img_path}")
    except Exception as error:
        logger.error(f"Could not make screenshot ({this_img_path}) \n[!] {str(error)}")


ALLOWED_EXTENSIONS = [".png", ".jpg"]

parser = argparse.ArgumentParser("Screenshot.py von Louai Almasri")
parser.add_argument(
    "-p",
    "--path",
    help="Path to image - Don't forget to add a file extension! ("
    + ",".join(ALLOWED_EXTENSIONS)
    + ")",
)
args = parser.parse_args()
if args.path is None:
    parser.print_help()
    logger.info(
        "Example: python3 screenshot.py --path /home/username/Documents/picture.png"
    )
    sys.exit()


if __name__ == "__main__":
    img_path = args.path
    if "." in img_path:
        shot(img_path, ALLOWED_EXTENSIONS)
    else:
        logger.critical("No path given")
