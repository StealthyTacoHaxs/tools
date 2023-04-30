#!/usr/bin/env python3

import os
import sys
import shutil
import subprocess
import ruamel.yaml as yaml  # pip3 install ruamel.yaml
import argparse

parser = argparse.ArgumentParser(description="Install the dotfiles")
parser.add_argument(
    "-p",
    "--packages",
    help="Install packages",
    action="store_true")
parser.add_argument(
    "-b",
    "--bashrc",
    help="Install bashrc",
    action="store_true")
parser.add_argument(
    "-n",
    "--dry-run",
    help="Dry run",
    action="store_true"
)
args = parser.parse_args()

if args.dry_run:
    env_dir = os.path.join(os.getcwd(), ".env")
    if not os.path.exists(env_dir):
        os.makedirs(env_dir, exist_ok=True)
    HOME = env_dir
else:
    HOME = os.path.expanduser("~")

PATH = os.path.dirname(os.path.realpath(__file__))
PYTHON_SITE_PACKAGES = subprocess.check_output(
    ["python3", "-m", "site", "--user-site"]).decode("utf-8").strip()

PACKAGES = os.listdir(PATH + "/submodules")

def parse_remote_packages_list():
    with open(PATH + "/remote_packages.yml", "r") as f:
        remote_packages = yaml.load(f, Loader=yaml.Loader)
    return remote_packages

def install_packages():

    print("Installing python packages...")
    for package in PACKAGES:
        if not os.path.exists(PATH + "/submodules/" + package + "/setup.py"):
            continue
        print("Installing " + package + "...")
        subprocess.call(["pip3", "install", "-e", "submodules/" + package])

    print("Installing remote packages...")
    remote_packages = parse_remote_packages_list()
    if shutil.which("apt"):
        for package in remote_packages['apt']:
            print("Installing " + package + "...")
            subprocess.call(["sudo", "apt", "install", "-y", package])
    else:
        print("apt not found. Skipping apt packages.")

    if shutil.which("pip3") or shutil.which("pip"):
        if shutil.which("pip3"):
            pip = "pip3"
        else:
            pip = "pip"
        for package in remote_packages['pip']:
            print("Installing " + package + "...")
            subprocess.call([pip, "install", package])
    else:
        print("pip3 not found. Skipping pip packages.")

    if shutil.which("pipx"):
        for package in remote_packages['pipx']:
            print("Installing " + package + "...")
            subprocess.call(["pipx", "install", package])

    shell = get_shell()
    if shell == "bash":
        with open(HOME + "/.bashrc", "a") as f:
            f.write("\n# add python packages to path\n")
            f.write(
                "export PATH=$PATH:" +
                PYTHON_SITE_PACKAGES +
                ":" +
                HOME +
                "/.local/bin"
                "\n")
    elif shell == "fish":
        if not os.path.exists(HOME + "/.config/fish"):
            os.makedirs(HOME + "/.config/fish", exist_ok=True)
        with open(HOME + "/.config/fish/config.fish", "a") as f:
            f.write("\n# add python packages to path\n")
            f.write(
                "set -x PATH $PATH " +
                PYTHON_SITE_PACKAGES +
                " " +
                HOME +
                "/.local/bin"
                "\n")
    elif shell == "zsh":
        with open(HOME + "/.zshrc", "a") as f:
            f.write("\n# add python packages to path\n")
            f.write(
                "export PATH=$PATH:" +
                PYTHON_SITE_PACKAGES +
                ":" +
                HOME +
                "/.local/bin"
                "\n")
    else:
        print("Invalid shell.")
        sys.exit(1)

def get_shell():
    shell = os.environ.get("SHELL")
    if shell is None:
        print("SHELL could not be determined.")
        shell = input("Enter your shell (bash, fish, or zsh): ")
        if shell not in ["bash", "fish", "zsh"]:
            print("Invalid shell.")
            sys.exit(1)
    return shell


if __name__ == "__main__":
    if args.packages:
        install_packages()
        exit(0)
    if args.bashrc:
        pass
    if args._get_args() == []:
        print("No arguments given.")
        prompt = input("Would you like to install packages? (y/n) ")
        if prompt == "y":
            args.packages = True
        else:
            exit(1)
