import sys
import os
import threading
import subprocess
import argparse
import time
from rich import pretty, console as cons


class Backdoor:
    """Provides functionality for creating subprocesses via a command given to the class"""

    def __init__(self, console, args):
        """
        (Constructor) Initiates the console object and the args for the backdoor application
        """
        self.console = console
        self.args = args

    def handle_thread(self):
        """Setup and create the thread from the command and specified args"""
        commands_args = self.args.commands
        if "," in commands_args:
            all_commands = commands_args.split(",")
        else:
            all_commands = commands_args.split(" ")
        self.console.log("Started Thread")
        with self.console.status(f"Executing {len(all_commands)} Commands..."):
            for command in all_commands:
                try:
                    command_output = subprocess.run(
                        command.split(" "),
                        capture_output=True,
                        text=True,
                        shell=True,
                        check=True,
                    )
                    self.console.log(
                        f"Executed command [bold white]'{command}'"
                        + f"[yellow]->[green] {command_output.stdout}"
                    )
                except Exception as error:
                    self.console.log(
                        f"[bold red] An error occurred while executing a command. \n {str(error)}"
                    )
        self.console.log("[red]Closed Thread")
        time.sleep(10)
        sys.exit()

    def run(self):
        """Execute the command in a thread"""
        self.console.log("[bold green] Started Backdoor")
        back_thread = threading.Thread(target=self.handle_thread, args=())
        back_thread.setDaemon(False)  # Running in background
        back_thread.start()
        self.console.log("[bold yellow] Closed Backdoor")


#
parser = argparse.ArgumentParser("Backdoor.py - Louai")
parser.add_argument("-c", "--commands", help="Commands to execute", required=True)
args = parser.parse_args()

if args.commands is None:
    parser.print_help()
    sys.exit()

pretty.install()
console = cons.Console()
#

if __name__ == "__main__":
    os.system("cls")  # Windows
    Backdoor(console, args).run()
