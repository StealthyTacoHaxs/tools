#!/usr/bin/env python3

import os
import sys
import shutil
import subprocess
import argparse

HOME = os.path.expanduser("~")
PATH = os.path.dirname(os.path.realpath(__file__))
PYTHON_SITE_PACKAGES = subprocess.check_output(
    ["python3", "-m", "site", "--user-site"]).decode("utf-8").strip()

PYTHON_PACKAGES = [
    "dirsearch"
]

def install_python_packages():
    print("Installing python packages...")
    for package in PYTHON_PACKAGES:
        subprocess.call(["pip3", "install", "-e", "submodules/" + package])
    # add python packages to path
    shell = get_shell()
    if shell == "bash":
        with open(HOME + "/.bashrc", "a") as f:
            f.write("\n# add python packages to path\n")
            f.write("export PATH=$PATH:" + PYTHON_SITE_PACKAGES + "\n")
    elif shell == "fish":
        if not os.path.exists(HOME + "/.config/fish"):
            os.makedirs(HOME + "/.config/fish")
        with open(HOME + "/.config/fish/config.fish", "a") as f:
            f.write("\n# add python packages to path\n")
            f.write("set -x PATH $PATH " + PYTHON_SITE_PACKAGES + "\n")
    elif shell == "zsh":
        with open(HOME + "/.zshrc", "a") as f:
            f.write("\n# add python packages to path\n")
            f.write("export PATH=$PATH:" + PYTHON_SITE_PACKAGES + "\n")
    else:
        print("Invalid shell.")
        sys.exit(1)

def get_shell():
    shell = os.environ.get("SHELL")
    if shell is None:
        print("SHELL could not be determined.")
        # allow the user to specify bash, fish, or zsh
        shell = input("Enter your shell (bash, fish, or zsh): ")
        if shell not in ["bash", "fish", "zsh"]:
            print("Invalid shell.")
            sys.exit(1)
    return shell


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Install the dotfiles")
    parser.add_argument(
        "-p",
        "--python",
        help="Install python packages",
        action="store_true")
    parser.add_argument(
        "-b",
        "--bashrc",
        help="Install bashrc",
        action="store_true")
    args = parser.parse_args()

    if args.python:
        install_python_packages()
    if args.bashrc:
        pass
